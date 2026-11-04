"""Write web/src/api/client.ts from the FastAPI OpenAPI schema."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app  # noqa: E402

OUT = ROOT / "web" / "src" / "api" / "client.ts"


def ts_type(schema: dict) -> str:
    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]
    if "anyOf" in schema:
        return " | ".join(ts_type(item) for item in schema["anyOf"])
    if "allOf" in schema:
        return " & ".join(ts_type(item) for item in schema["allOf"])
    kind = schema.get("type")
    if kind == "array":
        item = ts_type(schema.get("items") or {"type": "unknown"})
        if "|" in item or "&" in item:
            item = f"({item})"
        return f"{item}[]"
    return {
        "string": "string",
        "integer": "number",
        "number": "number",
        "boolean": "boolean",
        "null": "null",
        "object": "Record<string, unknown>",
    }.get(kind or "", "unknown")


def emit_interface(name: str, schema: dict) -> str:
    required = set(schema.get("required") or [])
    lines = [f"export interface {name} {{"]
    for prop, prop_schema in (schema.get("properties") or {}).items():
        optional = "" if prop in required else "?"
        lines.append(f"  {prop}{optional}: {ts_type(prop_schema)};")
    lines.append("}")
    return "\n".join(lines)


def response_type(operation: dict) -> str:
    for code in ("200", "201"):
        response = (operation.get("responses") or {}).get(code) or {}
        schema = ((response.get("content") or {}).get("application/json") or {}).get("schema")
        if schema:
            return ts_type(schema)
    return "void"


def emit_operation(path: str, method: str, operation: dict) -> str:
    op_id = operation["operationId"]
    path_params: list[tuple[str, str]] = []
    query_params: list[tuple[str, str]] = []
    for param in operation.get("parameters") or []:
        name = param["name"]
        kind = ts_type(param.get("schema") or {"type": "string"})
        if param.get("in") == "path":
            path_params.append((name, kind))
        elif param.get("in") == "query":
            query_params.append((name, kind))
    body_schema = None
    request_body = operation.get("requestBody") or {}
    body_json = ((request_body.get("content") or {}).get("application/json") or {}).get("schema")
    if body_json:
        body_schema = ts_type(body_json)
    args = [f"{name}: {kind}" for name, kind in path_params]
    args.extend(f"{name}: {kind}" for name, kind in query_params)
    if body_schema:
        args.append(f"body: {body_schema}")
    url = path
    for name, _kind in path_params:
        url = url.replace("{" + name + "}", "${" + name + "}")
    ret = response_type(operation)
    lines = [f"export async function {op_id}({', '.join(args)}): Promise<{ret}> {{"]
    if query_params:
        lines.append("  const params = new URLSearchParams();")
        for name, _kind in query_params:
            lines.append(f"  params.set({json_string(name)}, String({name}));")
        lines.append(f"  const path = `{url}?${{params.toString()}}`;")
    else:
        lines.append(f"  const path = `{url}`;")
    body_arg = ", body" if body_schema else ""
    lines.append(f"  return request<{ret}>(\"{method.upper()}\", path{body_arg});")
    lines.append("}")
    return "\n".join(lines)


def json_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    spec = app.openapi()
    schemas = (spec.get("components") or {}).get("schemas") or {}
    parts = [
        "// Generated from the FastAPI OpenAPI schema. Do not edit by hand.",
        "// Regenerate with: uv run python scripts/generate_openapi_client.py",
        "",
        "export class ApiError extends Error {",
        "  readonly status: number;",
        "",
        "  constructor(detail: string, status: number) {",
        "    super(detail);",
        '    this.name = "ApiError";',
        "    this.status = status;",
        "  }",
        "}",
        "",
        "async function request<T>(method: string, path: string, body?: unknown): Promise<T> {",
        "  const response = await fetch(path, {",
        "    method,",
        '    headers: body === undefined ? undefined : { "Content-Type": "application/json" },',
        "    body: body === undefined ? undefined : JSON.stringify(body),",
        "  });",
        "  if (!response.ok) {",
        '    let detail = "Couldn\'t save.";',
        "    try {",
        "      const data: unknown = await response.json();",
        '      if (data !== null && typeof data === "object" && "detail" in data && typeof data.detail === "string") {',
        "        detail = data.detail;",
        "      }",
        "    } catch {",
        "      /* The response was not JSON. Keep the fallback detail. */",
        "    }",
        "    throw new ApiError(detail, response.status);",
        "  }",
        "  if (response.status === 204) {",
        "    return undefined as T;",
        "  }",
        "  return (await response.json()) as T;",
        "}",
        "",
    ]
    for name in sorted(schemas):
        schema = schemas[name]
        if schema.get("type") == "object" or "properties" in schema:
            parts.append(emit_interface(name, schema))
            parts.append("")
    operations: list[tuple[str, str, dict]] = []
    for path, methods in (spec.get("paths") or {}).items():
        for method, operation in methods.items():
            if method.startswith("x-") or not isinstance(operation, dict):
                continue
            if "operationId" not in operation:
                continue
            operations.append((path, method, operation))
    operations.sort(key=lambda item: item[2]["operationId"])
    for path, method, operation in operations:
        parts.append(emit_operation(path, method, operation))
        parts.append("")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.errors import AppError
from app.routers import copies, health, lists, todos, views

DIST = Path(__file__).resolve().parents[2] / "web" / "dist"


def _detail_text(detail: object) -> str:
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):
        parts: list[str] = []
        for item in detail:
            if isinstance(item, dict):
                loc = [str(part) for part in item.get("loc", []) if part not in ("body", "query")]
                message = str(item.get("msg", "Invalid request"))
                parts.append(f"{'.'.join(loc)}: {message}" if loc else message)
            else:
                parts.append(str(item))
        return "; ".join(parts) if parts else "Invalid request"
    return str(detail)


def create_app() -> FastAPI:
    app = FastAPI(title="Todo App", docs_url=None, redoc_url=None)
    app.include_router(health.router)
    app.include_router(lists.router)
    app.include_router(todos.router)
    app.include_router(views.router)
    app.include_router(copies.router)

    @app.exception_handler(AppError)
    async def app_error_handler(_request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": _detail_text(exc.errors())})

    @app.exception_handler(HTTPException)
    async def http_handler(_request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": _detail_text(exc.detail)})

    @app.api_route("/docs", methods=["GET", "HEAD"], include_in_schema=False)
    @app.api_route("/redoc", methods=["GET", "HEAD"], include_in_schema=False)
    def interactive_docs_off() -> None:
        raise HTTPException(status_code=404, detail="Not found")

    def openapi() -> dict:
        if app.openapi_schema:
            return app.openapi_schema
        schema = get_openapi(title=app.title, version=app.version, routes=app.routes)
        schemas = schema.setdefault("components", {}).setdefault("schemas", {})
        schemas["ErrorOut"] = {
            "properties": {"detail": {"type": "string", "title": "Detail"}},
            "type": "object",
            "required": ["detail"],
            "title": "ErrorOut",
        }
        for path_item in schema.get("paths", {}).values():
            for operation in path_item.values():
                if isinstance(operation, dict) and "422" in operation.get("responses", {}):
                    operation["responses"]["422"] = {
                        "description": "Error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorOut"},
                            }
                        },
                    }
        schemas.pop("HTTPValidationError", None)
        schemas.pop("ValidationError", None)
        app.openapi_schema = schema
        return schema

    app.openapi = openapi

    if DIST.is_dir():
        assets = DIST / "assets"
        if assets.is_dir():
            app.mount("/assets", StaticFiles(directory=assets), name="assets")

        @app.get("/{full_path:path}", include_in_schema=False)
        def frontend(full_path: str) -> FileResponse:
            if full_path == "api" or full_path.startswith("api/") or full_path.startswith("openapi"):
                raise HTTPException(status_code=404, detail="Not found")
            root = DIST.resolve()
            candidate = (DIST / full_path).resolve()
            if full_path and candidate.is_file() and candidate.is_relative_to(root):
                return FileResponse(candidate)
            return FileResponse(DIST / "index.html")

    return app


app = create_app()

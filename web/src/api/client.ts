// Generated from the FastAPI OpenAPI schema. Do not edit by hand.
// Regenerate with: uv run python scripts/generate_openapi_client.py

export class ApiError extends Error {
  readonly status: number;

  constructor(detail: string, status: number) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const response = await fetch(path, {
    method,
    headers: body === undefined ? undefined : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    let detail = "Couldn't save.";
    try {
      const data: unknown = await response.json();
      if (data !== null && typeof data === "object" && "detail" in data && typeof data.detail === "string") {
        detail = data.detail;
      }
    } catch {
      /* The response was not JSON. Keep the fallback detail. */
    }
    throw new ApiError(detail, response.status);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}

export interface CopyCreate {
  source_list_id?: number | null;
  destination_list_id?: number | null;
  on_date?: string | null;
}

export interface CopyOut {
  id: number;
  todos: TodoOut[];
}

export interface ErrorOut {
  detail: string;
}

export interface ListCreate {
  name?: string | null;
}

export interface ListOut {
  id: number;
  name: string;
  position: number;
}

export interface ListUpdate {
  name?: string | null;
}

export interface PeriodOut {
  grain: string;
  anchor: string;
  todos: TodoOut[];
  undated: TodoOut[];
}

export interface TodayOut {
  on_date: string;
  todos: TodoOut[];
  next_todo_id: number | null;
}

export interface TodoCreate {
  title?: string | null;
  priority?: number | null;
  state?: string | null;
  notes?: string | null;
  on_date?: string | null;
  at_time?: string | null;
  alarm_at?: string | null;
  person_name?: string | null;
  parent_id?: number | null;
  position?: number | null;
}

export interface TodoOut {
  id: number;
  list_id: number;
  parent_id: number | null;
  position: number;
  title: string;
  state: string;
  priority: number;
  notes: string;
  on_date: string | null;
  at_time: string | null;
  alarm_at: string | null;
  person_name: string | null;
  copy_id: number | null;
  copy_confirmed: boolean;
}

export interface TodoPatch {
  title?: string | null;
  priority?: number | null;
  state?: string | null;
  notes?: string | null;
  on_date?: string | null;
  at_time?: string | null;
  alarm_at?: string | null;
  person_name?: string | null;
  position?: number | null;
}

export async function confirm_copy(copy_id: number): Promise<CopyOut> {
  const path = `/api/copies/${copy_id}/confirm`;
  return request<CopyOut>("POST", path);
}

export async function create_copy(body: CopyCreate): Promise<CopyOut> {
  const path = `/api/copies`;
  return request<CopyOut>("POST", path, body);
}

export async function create_list(body: ListCreate): Promise<ListOut> {
  const path = `/api/lists`;
  return request<ListOut>("POST", path, body);
}

export async function create_todo(list_id: number, body: TodoCreate): Promise<TodoOut> {
  const path = `/api/lists/${list_id}/todos`;
  return request<TodoOut>("POST", path, body);
}

export async function delete_list(list_id: number): Promise<void> {
  const path = `/api/lists/${list_id}`;
  return request<void>("DELETE", path);
}

export async function delete_todo(todo_id: number): Promise<void> {
  const path = `/api/todos/${todo_id}`;
  return request<void>("DELETE", path);
}

export async function get_copy(copy_id: number): Promise<CopyOut> {
  const path = `/api/copies/${copy_id}`;
  return request<CopyOut>("GET", path);
}

export async function get_not_done(): Promise<TodoOut[]> {
  const path = `/api/views/not-done`;
  return request<TodoOut[]>("GET", path);
}

export async function get_period(grain: string, anchor: string): Promise<PeriodOut> {
  const params = new URLSearchParams();
  params.set("grain", String(grain));
  params.set("anchor", String(anchor));
  const path = `/api/views/period?${params.toString()}`;
  return request<PeriodOut>("GET", path);
}

export async function get_today(on_date: string): Promise<TodayOut> {
  const params = new URLSearchParams();
  params.set("on_date", String(on_date));
  const path = `/api/views/today?${params.toString()}`;
  return request<TodayOut>("GET", path);
}

export async function get_todo(todo_id: number): Promise<TodoOut> {
  const path = `/api/todos/${todo_id}`;
  return request<TodoOut>("GET", path);
}

export async function list_lists(): Promise<ListOut[]> {
  const path = `/api/lists`;
  return request<ListOut[]>("GET", path);
}

export async function list_todos(list_id: number): Promise<TodoOut[]> {
  const path = `/api/lists/${list_id}/todos`;
  return request<TodoOut[]>("GET", path);
}

export async function update_list(list_id: number, body: ListUpdate): Promise<ListOut> {
  const path = `/api/lists/${list_id}`;
  return request<ListOut>("PATCH", path, body);
}

export async function update_todo(todo_id: number, body: TodoPatch): Promise<TodoOut> {
  const path = `/api/todos/${todo_id}`;
  return request<TodoOut>("PATCH", path, body);
}

from sqlalchemy import text

from app.db import engine


def test_matrix_open_site(client):
    assert client.get("/docs").status_code == 404
    assert client.get("/redoc").status_code == 404
    assert client.get("/docs").json()["detail"]
    paths = " ".join(client.app.openapi()["paths"])
    for banned in ("calendar", "login", "signin", "sign-in", "auth", "alarm", "account"):
        assert banned not in paths
    with engine.connect() as connection:
        tables = connection.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        ).scalars().all()
    assert {"lists", "todos", "copies"} <= set(tables)
    assert "accounts" not in tables
    assert "users" not in tables
    assert client.get("/api/lists").json() == []
    assert client.get("/api/views/not-done").json() == []


def test_matrix_today_and_not_done(client, detail, make_list, make_todo):
    row = make_list("Saturday")
    done = make_todo(row["id"], title="English drop-off", priority=5, position=1, state="done", on_date="2026-11-07", at_time="09:00:00")
    partial = make_todo(
        row["id"],
        title="English pickup",
        priority=4,
        position=2,
        state="partial",
        notes="traffic",
        on_date="2026-11-07",
        at_time="10:00:00",
    )
    later = make_todo(row["id"], title="Ballet drop-off", priority=3, position=3, on_date="2026-11-07")
    other_day = make_todo(row["id"], title="Ballet pickup", priority=2, position=4, on_date="2026-11-14", at_time="14:30:00")
    undated = make_todo(row["id"], title="Costco", priority=1, position=5)

    missing = client.get("/api/views/today")
    assert missing.status_code == 422
    detail(missing)

    today = client.get("/api/views/today", params={"on_date": "2026-11-07"})
    assert today.status_code == 200
    body = today.json()
    assert body["on_date"] == "2026-11-07"
    assert [item["id"] for item in body["todos"]] == [done["id"], partial["id"], later["id"]]
    assert later["at_time"] is None
    assert body["next_todo_id"] == partial["id"]
    assert "T" not in body["on_date"]

    open_rows = client.get("/api/views/not-done").json()
    open_ids = {item["id"] for item in open_rows}
    assert partial["id"] in open_ids
    assert later["id"] in open_ids
    assert other_day["id"] in open_ids
    assert undated["id"] in open_ids
    assert done["id"] not in open_ids
    assert all(item["copy_confirmed"] is True for item in open_rows)

    client.patch(f"/api/todos/{partial['id']}", json={"state": "done"})
    client.patch(f"/api/todos/{later['id']}", json={"state": "done"})
    finished = client.get("/api/views/today", params={"on_date": "2026-11-07"}).json()
    assert [item["id"] for item in finished["todos"]] == [done["id"], partial["id"], later["id"]]
    assert finished["next_todo_id"] is None
    empty = client.get("/api/views/today", params={"on_date": "2026-11-08"}).json()
    assert empty["todos"] == []
    assert empty["next_todo_id"] is None

    pending = client.post(
        "/api/copies",
        json={"source_list_id": row["id"], "destination_list_id": row["id"], "on_date": "2026-11-07"},
    )
    assert pending.status_code == 201
    copied_ids = {item["id"] for item in pending.json()["todos"]}
    refreshed = client.get("/api/views/today", params={"on_date": "2026-11-07"}).json()
    assert copied_ids.isdisjoint({item["id"] for item in refreshed["todos"]})
    not_done_ids = {item["id"] for item in client.get("/api/views/not-done").json()}
    assert copied_ids.isdisjoint(not_done_ids)


def test_matrix_period(client, detail, make_list, make_todo):
    row = make_list("Saturday")
    monday = make_todo(row["id"], title="Monday", priority=1, position=2, on_date="2026-11-02")
    sunday = make_todo(row["id"], title="Sunday", priority=5, position=1, on_date="2026-11-08")
    previous = make_todo(row["id"], title="Previous", priority=3, on_date="2026-11-01")
    next_week = make_todo(row["id"], title="Next", priority=3, on_date="2026-11-09")
    dated_notime = make_todo(row["id"], title="Rest", priority=2, on_date="2026-11-04")
    undated = make_todo(row["id"], title="No date row", priority=4)
    december = make_todo(row["id"], title="December", priority=1, on_date="2026-12-01")
    other_year = make_todo(row["id"], title="Next year", priority=1, on_date="2027-01-01")

    day = client.get("/api/views/period", params={"grain": "day", "anchor": "2026-11-04"}).json()
    assert day["grain"] == "day"
    assert day["anchor"] == "2026-11-04"
    assert [item["id"] for item in day["todos"]] == [dated_notime["id"]]
    assert [item["id"] for item in day["undated"]] == [undated["id"]]

    week = client.get("/api/views/period", params={"grain": "week", "anchor": "2026-11-04"}).json()
    week_ids = [item["id"] for item in week["todos"]]
    assert week_ids == [monday["id"], dated_notime["id"], sunday["id"]]
    assert previous["id"] not in week_ids
    assert next_week["id"] not in week_ids
    assert [item["id"] for item in week["undated"]] == [undated["id"]]
    assert week["todos"][0]["on_date"] < week["todos"][-1]["on_date"]
    assert sunday["priority"] == 5
    assert week_ids[0] != sunday["id"]

    month = client.get("/api/views/period", params={"grain": "month", "anchor": "2026-11-15"}).json()
    month_ids = {item["id"] for item in month["todos"]}
    assert {monday["id"], sunday["id"], previous["id"], next_week["id"], dated_notime["id"]} <= month_ids
    assert december["id"] not in month_ids

    year = client.get("/api/views/period", params={"grain": "year", "anchor": "2026-06-01"}).json()
    year_ids = {item["id"] for item in year["todos"]}
    assert december["id"] in year_ids
    assert other_year["id"] not in year_ids
    assert undated["id"] not in year_ids
    assert undated["id"] in {item["id"] for item in year["undated"]}

    pending = client.post(
        "/api/copies",
        json={"source_list_id": row["id"], "destination_list_id": row["id"], "on_date": "2026-11-04"},
    )
    copied_ids = {item["id"] for item in pending.json()["todos"]}
    again = client.get("/api/views/period", params={"grain": "day", "anchor": "2026-11-04"}).json()
    visible = {item["id"] for item in again["todos"]} | {item["id"] for item in again["undated"]}
    assert copied_ids.isdisjoint(visible)

    for params in (
        {"anchor": "2026-11-04"},
        {"grain": "decade", "anchor": "2026-11-04"},
        {"grain": "week", "anchor": "11/04/2026"},
    ):
        rejected = client.get("/api/views/period", params=params)
        assert rejected.status_code == 422
        detail(rejected)

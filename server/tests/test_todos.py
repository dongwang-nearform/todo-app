from sqlalchemy import text

from app.db import engine


def test_matrix_create_todo_priority_and_no_autoselect(client, detail, make_list, make_todo):
    target = make_list("Saturday")
    other = make_list("Errands")
    assert client.get(f"/api/lists/{target['id']}/todos").json() == []
    assert client.get("/api/views/not-done").json() == []

    low = make_todo(target["id"], title="Costco", priority=1, position=2)
    high = make_todo(target["id"], title="English drop-off", priority=5, position=1)
    assert low["state"] == "not_done"
    assert low["copy_confirmed"] is True
    assert high["copy_confirmed"] is True
    listed = client.get(f"/api/lists/{target['id']}/todos").json()
    assert [row["id"] for row in listed] == [high["id"], low["id"]]
    assert [row["priority"] for row in listed] == [5, 1]
    blob = listed[0]
    assert "quick_to_finish" not in blob
    assert "quick" not in blob
    assert "recommended" not in blob
    assert "progress" not in blob
    assert client.get(f"/api/lists/{other['id']}/todos").json() == []

    for payload in (
        {"priority": 5},
        {"title": "Milk"},
        {"title": "   ", "priority": 3},
        {"title": "Milk", "priority": 0},
        {"title": "Milk", "priority": 6},
    ):
        rejected = client.post(f"/api/lists/{target['id']}/todos", json=payload)
        assert rejected.status_code == 422, payload
        detail(rejected)
    assert len(client.get(f"/api/lists/{target['id']}/todos").json()) == 2

    missing_list = client.post("/api/lists/9999/todos", json={"title": "Milk", "priority": 1})
    assert missing_list.status_code == 404
    detail(missing_list)


def test_matrix_update_and_delete(client, detail, make_list, make_todo):
    first = make_list("Saturday")
    second = make_list("Errands")
    todo = make_todo(first["id"], title="Costco", priority=2, position=1)
    other = make_todo(second["id"], title="Milk", priority=3)

    updated = client.patch(
        f"/api/todos/{todo['id']}",
        json={"title": "Costco run", "priority": 4, "position": 3},
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["title"] == "Costco run"
    assert body["priority"] == 4
    assert body["position"] == 3
    assert client.get(f"/api/lists/{first['id']}/todos").json()[0]["title"] == "Costco run"

    rejected = client.patch(f"/api/todos/{todo['id']}", json={"title": "Ignored", "priority": 9})
    assert rejected.status_code == 422
    detail(rejected)
    stored = client.get(f"/api/todos/{todo['id']}").json()
    assert stored["priority"] == 4
    assert stored["title"] == "Costco run"

    unknown = client.patch("/api/todos/9999", json={"title": "Nope"})
    assert unknown.status_code == 404
    detail(unknown)
    unknown_delete = client.delete("/api/todos/9999")
    assert unknown_delete.status_code == 404
    detail(unknown_delete)

    deleted = client.delete(f"/api/todos/{todo['id']}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/api/lists/{first['id']}/todos").json() == []
    assert client.get(f"/api/todos/{todo['id']}").status_code == 404
    assert client.get(f"/api/lists/{second['id']}/todos").json()[0]["id"] == other["id"]


def test_matrix_done_and_partial(client, detail, make_list, make_todo):
    row = make_list("Saturday")
    todo = make_todo(row["id"], title="Ballet", priority=4, notes="studio")

    done = client.patch(f"/api/todos/{todo['id']}", json={"state": "done"})
    assert done.status_code == 200
    assert done.json()["state"] == "done"
    assert client.get(f"/api/lists/{row['id']}/todos").json()[0]["state"] == "done"

    reopened = client.patch(f"/api/todos/{todo['id']}", json={"state": "not_done"})
    assert reopened.json()["state"] == "not_done"

    partial = client.patch(
        f"/api/todos/{todo['id']}",
        json={"state": "partial", "notes": "left early", "progress": 40, "percent": "50%", "count": 2},
    )
    assert partial.status_code == 200
    body = partial.json()
    assert body["state"] == "partial"
    assert body["notes"] == "left early"
    assert "progress" not in body
    assert "percent" not in body
    assert "count" not in body
    with engine.connect() as connection:
        columns = connection.execute(
            text("SELECT column_name FROM information_schema.columns WHERE table_name = 'todos'")
        ).scalars().all()
    assert "progress" not in columns
    assert "percent" not in columns

    finished = client.patch(f"/api/todos/{todo['id']}", json={"state": "done"})
    assert finished.json()["state"] == "done"
    assert finished.json()["notes"] == "left early"
    again = client.patch(f"/api/todos/{todo['id']}", json={"state": "not_done"})
    assert again.json()["state"] == "not_done"
    assert again.json()["notes"] == "left early"

    rejected = client.patch(f"/api/todos/{todo['id']}", json={"state": "started"})
    assert rejected.status_code == 422
    detail(rejected)
    assert client.get(f"/api/todos/{todo['id']}").json()["state"] == "not_done"

    hidden = client.patch(f"/api/todos/{todo['id']}", json={"copy_confirmed": False, "copy_id": 4})
    assert hidden.status_code == 200
    assert hidden.json()["copy_confirmed"] is True
    assert hidden.json()["copy_id"] is None


def test_matrix_time_and_alarm(client, detail, make_list, make_todo):
    row = make_list("Saturday")
    clocks = {
        "English drop-off": "09:00:00",
        "English pickup": "10:00:00",
        "Ballet drop-off": "13:00:00",
        "Ballet pickup": "14:30:00",
    }
    for title, at_time in clocks.items():
        stored = make_todo(row["id"], title=title, priority=3, on_date="2026-11-07", at_time=at_time)
        assert stored["on_date"] == "2026-11-07"
        assert stored["at_time"] == at_time
        assert "+" not in stored["at_time"]
        assert "T" not in stored["on_date"]

    with engine.connect() as connection:
        types = dict(
            connection.execute(
                text(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'todos' AND column_name IN ('on_date', 'at_time', 'alarm_at')
                    """
                )
            ).all()
        )
    assert types["on_date"] == "date"
    assert types["at_time"] == "time without time zone"
    assert types["alarm_at"] == "time without time zone"

    todo = make_todo(row["id"], title="Home", priority=2, on_date="2026-11-07", at_time="11:00:00")
    cleared = client.patch(f"/api/todos/{todo['id']}", json={"on_date": None})
    assert cleared.json()["on_date"] is None
    assert cleared.json()["at_time"] == "11:00:00"
    cleared_time = client.patch(f"/api/todos/{todo['id']}", json={"at_time": None})
    assert cleared_time.json()["at_time"] is None
    assert cleared_time.json()["on_date"] is None

    bad_date = client.patch(f"/api/todos/{todo['id']}", json={"on_date": "11/07/2026", "at_time": "12:00:00"})
    assert bad_date.status_code == 422
    detail(bad_date)
    bad_time = client.patch(f"/api/todos/{todo['id']}", json={"at_time": "09:00"})
    assert bad_time.status_code == 422
    detail(bad_time)
    stored = client.get(f"/api/todos/{todo['id']}").json()
    assert stored["on_date"] is None
    assert stored["at_time"] is None

    timed = client.patch(f"/api/todos/{todo['id']}", json={"at_time": "09:00:00", "alarm_at": "08:30:00"})
    assert timed.status_code == 200
    assert timed.json()["alarm_at"] == "08:30:00"
    paths = " ".join(client.app.openapi()["paths"])
    assert "alarm" not in paths
    assert "calendar" not in paths

    bare = make_todo(row["id"], title="Rest", priority=1)
    rejected = client.patch(f"/api/todos/{bare['id']}", json={"alarm_at": "08:00:00"})
    assert rejected.status_code == 422
    detail(rejected)
    assert client.get(f"/api/todos/{bare['id']}").json()["alarm_at"] is None

    kept = client.patch(f"/api/todos/{todo['id']}", json={"at_time": None})
    assert kept.status_code == 422
    detail(kept)
    current = client.get(f"/api/todos/{todo['id']}").json()
    assert current["at_time"] == "09:00:00"
    assert current["alarm_at"] == "08:30:00"

    both = client.patch(f"/api/todos/{todo['id']}", json={"at_time": None, "alarm_at": None})
    assert both.status_code == 200
    assert both.json()["at_time"] is None
    assert both.json()["alarm_at"] is None

    no_alarm = make_todo(row["id"], title="Undated", priority=1)
    assert no_alarm["at_time"] is None
    assert no_alarm["alarm_at"] is None


def test_matrix_subtodos_and_person(client, detail, make_list, make_todo):
    row = make_list("Saturday")
    other = make_list("Errands")
    parent = make_todo(row["id"], title="Ballet", priority=5)
    child = make_todo(row["id"], title="Shoes", priority=2, parent_id=parent["id"])
    sibling = make_todo(row["id"], title="Costco", priority=3)
    assert child["parent_id"] == parent["id"]
    listed = client.get(f"/api/lists/{row['id']}/todos").json()
    assert {item["id"] for item in listed} == {parent["id"], child["id"], sibling["id"]}

    missing = client.post(
        f"/api/lists/{row['id']}/todos",
        json={"title": "Lost", "priority": 1, "parent_id": 9999},
    )
    assert missing.status_code == 422
    detail(missing)
    cross = client.post(
        f"/api/lists/{other['id']}/todos",
        json={"title": "Lost", "priority": 1, "parent_id": parent["id"]},
    )
    assert cross.status_code == 422
    detail(cross)
    assert len(client.get(f"/api/lists/{other['id']}/todos").json()) == 0

    named = client.patch(f"/api/todos/{sibling['id']}", json={"person_name": "his wife"})
    assert named.json()["person_name"] == "his wife"
    daughter = client.patch(f"/api/todos/{parent['id']}", json={"person_name": "his daughter"})
    assert daughter.json()["person_name"] == "his daughter"
    cleared = client.patch(f"/api/todos/{sibling['id']}", json={"person_name": None})
    assert cleared.json()["person_name"] is None
    paths = " ".join(client.app.openapi()["paths"])
    assert "auth" not in paths
    assert "login" not in paths
    assert "account" not in paths

    done = client.patch(f"/api/todos/{parent['id']}", json={"state": "done"})
    assert done.json()["state"] == "done"
    follow = make_todo(row["id"], title="Follow up", priority=4)
    another = make_todo(row["id"], title="Tights", priority=2, parent_id=parent["id"])
    assert follow["id"] != parent["id"]
    assert another["parent_id"] == parent["id"]

    client.delete(f"/api/todos/{parent['id']}")
    remaining = client.get(f"/api/lists/{row['id']}/todos").json()
    assert [item["id"] for item in remaining] == [sibling["id"], follow["id"]]
    assert client.get(f"/api/todos/{child['id']}").status_code == 404
    assert client.get(f"/api/todos/{another['id']}").status_code == 404

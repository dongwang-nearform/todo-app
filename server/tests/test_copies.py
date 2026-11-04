def test_matrix_copy(client, detail, make_list, make_todo):
    source = make_list("Template")
    dest = make_list("Saturday")
    parent = make_todo(
        source["id"],
        title="English drop-off",
        priority=5,
        position=1,
        at_time="09:00:00",
        alarm_at="08:30:00",
        person_name="his daughter",
        notes="gate",
    )
    make_todo(
        source["id"],
        title="English pickup",
        priority=4,
        position=2,
        parent_id=parent["id"],
        at_time="10:00:00",
    )
    make_todo(
        source["id"],
        title="Ballet pickup",
        priority=3,
        position=3,
        state="done",
        at_time="14:30:00",
    )
    extra = make_list("Extra")
    make_todo(extra["id"], title="Hidden", priority=1)
    hidden_copy = client.post(
        "/api/copies",
        json={"source_list_id": extra["id"], "destination_list_id": source["id"], "on_date": "2026-11-01"},
    )
    assert hidden_copy.status_code == 201
    assert hidden_copy.json()["todos"][0]["copy_confirmed"] is False

    before = client.get(f"/api/lists/{dest['id']}/todos").json()
    assert before == []

    copied = client.post(
        "/api/copies",
        json={"source_list_id": source["id"], "destination_list_id": dest["id"], "on_date": "2026-11-07"},
    )
    assert copied.status_code == 201
    payload = copied.json()
    rows = payload["todos"]
    by_title = {row["title"]: row for row in rows}
    assert [row["title"] for row in rows] == ["English drop-off", "English pickup", "Ballet pickup"]
    assert "Hidden" not in by_title
    assert by_title["English pickup"]["parent_id"] == by_title["English drop-off"]["id"]
    assert by_title["English drop-off"]["parent_id"] is None
    assert by_title["English drop-off"]["at_time"] == "09:00:00"
    assert by_title["English drop-off"]["alarm_at"] == "08:30:00"
    assert by_title["English drop-off"]["person_name"] == "his daughter"
    assert by_title["English drop-off"]["notes"] == "gate"
    assert by_title["English drop-off"]["priority"] == 5
    assert by_title["English drop-off"]["state"] == "not_done"
    assert by_title["Ballet pickup"]["state"] == "done"
    assert [row["position"] for row in rows] == [1, 2, 3]
    assert all(row["copy_confirmed"] is False for row in rows)
    assert all(row["copy_id"] == payload["id"] for row in rows)
    assert all(row["list_id"] == dest["id"] for row in rows)
    assert all(row["on_date"] == "2026-11-07" for row in rows)

    assert client.get(f"/api/lists/{dest['id']}/todos").json() == []
    assert client.get("/api/views/today", params={"on_date": "2026-11-07"}).json()["todos"] == []
    not_done_ids = {row["id"] for row in client.get("/api/views/not-done").json()}
    assert by_title["English drop-off"]["id"] not in not_done_ids
    period = client.get("/api/views/period", params={"grain": "day", "anchor": "2026-11-07"}).json()
    assert period["todos"] == []
    review = client.get(f"/api/copies/{payload['id']}")
    assert review.status_code == 200
    assert [row["title"] for row in review.json()["todos"]] == ["English drop-off", "English pickup", "Ballet pickup"]
    direct = client.get(f"/api/todos/{by_title['English drop-off']['id']}")
    assert direct.status_code == 200
    assert direct.json()["copy_confirmed"] is False

    confirmed = client.post(f"/api/copies/{payload['id']}/confirm")
    assert confirmed.status_code == 200
    assert all(row["copy_confirmed"] is True for row in confirmed.json()["todos"])
    assert [row["title"] for row in client.get(f"/api/lists/{dest['id']}/todos").json()] == [
        "English drop-off",
        "English pickup",
        "Ballet pickup",
    ]
    saturday = client.get("/api/views/today", params={"on_date": "2026-11-07"}).json()
    assert [row["title"] for row in saturday["todos"]] == ["English drop-off", "English pickup", "Ballet pickup"]
    later = client.get("/api/views/today", params={"on_date": "2026-11-14"}).json()
    assert later["todos"] == []

    again = client.post(f"/api/copies/{payload['id']}/confirm")
    assert again.status_code == 200
    assert len(again.json()["todos"]) == 3
    assert len(client.get(f"/api/lists/{dest['id']}/todos").json()) == 3

    count_before = len(client.get(f"/api/lists/{dest['id']}/todos").json())
    missing_source = client.post(
        "/api/copies",
        json={"source_list_id": 9999, "destination_list_id": dest["id"], "on_date": "2026-11-21"},
    )
    assert missing_source.status_code == 404
    detail(missing_source)
    missing_dest = client.post(
        "/api/copies",
        json={"source_list_id": source["id"], "destination_list_id": 9999, "on_date": "2026-11-21"},
    )
    assert missing_dest.status_code == 404
    detail(missing_dest)
    bad_date = client.post(
        "/api/copies",
        json={"source_list_id": source["id"], "destination_list_id": dest["id"], "on_date": "Saturday"},
    )
    assert bad_date.status_code == 422
    detail(bad_date)
    assert len(client.get(f"/api/lists/{dest['id']}/todos").json()) == count_before
    unknown = client.post("/api/copies/9999/confirm")
    assert unknown.status_code == 404
    detail(unknown)
    assert client.get("/api/copies/9999").status_code == 404

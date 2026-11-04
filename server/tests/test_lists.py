def test_matrix_lists_create_rename_and_empty_name(client, detail, make_list):
    empty = client.get("/api/lists")
    assert empty.status_code == 200
    assert empty.json() == []

    first = make_list("Errands")
    second = make_list("Saturday")
    listed = client.get("/api/lists")
    assert listed.status_code == 200
    assert [row["name"] for row in listed.json()] == ["Errands", "Saturday"]
    assert first["id"] != second["id"]

    renamed = client.patch(f"/api/lists/{first['id']}", json={"name": "Weekend"})
    assert renamed.status_code == 200
    assert renamed.json()["name"] == "Weekend"
    assert client.get("/api/lists").json()[0]["name"] == "Weekend"

    for payload in ({"name": ""}, {"name": "   "}, {}):
        rejected = client.post("/api/lists", json=payload)
        assert rejected.status_code == 422
        detail(rejected)
        rename = client.patch(f"/api/lists/{second['id']}", json=payload)
        assert rename.status_code == 422
        detail(rename)
    assert client.get(f"/api/lists").json()[1]["name"] == "Saturday"


def test_matrix_delete_list_removes_only_its_todos(client, detail, make_list, make_todo):
    first = make_list("Errands")
    second = make_list("Saturday")
    gone = make_todo(first["id"], title="Milk", priority=2)
    kept = make_todo(second["id"], title="Costco", priority=4)

    deleted = client.delete(f"/api/lists/{first['id']}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get("/api/lists").json() == [second]
    missing = client.get(f"/api/lists/{first['id']}/todos")
    assert missing.status_code == 404
    detail(missing)
    assert client.get(f"/api/lists/{second['id']}/todos").json()[0]["id"] == kept["id"]
    assert client.get(f"/api/todos/{gone['id']}").status_code == 404

    unknown = client.delete("/api/lists/9999")
    assert unknown.status_code == 404
    detail(unknown)
    unknown_rename = client.patch("/api/lists/9999", json={"name": "Nope"})
    assert unknown_rename.status_code == 404
    detail(unknown_rename)

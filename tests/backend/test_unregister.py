def test_unregister_removes_normalized_participant(client):
    client.post("/activities/Chess Club/signup?email=alice@mergington.edu")

    response = client.delete(
        "/activities/Chess Club/unregister?email=%20ALICE%40MERGINGTON.EDU%20"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered alice@mergington.edu from Chess Club"
    assert "alice@mergington.edu" not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown/unregister?email=alice@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_unregistered_participant(client):
    response = client.delete(
        "/activities/Chess Club/unregister?email=alice@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_unregister_rejects_empty_email(client):
    response = client.delete("/activities/Chess Club/unregister?email=")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"

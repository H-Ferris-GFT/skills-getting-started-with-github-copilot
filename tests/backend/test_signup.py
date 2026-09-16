def test_signup_adds_normalized_participant(client):
    response = client.post(
        "/activities/Chess Club/signup?email=%20ALICE%40MERGINGTON.EDU%20"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up alice@mergington.edu for Chess Club"
    assert "alice@mergington.edu" in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_duplicate_is_rejected(client):
    client.post("/activities/Chess Club/signup?email=alice@mergington.edu")

    response = client.post("/activities/Chess Club/signup?email=ALICE@MERGINGTON.EDU")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already registered for this activity"


def test_signup_rejects_unknown_activity(client):
    response = client.post("/activities/Unknown/signup?email=alice@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_empty_email(client):
    response = client.post("/activities/Chess Club/signup?email=")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email is required"


def test_signup_rejects_full_activity(client, activities):
    activity = activities["Chess Club"]
    activity["participants"] = [
        f"student{index}@mergington.edu"
        for index in range(activity["max_participants"])
    ]

    response = client.post("/activities/Chess Club/signup?email=new@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"

def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"] == (
        "Learn strategies and compete in chess tournaments"
    )
    assert "participants" in activities["Chess Club"]


def test_signup_adds_student_to_activity(client):
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post("/activities/Soccer Team/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Soccer Team"
    }
    assert email in client.get("/activities").json()["Soccer Team"]["participants"]


def test_signup_rejects_unknown_activity(client):
    # Arrange

    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_student(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up"}


def test_unregister_removes_student_from_activity(client):
    # Arrange
    email = "student@mergington.edu"
    client.post("/activities/Soccer Team/signup", params={"email": email})

    # Act
    response = client.delete(
        "/activities/Soccer Team/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered student@mergington.edu from Soccer Team"
    }
    assert email not in client.get("/activities").json()["Soccer Team"]["participants"]


def test_unregister_rejects_unknown_activity(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_student_not_signed_up(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Soccer Team/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up"}

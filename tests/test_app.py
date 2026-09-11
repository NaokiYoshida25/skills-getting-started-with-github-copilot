def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test retrieving all extracurricular activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9


def test_signup_success(client):
    """Test successfully signing up for an activity."""
    new_email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": new_email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for Chess Club"

    # Verify participant was added
    activities_resp = client.get("/activities")
    chess_participants = activities_resp.json()["Chess Club"]["participants"]
    assert new_email in chess_participants


def test_signup_activity_not_found(client):
    """Test signing up for a non-existent activity."""
    response = client.post("/activities/NonExistent/signup", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered(client):
    """Test signing up an email that is already registered."""
    existing_email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": existing_email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_success(client):
    """Test successfully unregistering a participant from an activity."""
    existing_email = "michael@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": existing_email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {existing_email} from Chess Club"

    # Verify participant was removed
    activities_resp = client.get("/activities")
    chess_participants = activities_resp.json()["Chess Club"]["participants"]
    assert existing_email not in chess_participants


def test_unregister_activity_not_found(client):
    """Test unregistering from a non-existent activity."""
    response = client.delete("/activities/NonExistent/participants", params={"email": "student@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found(client):
    """Test unregistering a student who is not registered in the activity."""
    non_participant = "notregistered@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": non_participant})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

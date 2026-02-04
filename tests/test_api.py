import json

def test_health_check(client):
    """Test the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("status") == "healthy"

def test_api_v1_info(client):
    """Test the API versioning info endpoint."""
    response = client.get("/api/v1")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("version") == "1.0.0"
    assert "auth" in data.get("endpoints")

def test_user_registration_success(client):
    """Test successful user registration."""
    payload = {
        "email": "test_user@example.com",
        "password": "SecurePass123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "registered successfully" in data.get("message").lower()
    assert data["user"]["email"] == "test_user@example.com"

def test_user_registration_missing_fields(client):
    """Test registration failure with missing fields."""
    payload = {
        "email": "incomplete@example.com"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "required" in data.get("error").lower()

def test_user_registration_duplicate_email(client):
    """Test registration failure with existing email."""
    payload = {
        "email": "duplicate@example.com",
        "password": "SecurePass123!"
    }
    # First registration
    client.post("/api/v1/auth/register", json=payload)
    # Second registration with same email
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "already registered" in data.get("error").lower()

def test_user_login_success(client):
    """Test successful login and JWT generation."""
    # Register first
    payload = {
        "email": "login_test@example.com",
        "password": "SecurePass123!"
    }
    client.post("/api/v1/auth/register", json=payload)
    
    # Attempt login
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
    assert data["user"]["email"] == "login_test@example.com"

def test_user_login_invalid_credentials(client):
    """Test login failure with wrong password."""
    # Register first
    payload = {
        "email": "wrong_pass@example.com",
        "password": "CorrectPass123!"
    }
    client.post("/api/v1/auth/register", json=payload)
    
    # Attempt login with wrong password
    login_payload = {
        "email": "wrong_pass@example.com",
        "password": "WrongPass123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    data = response.get_json()
    assert "invalid" in data.get("error").lower()
    
def test_task_crud_lifecycle(client):
    """Test full lifecycle of a task: Create, Read, Update, Delete."""
    # 1. Login to get token
    payload = {"email": "task_tester@example.com", "password": "TaskPass123!"}
    client.post("/api/v1/auth/register", json=payload)
    login_resp = client.post("/api/v1/auth/login", json=payload)
    token = login_resp.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Task
    task_payload = {"title": "Test Task", "description": "This is a test"}
    create_resp = client.post("/api/v1/tasks", json=task_payload, headers=headers)
    assert create_resp.status_code == 201
    task_id = create_resp.get_json()["task"]["id"]

    # 3. List Tasks
    list_resp = client.get("/api/v1/tasks", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.get_json()["tasks"]) >= 1

    # 4. Update Task
    update_payload = {"status": "completed"}
    update_resp = client.put(f"/api/v1/tasks/{task_id}", json=update_payload, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.get_json()["task"]["status"] == "completed"

    # 5. Delete Task
    delete_resp = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_resp.status_code == 200

    # 6. Verify Deletion
    get_resp = client.get(f"/api/v1/tasks/{task_id}", headers=headers)
    assert get_resp.status_code == 404

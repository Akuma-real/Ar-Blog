import pytest
import requests

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_register_and_login():
    # 1. 注册测试
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/register", json=register_data)
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == register_data["username"]
    assert user_data["email"] == register_data["email"]
    
    # 2. 登录测试
    login_data = {
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(
        f"{BASE_URL}/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # 3. 测试token
    token = token_data["access_token"]
    response = requests.post(
        f"{BASE_URL}/test-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == register_data["username"]

if __name__ == "__main__":
    pytest.main([__file__])

"""This tests the dashboard page"""

def test_dashboard(client):
    response = client.get("/dashboard")
    assert response.status_code == 302
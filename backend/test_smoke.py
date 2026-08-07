"""Simple smoke test for the GraphHire AI Flask application."""

from backend.app import app
from backend.seed import _build_seed_data


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["service"] == "GraphHire AI"


def test_dashboard_endpoint():
    client = app.test_client()
    response = client.get("/dashboard")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["data"]["top_skills"]
    assert payload["data"]["top_companies"]


def test_developers_endpoint_returns_demo_data_when_graph_is_unavailable():
    client = app.test_client()
    response = client.get("/developers")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] > 0
    assert payload["data"]


def test_seed_dataset_contains_exactly_twenty_indian_developers():
    seed_data = _build_seed_data()
    developers = seed_data["developers"]

    expected_names = {
        "Apeksha Vishwasrao",
        "Aarav Mehta",
        "Ananya Gupta",
        "Aditya Joshi",
        "Priya Patil",
        "Rahul Sharma",
        "Sneha Kulkarni",
        "Rohan Deshmukh",
        "Isha Nair",
        "Arjun Reddy",
        "Riya Shah",
        "Kunal Verma",
        "Neha Singh",
        "Amit Singh",
        "Kavya Iyer",
        "Siddharth Joshi",
        "Anjali Joshi",
        "Aman Agarwal",
        "Sanjay Malhotra",
        "Shreya Gupta",
    }

    assert len(developers) == 20
    assert {developer["full_name"] for developer in developers} == expected_names
    assert all(developer["country"] == "India" for developer in developers)
    assert all(developer["city"] in {"Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi", "Chennai", "Kolkata", "Ahmedabad", "Noida", "Gurugram"} for developer in developers)
    assert all(developer["current_company"] for developer in developers)

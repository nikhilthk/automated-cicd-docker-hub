from app import app, format_uptime

client = app.test_client()


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Pipeline Tracker" in response.data


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_info_has_expected_keys():
    data = client.get("/api/info").get_json()
    for key in ("version", "commit", "built_at", "hostname", "python", "uptime"):
        assert key in data


def test_format_uptime():
    assert format_uptime(3725) == "1h 2m 5s"
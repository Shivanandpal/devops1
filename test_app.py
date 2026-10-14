import pytest

from app import app, calculate_result


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_calculate_result_pass():
    result = calculate_result({
        "python": 78,
        "mathematics": 82,
        "devops": 91,
    })

    assert result["total"] == 251
    assert result["percentage"] == pytest.approx(83.67, abs=0.01)
    assert result["status"] == "PASS"


def test_calculate_result_fail_if_any_subject_below_pass_mark():
    result = calculate_result({
        "python": 28,
        "mathematics": 45,
        "devops": 32,
    })

    assert result["total"] == 105
    assert result["status"] == "FAIL"


def test_result_endpoint_returns_student_result(client):
    response = client.get("/results/101")

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Aarav Shah"
    assert data["total"] == 251
    assert data["status"] == "PASS"


def test_unknown_roll_number_returns_404(client):
    response = client.get("/results/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Student roll number not found"


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}

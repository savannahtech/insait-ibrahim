import os
from unittest.mock import patch

import pytest

from insait.app import create_app
from insait.database import db
from insait.models import Question

TEST_DB = os.path.join(os.path.dirname(__file__), "test.db")


@pytest.fixture
def app():

    os.environ["DATABASE_URL"] = "sqlite:///:memory:"

    app = create_app()

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@patch("insait.services.OpenAIUtility.get_answer")
def test_post_question(mock_open_ai, client):

    mock_open_ai.return_value = "Mocked answer"

    response = client.post("/ask", json={"question": "What is Flask?"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert "created_at" in data
    assert "question" in data
    assert "answer" in data
    assert data["question"] == "What is Flask?"
    assert data["answer"] == "Mocked answer"

    # Verify that the question was saved in the database
    question_in_db = Question.query.filter_by(id=data["id"]).first()
    assert question_in_db is not None
    assert question_in_db.question == "What is Flask?"
    assert question_in_db.answer == "Mocked answer"


@patch("insait.services.OpenAIUtility.get_answer")
def test_openai_method_was_called(mock_open_ai, client):

    mock_open_ai.return_value = "Mocked answer"

    response = client.post("/ask", json={"question": "What is Flask?"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert "created_at" in data
    assert "question" in data
    assert "answer" in data
    assert data["question"] == "What is Flask?"
    assert data["answer"] == "Mocked answer"

    # Verify that the question was saved in the database
    question_in_db = Question.query.filter_by(id=data["id"]).first()
    assert question_in_db is not None
    assert question_in_db.question == "What is Flask?"
    assert question_in_db.answer == "Mocked answer"

    # Assert that OpenAIUtility get_answer was called with correct parameters
    mock_open_ai.assert_called_once_with(question="What is Flask?")


def test_post_question_invalid(client):
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 400

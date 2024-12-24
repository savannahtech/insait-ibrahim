import os

from asgiref.wsgi import WsgiToAsgi
from flask import Flask, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest

import insait.services as services
from insait.database import init_db
from insait.schemas import QuestionRequest


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app)

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        response = jsonify(
            {
                "error": "Bad Request",
                "message": error.description,  # or you can customize the error message here
            }
        )
        response.status_code = 400
        return response

    @app.route("/ask", methods=["POST"])
    def ask_question():
        """The endpoint takes a question and returns an answer."""

        try:
            request_data = request.get_json()
            validated_request = QuestionRequest(**request_data)
        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

        question = validated_request.question

        response = services.get_answer(question=question)

        return jsonify(response), 201

    return app


flask_app = create_app()
asgi_app = WsgiToAsgi(flask_app)


if __name__ == "__main__":
    flask_app.run(debug=True)

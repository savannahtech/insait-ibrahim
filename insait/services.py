from typing import Any, Dict

from insait.database import db
from insait.models import Question
from insait.schemas import QuestionResponse
from insait.util_classes import OpenAIUtility

openai = OpenAIUtility()


def get_answer(question: str) -> Dict[str, Any]:
    """Get an answer to the question from OpenAI."""

    answer = openai.get_answer(question=question)

    question = Question(question=question, answer=answer)
    db.session.add(question)
    db.session.commit()
    db.session.refresh(question)

    response_data = QuestionResponse(
        id=question.id,
        question=question.question,
        answer=question.answer,
        created_at=question.created_at.isoformat(),
    )

    return response_data.model_dump()

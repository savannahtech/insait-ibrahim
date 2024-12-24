from datetime import datetime

from pydantic import BaseModel, constr


class QuestionRequest(BaseModel):
    question: constr(min_length=5, max_length=1024)


# Define a Pydantic model for the response
class QuestionResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime

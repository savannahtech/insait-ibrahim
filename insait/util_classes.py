import logging
import os

from openai import OpenAI
from werkzeug.exceptions import BadRequest, InternalServerError

logger = logging.getLogger(__name__)


class OpenAIUtility:
    """OpenAI API utilities."""

    def __init__(self):

        api_key = os.environ.get("OPENAI_API_KEY")

        self.client = OpenAI(api_key=api_key)

    def get_answer(self, question: str) -> str:
        """Get an answer to the question from OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": question}]
            )
            return response.choices[0].message.content

        except Exception as e:
            logger.error("Error from OpenAI: %s", e)
            # pylint: disable=raise-missing-from
            raise InternalServerError(
                description="Error when generating answer to the question"
            )

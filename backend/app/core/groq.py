from backend.app.errors.exceptions import PeakFitError
from backend.app.core.groq import AsyncGroq
from groq.types.chat import ChatCompletionMessageParam
from fastapi import status

class GroqClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.client: AsyncGroq = AsyncGroq(api_key=api_key)
        self.model: str = model

    async def chat_completion(self, user_message: ChatCompletionMessageParam, system_message: ChatCompletionMessageParam) -> str:
        try:
            chat_completion = await self.client.chat.completions.create(
                messages=[user_message, system_message],
                model=self.model
            )

            return str(chat_completion.choices[0].message.content)
        except:
            raise PeakFitError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Error al conectar con la ia."
            )

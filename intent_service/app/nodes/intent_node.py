from app.clients.intent_client import IntentClient
from app.core.schemas import IntentResult


async def run(message: str) -> IntentResult:
    """Predict intent by calling the fine-tuned model server."""
    client = IntentClient()
    return await client.predict(message)

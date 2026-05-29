from app.clients.grpc_intent_client import GrpcIntentClient
from app.core.schemas import IntentResult


async def run(message: str) -> IntentResult:
    client = GrpcIntentClient()
    return await client.predict(message)

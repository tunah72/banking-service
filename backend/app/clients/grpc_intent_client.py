"""gRPC client for the Intent Service."""

import grpc
from grpc import aio

from app.clients.intent_grpc import intent_service_pb2
from app.clients.intent_grpc import intent_service_pb2_grpc
from app.core.schemas import IntentResult
from app.core.settings import get_settings


class GrpcIntentClient:
    """Calls the Intent Service via gRPC to predict customer intent."""

    def __init__(self) -> None:
        settings = get_settings()
        self._target = f"{settings.intent_service_host}:{settings.intent_service_port}"

    async def predict(self, text: str) -> IntentResult:
        async with aio.insecure_channel(self._target) as channel:
            stub = intent_service_pb2_grpc.IntentServiceStub(channel)
            request = intent_service_pb2.IntentRequest(message=text)
            response = await stub.IntentRecognizer(request, timeout=30.0)
            return IntentResult(
                intent=response.intent,
                confidence=response.confidence,
                reason=response.reason,
                top_k=[],
            )

"""gRPC server for Intent Classification Service."""

import asyncio
import logging
import sys
import os

import grpc
from grpc import aio

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

import intent_service_pb2
import intent_service_pb2_grpc
from app.nodes.intent_node import run as predict_intent
from app.core.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


class IntentServiceServicer(intent_service_pb2_grpc.IntentServiceServicer):
    """Implements the IntentService gRPC interface."""

    async def IntentRecognizer(self, request, context):
        message = request.message
        logger.info("Received intent request: %s", message[:80])

        try:
            result = await predict_intent(message)
            logger.info(
                "Predicted intent='%s' confidence=%.2f",
                result.intent,
                result.confidence,
            )
            return intent_service_pb2.IntentResponse(
                intent=result.intent,
                confidence=result.confidence,
                reason=result.reason,
            )
        except Exception as e:
            logger.error("Intent prediction failed: %s", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Intent prediction failed: {e}")
            return intent_service_pb2.IntentResponse()


async def serve():
    settings = get_settings()
    port = settings.grpc_port
    server = aio.server()
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(
        IntentServiceServicer(), server
    )
    listen_addr = f"[::]:{port}"
    server.add_insecure_port(listen_addr)

    logger.info("Starting Intent Service gRPC server on %s", listen_addr)
    logger.info("Intent API URL: %s", settings.intent_api_url)

    await server.start()
    logger.info("Server started successfully.")

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await server.stop(5)


if __name__ == "__main__":
    asyncio.run(serve())

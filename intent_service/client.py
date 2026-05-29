"""gRPC client for testing the Intent Service."""

import asyncio
import sys

from grpc import aio

import intent_service_pb2
import intent_service_pb2_grpc


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <message> [host:port]")
        print('Example: python client.py "My card was stolen"')
        sys.exit(1)

    message = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "localhost:50051"

    async with aio.insecure_channel(target) as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        request = intent_service_pb2.IntentRequest(message=message)

        print(f"Sending to {target}: {message!r}")
        response = await stub.IntentRecognizer(request)

        print(f"Intent:     {response.intent}")
        print(f"Confidence: {response.confidence:.4f}")
        print(f"Reason:     {response.reason}")


if __name__ == "__main__":
    asyncio.run(main())

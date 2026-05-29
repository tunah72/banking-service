import httpx
from app.core.schemas import IntentResult
from app.core.settings import get_settings


class IntentClient:
    """HTTP client that calls the fine-tuned intent model server (on Colab)."""

    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.intent_api_url.rstrip("/")

    async def predict(self, text: str) -> IntentResult:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self._base_url}/predict", json={"text": text}
            )
            response.raise_for_status()
            data = response.json()
            top_k = data.get("top_k", [])
            intent = data.get("intent", "unknown")
            confidence = data.get("confidence", 0.0)
            reason = (
                f"Fine-tuned model predicted '{intent}' "
                f"with {confidence:.0%} confidence."
            )
            return IntentResult(
                intent=intent,
                confidence=confidence,
                reason=reason,
                top_k=top_k,
            )

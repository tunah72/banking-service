import json
import os
from typing import Generator

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Banking AI Agent", layout="wide")
st.title("Banking AI Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "trace" not in st.session_state:
    st.session_state.trace = None


def _stream_chunks(user_input: str, history: list[dict]) -> Generator[str, None, None]:
    payload = {"message": user_input, "history": history}
    with httpx.Client(timeout=120.0) as client:
        with client.stream("POST", f"{API_URL}/chat/stream", json=payload) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line.startswith("data: "):
                    continue
                event = json.loads(line[6:])
                if event["type"] == "chunk":
                    yield event["text"]
                elif event["type"] == "done":
                    st.session_state.trace = event["trace"]
                    st.session_state.pending_action = event["action"]


col_chat, col_trace = st.columns([3, 2])

with col_chat:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Describe your banking issue..."):
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            try:
                full_response = st.write_stream(_stream_chunks(user_input, history))
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
            except httpx.HTTPStatusError as e:
                st.error(f"API error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

        st.rerun()

with col_trace:
    st.subheader("Pipeline Trace")
    trace = st.session_state.trace

    if trace is None:
        st.info("Send a message to see the pipeline trace.")
    else:
        intent = trace.get("intent", {})
        priority = trace.get("priority", {})
        routing = trace.get("routing", {})

        st.markdown("**Intent Detection**")
        st.write(f"Intent: `{intent.get('intent', '-')}`")
        confidence = intent.get("confidence", 0)
        st.progress(confidence, text=f"Confidence: {confidence:.0%}")

        reason = intent.get("reason", "")
        if reason:
            st.caption(reason)

        with st.expander("Top-5 intents"):
            top_k = intent.get("top_k", [])
            if top_k:
                for item in top_k:
                    st.write(f"`{item['intent']}` — {item['score']:.0%}")
            else:
                st.write("N/A (gRPC response)")

        st.divider()

        st.markdown("**Priority**")
        level = priority.get("level", "-")
        color = {"high": ":red[high]", "medium": ":orange[medium]", "low": ":green[low]"}.get(
            level, level
        )
        st.markdown(f"Level: {color}")
        if priority.get("reason"):
            st.caption(priority["reason"])

        st.divider()

        st.markdown("**Routing Decision**")
        action = routing.get("action", "-")
        st.write(f"Action: `{action}`")
        if routing.get("reason"):
            st.caption(routing["reason"])

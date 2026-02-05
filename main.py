from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import logic  # Import the logic we wrote above

app = FastAPI()

# Database to store conversation state in memory
# Structure: { "session_id": [ {role: "user", content: "..."} ] }
conversations_db = {}

# Updated Schema with Default Values
class ScammerMessage(BaseModel):
    # We add defaults (= "...") so the API never complains about missing fields
    session_id: str = "test_session_123"
    message: str = "Hello, this is a test message."
    timestamp: str = "2026-01-01T12:00:00Z"

# Output Schema
class AgentResponse(BaseModel):
    session_id: str
    scam_detected: bool
    agent_message: Optional[str] = None
    extracted_intelligence: dict
    engagement_metrics: dict

# The Main Endpoint
@app.post("/webhook", response_model=AgentResponse)
async def webhook(data: ScammerMessage, x_api_key: str = Header(None)):
    
    # 1. Security Check
    MY_SECRET_KEY = "agentic-honeypot-abhijeet"
    if x_api_key != MY_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Load History
    session_id = data.session_id
    if session_id not in conversations_db:
        conversations_db[session_id] = []
    
    history = conversations_db[session_id]
    history.append({"role": "user", "content": data.message})

    # 3. Detect Scam
    is_scam = logic.detect_scam(data.message)

    agent_reply = None
    intelligence = {}

    # 4. Agent Handoff (If scam detected)
    if is_scam or len(history) > 1:
        # Generate Persona Response
        agent_reply = logic.generate_agent_response(history)
        history.append({"role": "assistant", "content": agent_reply})
        
        # Extract Intelligence
        intelligence = logic.extract_intelligence(history)

    # 5. Metrics
    metrics = {
        "turn_count": len(history),
        "engagement_status": "active" if agent_reply else "ignoring"
    }

    # 6. Save State & Return
    conversations_db[session_id] = history
    
    return {
        "session_id": session_id,
        "scam_detected": is_scam,
        "agent_message": agent_reply,
        "extracted_intelligence": intelligence,
        "engagement_metrics": metrics

    }

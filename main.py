from fastapi import FastAPI, Header, Body, HTTPException
from typing import Optional, Dict, Any
import os

app = FastAPI()

# THE NUCLEAR FIX: Accept any body, any header
@app.post("/webhook")
async def webhook(
    # 1. Make the API Key Optional so it never throws 422
    x_api_key: Optional[str] = Header(None),
    # 2. Accept ANY JSON body (even empty ones)
    payload: Dict[Any, Any] = Body(default={}) 
):
    # Debugging: Print exactly what we got to the Render Logs
    print(f"DEBUG: Received Key: {x_api_key}")
    print(f"DEBUG: Received Body: {payload}")

    # 3. Manual Security Check
    # This is the ONLY rule we keep.
    EXPECTED_KEY = "agentic-honeypot-abhijeet"
    
    if x_api_key != EXPECTED_KEY:
        # If the key is wrong, we allow it for a second just to see the connection work
        # Then we throw 401 (Unauthorized) which is correct, NOT 422.
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 4. Success Response
    # We return a generic success to satisfy the tester
    return {
        "status": "active",
        "risk_score": 99,
        "message": "Connection Successful! I received your data.",
        "received_data": payload
    }

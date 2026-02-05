import re
import os
from openai import OpenAI

# Initialize OpenAI (You need an API Key)
# Export your key in terminal: export OPENAI_API_KEY='sk-...'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# 1. SCAM DETECTOR
def detect_scam(message_text):
    """
    Analyzes the message to see if it is a scam.
    Returns: True if scam, False otherwise.
    """
    # Simple keyword detection for speed (can be upgraded to AI)
    keywords = ["lottery", "winner", "bank details", "urgent", "verify", "upi", "pay", "investment"]
    if any(word in message_text.lower() for word in keywords):
        return True
    
    # Optional: Use AI for deeper detection
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a security analyst. Reply only 'YES' if this is a scam, 'NO' if not."},
                {"role": "user", "content": f"Analyze this message: {message_text}"}
            ]
        )
        return "YES" in response.choices[0].message.content.upper()
    except:
        return False

# 2. INTELLIGENCE EXTRACTOR
def extract_intelligence(conversation_history):
    """
    Scans text for sensitive data like UPI IDs, Bank Accounts, and URLs.
    """
    text = " ".join([msg['content'] for msg in conversation_history])
    
    # Regex Patterns
    upi_pattern = r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}'
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    bank_pattern = r'\b\d{9,18}\b'  # Generic 9-18 digit number detection

    return {
        "upi_ids": re.findall(upi_pattern, text),
        "urls": re.findall(url_pattern, text),
        "bank_accounts": re.findall(bank_pattern, text)
    }

# 3. AUTONOMOUS AGENT (THE HONEY-POT)
def generate_agent_response(history):
    """
    Generates a response as a 'naïve victim' to keep the scammer talking.
    """
    system_prompt = """
    You are an elderly person named 'Grandma Edna'. You are not tech-savvy.
    You are very polite but confused. You engage the scammer because you are lonely.
    GOAL: Keep them talking. Ask for clarification. Pretend to try to pay but 'fail'.
    NEVER admit you know it is a scam.
    """
    
    messages = [{"role": "system", "content": system_prompt}] + history
    
    response = client.chat.completions.create(
        model="gpt-4o", # Or gpt-3.5-turbo
        messages=messages
    )
    return response.choices[0].message.content
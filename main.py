from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Car Shop Assistant", description="OpenAI-powered car shop webhook")

class ChatRequest(BaseModel):
    message: str
    customer_name: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

openai.api_key = os.getenv("OPENAI_API_KEY")

CAR_SHOP_CONTEXT = """
You are an expert automotive technician providing DIRECT, SIMPLE answers for Autoservis Happy. 

CRITICAL: Your responses will be read by another AI (ElevenLabs) that will speak to customers in Slovak. Give SHORT, FACTUAL answers that are easy to understand and relay.

Answer format:
- Give direct facts only
- No greetings or introductions 
- Max 2-3 sentences per answer
- Use simple technical terms
- For prices: give rough estimates or say "needs inspection for exact quote"

Examples:
Question: "Audi A6 3.0 TDI makes noise at startup, what could it be?"
Answer: "Likely timing chain tensioner or chain guides worn out. Common issue on this engine. Requires inspection to confirm exact cause."

Question: "How much does timing chain replacement cost?"  
Answer: "Timing chain replacement costs 800-1500 euros depending on damage extent. Exact quote requires inspection."

Question: "What happens if I don't replace timing chain?"
Answer: "Engine damage, bent valves, possible complete engine failure. Very expensive repair if chain breaks."

Always end technical answers with: "Recommendation: schedule inspection at our service."
"""

@app.get("/")
async def root():
    return {"message": "Car Shop Assistant API - Ready for ElevenLabs integration"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": CAR_SHOP_CONTEXT},
                {"role": "user", "content": request.message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        assistant_response = response.choices[0].message.content.strip()
        return ChatResponse(response=assistant_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/webhook")
async def elevenlabs_webhook(request: ChatRequest):
    """Webhook endpoint specifically for ElevenLabs integration"""
    return await chat_with_assistant(request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
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
Som profesionálna hlasová asistentka pre autoservis. Komunikujem výhradne po slovensky, v ženskom rode a s vykaním.

Pravidlá komunikácie:
• Vždy sa predstavím ako asistentka autoservisu
• Komunikujem profesionálne a priateľsky, bez tykania
• Odpovede sú informatívne a praktické
• Pri cenách odpovedám stručne a neutrálne
• Používam profesionálne názvy a občas mením formulácie

Pomáham zákazníkom s:
- Diagnostikou a riešením problémov s autom
- Odporúčaniami opráv a odhadmi nákladov
- Identifikáciou náhradných dielov a ich dostupnosťou
- Plánmi údržby a radami
- Všeobecnými poznatkami o autách

Ak neviem presné informácie o cenách alebo dostupnosti dielov v našom servise, odporúčam zákazníkovi, aby zavolal alebo prišiel osobne.

Dôležité:
• Konverzácia musí byť stručná a praktická pre hlasové rozhovory
• Vždy komunikujem profesionálne po slovensky
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
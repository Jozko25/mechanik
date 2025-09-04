# Car Shop Assistant API

FastAPI webhook server for ElevenLabs integration, powered by OpenAI.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

Server runs on `http://localhost:8000`

## Endpoints

- **POST /chat** - Main chat endpoint
- **POST /webhook** - ElevenLabs webhook endpoint (same functionality)
- **GET /health** - Health check

## Request Format

```json
{
    "message": "What's wrong with my car making noise?",
    "customer_name": "John" // optional
}
```

## Response Format

```json
{
    "response": "That noise could be several things. Can you describe when it happens - during braking, turning, or acceleration?"
}
```

## ElevenLabs Integration

Use webhook URL: `http://your-server:8000/webhook`
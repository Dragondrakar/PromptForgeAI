from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from uuid import uuid4

from models import OptimizeRequest, ScrapeRequest, Prompt
from database import load_json, save_json, deduct_tokens

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI(title="PromptForge AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_SECRET = os.getenv("API_SECRET_KEY", "dev-key")

@app.post("/optimize")
async def optimize(req: OptimizeRequest, authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {API_SECRET}":
        raise HTTPException(401, "Invalid token")
    
    if not deduct_tokens(15):
        raise HTTPException(429, "Token limit reached")

    prompt = f"""You are Prompt Genie. Turn this into a perfect super-prompt:
    Style: {req.style}
    Original: {req.input}
    Return ONLY the full optimized prompt."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    optimized = response.choices[0].message.content.strip()

    vault = load_json("prompts.json")
    new_prompt = Prompt(
        id=str(uuid4()),
        title=req.input[:50],
        original=req.input,
        optimized=optimized,
        tags=["auto"],
        created=datetime.utcnow().isoformat(),
    )
    vault["prompts"].append(new_prompt.model_dump())
    save_json(vault, "prompts.json")

    return {"optimized": optimized, "tokens_used": 15, "id": new_prompt.id}

@app.post("/scrape")
async def scrape(req: ScrapeRequest, authorization: str = Header(None)):
    if not authorization or authorization != f"Bearer {API_SECRET}":
        raise HTTPException(401, "Invalid token")
    
    if not deduct_tokens(30):
        raise HTTPException(429, "Token limit reached")

    async with httpx.AsyncClient() as http:
        html = (await http.get(req.url, timeout=10)).text

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)[:8000]  # limit for cost

    llm_prompt = f"""Extract structured data from this webpage text.
    Query: {req.query}
    Return ONLY valid JSON with the requested fields.

    Page text:
    {text}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": llm_prompt}],
        temperature=0.0,
        response_format={"type": "json_object"}
    )
    data = response.choices[0].message.content

    return {"data": json.loads(data), "tokens_used": 30}
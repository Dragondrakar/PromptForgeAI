# PromptForge API v1.1

# PromptForge API v1.1 (FastAPI)

Base: http://localhost:8000

**Headers required:**
Authorization: Bearer super-secret-dev-key-change-in-production

POST /optimize
POST /scrape

All responses include tokens_used. Data saved automatically to data-examples/*.json

Base URL: https://api.promptforge.ai/v1

All calls require header: Authorization: Bearer YOUR_USER_TOKEN

Endpoints:
POST /optimize
POST /scrape
GET /vault
POST /vault/save

Token usage is automatically deducted and logged in your JSON vault.
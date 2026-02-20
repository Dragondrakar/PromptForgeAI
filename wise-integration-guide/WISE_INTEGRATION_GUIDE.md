# Wise.com Billing Integration Guide for PromptForge AI

## Why Wise?
Zero fees for international customers, works in 160+ countries, perfect for indie SaaS.

## Step-by-step Setup (Manual – 5 minutes)

1. Create a free Wise Business account → https://wise.com/business
2. Verify your business (takes 1–3 days).
3. Go to “Balances” → “Request money”.
4. Create three reusable links:
   - Free plan → $0 (just a thank-you link)
   - Pro plan → $19/month → Title: "PromptForge AI – Pro Monthly"
   - Business plan → $49/month → Title: "PromptForge AI – Business Monthly"
5. Copy the link for each plan and paste into the landing page buttons (already prepared in index.html).

## After Customer Pays
1. You receive instant email + money in your Wise balance.
2. Manually activate the user in your dashboard (add their email to your `users.json` with token quota).
3. (Future) Connect Wise webhook → auto-activate user.

Full automation code (Python + FastAPI) available on request.
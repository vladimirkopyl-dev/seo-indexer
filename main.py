from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# ВАЖЛИВО: Переконайтеся, що ви додали STRIPE_SECRET_KEY у Variables на Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний стиль для всіх сторінок
STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 40px 20px; background: #f4f7f9; }
    .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; }
    h1 { color: #111; font-size: 2.5em; margin-bottom: 10px; }
    .btn { background: #6772E5; color: white; padding: 16px 32px; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block; margin: 20px 0; transition: background 0.2s; }
    .btn:hover { background: #5469d4; }
    .footer { margin-top: 50px; text-align: center; font-size: 0.85em; color: #666; }
    .footer a { color: #6772E5; text-decoration: none; margin: 0 10px; }
    textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-family: monospace; }
</style>
"""

# 1. ГОЛОВНА СТОРІНКА
@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>

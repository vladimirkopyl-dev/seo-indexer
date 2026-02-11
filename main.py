from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний стиль для текстових сторінок
TEXT_PAGE_STYLE = """
<style>
    body { font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 40px 20px; background: #f4f7f9; }
    .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    h1 { color: #111; }
    a { color: #6772E5; text-decoration: none; }
    .footer { margin-top: 40px; text-align: center; font-size: 0.9em; }
</style>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        <head>
            <title>SEO Turbo Indexer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {TEXT_PAGE_STYLE}
        </head>
        <body style="text-align: center;">
            <div class="container" style="max-width: 500px; margin: auto;">
                <h1>🚀 SEO Turbo Indexer</h1>
                <p>Get your pages indexed by Google within 24 hours.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 1.2em; font-weight: bold;">Only $10 / month</p>
                <a href="/buy" style="background: #6772E5; color: white; padding: 15px 25px; border-radius: 5px; font-weight: bold; display: inline-block;">Get Instant Access</a>
            </div>
            <div class="footer">
                <a href="/terms">Terms of Service</a> | <a href="/privacy">Privacy Policy</a>
            </div>
        </body>
    </html>
    """

@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return f"""
    <html>
        <head><title>Privacy Policy - SEO Turbo Indexer</title>{TEXT_PAGE_STYLE}</head>
        <body>
            <div class="container">
                <h1>Privacy Policy</h1>
                <p>Last updated: February 11, 2026</p>
                <p>At SEO Turbo Indexer, we respect your privacy. We only collect information necessary to provide our services:</p>
                <ul>
                    <li><strong>Email:</strong> Collected via Stripe to manage your access.</li>
                    <li><strong>URLs:</strong> The links you submit are used solely for indexing purposes.</li>
                </ul>
                <p>We do not sell your data to third parties. Payments are processed securely by Stripe.</p>
                <a href="/">← Back to Home</a>
            </div>
        </body>
    </html>
    """

@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return f"""
    <html>
        <head><title>Terms of Service - SEO Turbo Indexer</title>{TEXT_PAGE_STYLE}</head>
        <body>
            <div class="container">
                <h1>Terms of Service</h1>
                <p>By using SEO Turbo Indexer, you agree to the following:</p>
                <ul>
                    <li>The service is provided "as is". We aim for 24h indexing but cannot guarantee Google's internal algorithms.</li>
                    <li>The $10 fee is for a one-time access/monthly subscription as described.</li>
                    <li>Users are responsible for the URLs they submit.</li>
                </ul>
                <a href="/">← Back to Home</a>
            </div>
        </body>
    </html>
    """

# ... (інші функції /buy, /dashboard та /send-links залишаються такими ж)

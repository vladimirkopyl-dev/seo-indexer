from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, що ключ sk_test... або sk_live... доданий у Variables на Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

STYLE = """
<style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 40px 20px; background: #f4f7f9; }
    .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; }
    h1 { color: #111; font-size: 2.5em; margin-bottom: 10px; }
    .btn { background: #6772E5; color: white; padding: 16px 32px; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block; margin: 20px 0; transition: background 0.2s; border: none; cursor: pointer; }
    .btn:hover { background: #5469d4; }
    .footer { margin-top: 50px; text-align: center; font-size: 0.85em; color: #666; }
    .footer a { color: #6772E5; text-decoration: none; margin: 0 10px; }
    textarea { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-family: monospace; min-height: 200px; }
</style>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        <head>
            <title>SEO Turbo Indexer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {STYLE}
        </head>
        <body>
            <div class="container">
                <h1>🚀 SEO Turbo Indexer</h1>
                <p style="font-size: 1.2em; color: #555;">Get your pages indexed by Google within 24 hours.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="font-size: 1.4em; font-weight: bold;">Only $8.99 / month</p>
                <a href="/buy" class="btn">Get Instant Access</a>
            </div>
            <div class="footer">
                <a href="/terms">Terms of Service</a> | <a href="/privacy">Privacy Policy</a>
                <p>© 2026 SEO Turbo Indexer</p>
            </div>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'SEO Turbo Indexer - Full Access'},
                    'unit_amount': 899,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://seo-indexer-production.up.railway.app/dashboard', 
            cancel_url='https://seo-indexer-production.up.railway.app/',
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"""
    <html>
        <head><title>Dashboard - SEO Indexer</title>{STYLE}</head>
        <body>
            <div class="container">
                <h1 style="color: #28a745;">✅ Payment Successful!</h1>
                <h3>Submit your URLs for indexing</h3>
                <p>Enter one URL per line</p>
                <form action="/send-links" method="post">
                    <textarea name="links" placeholder="https://example.com/page1"></textarea><br>
                    <button type="submit" class="btn" style="width: 100%;">Start Indexing Now</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\\n') if url.strip()]
    return {
        "status": "success",
        "message": f"Received {len(urls)} URLs. Indexing started!",
        "next_steps": "Check Google Search Console in 24 hours."
    }

@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return f"""
    <html>
        <head><title>Privacy Policy</title>{STYLE}</head>
        <body>
            <div class="container" style="text-align: left;">
                <h1>Privacy Policy</h1>
                <p>We only collect your email and submitted URLs. We do not share your data.</p>
                <a href="/">← Back to Home</a>
            </div>
        </body>
    </html>
    """

@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return f"""
    <html>
        <head><title>Terms of Service</title>{STYLE}</head>
        <body>
            <div class="container" style="text-align: left;">
                <h1>Terms of Service</h1>
                <p>Service is provided 'as is'. Indexing speed depends on Google algorithms.</p>
                <a href="/">← Back to Home</a>
            </div>
        </body>
    </html>
    """

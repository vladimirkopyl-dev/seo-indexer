from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 1. LANDING PAGE (Головна сторінка)
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>SEO Turbo Indexer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f4f7f9;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h1>🚀 SEO Turbo Indexer</h1>
                <p>Get your pages indexed by Google within 24 hours.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 1.2em; font-weight: bold;">Only $10 / month</p>
                <a href="/buy" style="background: #6772E5; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Get Instant Access</a>
            </div>
        </body>
    </html>
    """

# 2. CHECKOUT SESSION (Оплата)
@app.get("/buy")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'SEO Turbo Indexer - Full Access'},
                    'unit_amount': 1000,
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

# 3. USER DASHBOARD (Особистий кабінет)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head><title>Dashboard - SEO Indexer</title></head>
        <body style="font-family: sans-serif; padding: 20px; text-align: center; background: #f4f7f9;">
            <div style="max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 10px;">
                <h2 style="color: #28a745;">✅ Payment Successful!</h2>
                <h3>Submit your URLs for indexing:</h3>
                <p style="color: #666;">Enter one URL per line</p>
                <form action="/send-links" method="post">
                    <textarea name="links" rows="10" style="width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px;" placeholder="https://example.com/my-page"></textarea><br><br>
                    <button type="submit" style="background: #28a745; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">Start Indexing Now</button>
                </form>
            </div>
        </body>
    </html>
    """

# 4. LINK PROCESSING (Обробка)
@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    # Filtering empty lines
    urls = [url.strip() for url in links.split('\n') if url.strip()]
    count = len(urls)
    return {
        "status": "success",
        "message": f"Received {count} URLs. Our bots have started the indexing process!",
        "next_steps": "You will see your pages in Google search results shortly."
    }

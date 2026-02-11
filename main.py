from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# 1. ГОЛОВНА СТОРІНКА
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>SEO Turbo Indexer</title><meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #f4f7f9;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h1>🚀 SEO Turbo Indexer</h1>
                <p>Ваші посилання будуть у Google за 24 години.</p>
                <a href="/buy" style="background: #6772E5; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Оплатити доступ за $10</a>
            </div>
        </body>
    </html>
    """

# 2. СТОРІНКА ОПЛАТИ
@app.get("/buy")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'SEO Indexer Access'}, 'unit_amount': 1000}, 'quantity': 1}],
            mode='payment',
            # ПІСЛЯ ОПЛАТИ КЛІЄНТ ПОТРАПИТЬ СЮДИ:
            success_url='https://seo-indexer-production.up.railway.app/dashboard', 
            cancel_url='https://seo-indexer-production.up.railway.app/',
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

# 3. РОБОЧА ПАНЕЛЬ (Dashboard) - Сюди потрапляють після оплати
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return """
    <html>
        <head><title>Dashboard - SEO Indexer</title></head>
        <body style="font-family: sans-serif; padding: 20px; text-align: center;">
            <h2>✅ Оплата успішна!</h2>
            <h3>Вставте посилання для індексації (кожне з нового рядка):</h3>
            <form action="/send-links" method="post">
                <textarea name="links" rows="10" style="width: 100%; max-width: 600px; padding: 10px;" placeholder="https://example.com/page1"></textarea><br><br>
                <button type="submit" style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">Запустити індексацію</button>
            </form>
        </body>
    </html>
    """

# 4. ОБРОБКА ПОСИЛАНЬ
@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    # Тут ми пізніше додамо код Google Indexing API
    # А поки що просто підтверджуємо отримання
    count = len(links.split('\n'))
    return {"message": f"Отримано {count} посилань. Ми почали їх обробку!"}

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Отримуємо секретний ключ зі змінних оточення Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/", response_class=HTMLResponse)
async def home():
    # Головна сторінка з кнопкою
    return """
    <html>
        <head>
            <title>SEO Turbo Indexer</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 100px; background-color: #f4f7f9;">
            <div style="max-width: 500px; margin: auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                <h1 style="color: #333;">🚀 SEO Turbo Indexer</h1>
                <p style="color: #666; font-size: 18px;">Пришвидшіть індексацію вашого сайту в Google за лічені години.</p>
                <div style="margin-top: 30px;">
                    <a href="/buy" style="background-color: #6772E5; color: white; padding: 18px 35px; text-decoration: none; border-radius: 5px; font-size: 20px; font-weight: bold; display: inline-block; transition: background 0.3s;">
                        Активувати за $10/міс
                    </a>
                </div>
                <p style="margin-top: 20px; font-size: 12px; color: #999;">Безпечна оплата через Stripe</p>
            </div>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout():
    # Створення сесії оплати
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'SEO Indexer Monthly Subscription'},
                    'unit_amount': 1000, # Сума в центах ($10.00)
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://google.com', # Повернення після успішної оплати
            cancel_url='https://google.com',  # Повернення при скасуванні
        )
        # Пряме перенаправлення на Stripe
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return {"error": str(e)}

@app.get("/status")
def check_status():
    return {"status": "online", "stripe_configured": bool(stripe.api_key)}

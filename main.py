from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/", response_class=HTMLResponse)
async def home():
    # Цей код створює гарну кнопку на головній сторінці
    return """
    <html>
        <head><title>SEO Turbo Indexer</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 100px;">
            <h1>🚀 SEO Turbo Indexer</h1>
            <p>Пришвидшіть індексацію вашого сайту в Google за 10$/міс.</p>
            <form action="/create-checkout-session" method="POST">
                <button type="submit" style="background-color: #6772E5; color: white; padding: 15px 30px; border: none; border-radius: 4px; font-size: 18px; cursor: pointer;">
                    Підписатися за $10
                </button>
            </form>
        </body>
    </html>
    """

@app.post("/create-checkout-session")
async def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'SEO Indexer Monthly Subscription'},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://google.com', # Сюди вставте посилання на ваш сайт після оплати
        cancel_url='https://google.com',
    )
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=session.url, status_code=303)
    

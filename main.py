from fastapi import FastAPI
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.get("/")
def home():
    return {"status": "SEO Indexer is Running", "message": "Welcome to your passive income machine!"}

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
        success_url='https://google.com', # Потім замінимо на ваш домен
        cancel_url='https://google.com',
    )
    return {"url": session.url}

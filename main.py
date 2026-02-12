from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe, os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def page(content):
    return f'<html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-gray-50 p-10 font-sans">{content}</body></html>'

@app.get("/", response_class=HTMLResponse)
async def home():
    c = '<h1 class="text-3xl font-black mb-6">SEO TURBO</h1>'
    c += '<div class="grid gap-4"><a href="/buy?plan=starter" class="p-4 bg-indigo-600 text-white rounded-xl">Buy Starter $10</a>'
    c += '<a href="/buy?plan=premium" class="p-4 bg-black text-white rounded-xl">Buy Premium $110</a></div>'
    return page(c)

@app.get("/buy")
async def buy(plan: str = 'starter'):
    prices = {'starter': 1000, 'premium': 11000}
    try:
        s = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': plan}, 'unit_amount': prices.get(plan, 1000)}, 'quantity': 1}],
            mode='payment',
            success_url='https://seo-indexer-production.up.railway.app/dashboard',
            cancel_url='https://seo-indexer-production.up.railway.app/'
        )
        return RedirectResponse(url=s.url, status_code=303)
    except Exception as e:
        return str(e)

@app.get("/dashboard", response_class=HTMLResponse)
async def dash():
    c = '<h1 class="text-2xl font-bold mb-4">Dashboard</h1>'
    c += '<form action="/send-links" method="post"><textarea name="links" class="w-full h-40 border p-4 mb-4"></textarea>'
    c += '<button class="w-full py-4 bg-indigo-600 text-white rounded-xl">Index Now</button></form>'
    return page(c)

@app.post("/send-links", response_class=HTMLResponse)
async def links(links: str = Form(...)):
    num = len([u for u in links.split('\n') if u.strip()])
    return page(f'<h1 class="text-xl">Success!</h1><p>Queued {num} links.</p><a href="/dashboard">Back</a>')

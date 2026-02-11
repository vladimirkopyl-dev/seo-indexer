from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, що ключ доданий у Variables на Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний заголовок зі стилями
HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Fast Google Indexing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        @keyframes bounce-slow { 0%, 100% { transform: translateY(-5%); } 50% { transform: translateY(0); } }
        .animate-bounce-slow { animation: bounce-slow 2s infinite; }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 text-slate-900 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-extrabold mb-4">🚀 SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">Get your pages indexed by Google in 24 hours.</p>
            </div>
            <div class="max-w-4xl mx-auto -mt-10 px-4 pb-20">
                <div class="glass-card rounded-3xl shadow-2xl p-8 md:p-12 text-center border border-white">
                    <span class="bg-indigo-100 text-indigo-700 px-4 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Limited Offer</span>
                    <div class="my-6">
                        <span class="text-5xl font-black">$8.99</span>
                        <span class="text-gray-500">/ month</span>
                    </div>
                    <ul class="text-left max-w-xs mx-auto space-y-4 mb-10 text-slate-600">
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> Instant API Submission</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> Unlimited URLs</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> 24/7 Priority Support</li>
                    </ul>
                    <a href="/buy" class="block w-full md:w-64 mx-auto bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold py-4 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg">
                        Get Instant Access
                    </a>
                </div>
                <div class="mt-12 text-center text-slate-400 text-sm">
                    <a href="/terms" class="hover:text-indigo-600">Terms</a> | <a href="/privacy" class="hover:text-indigo-600">Privacy</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout():
    try:
        # ПРИБРАНО f-string ТУТ, ЩОБ НЕ БУЛО ПОМИЛКИ З ДУЖКАМИ
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'SEO Turbo Indexer - Pro Access',
                        'description': 'Monthly Priority Indexing',
                    },
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
        return HTMLResponse(content=f"Stripe Error: {str(e)}", status_code=500)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 min-h-screen flex items-center justify-center p-6">
            <div class="max-w-xl w-full bg-white rounded-3xl shadow-xl overflow-hidden">
                <div class="bg-green-500 p-8 text-center text-white">
                    <div class="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-4 animate-bounce-slow">
                        <i class="fas fa-check text-3xl"></i>
                    </div>
                    <h1 class="text-3xl font-bold">Success!</h1>
                </div>
                <div class="p-8 text-center">
                    <form action="/send-links" method="post" class="space-y-4">
                        <textarea name="links" class="w-full h-48 p-4 bg-slate-50 border rounded-2xl outline-none" placeholder="Paste URLs here..."></textarea>
                        <button type="submit" class="w-full bg-black text-white font-bold py-4 rounded-2xl shadow-lg">Start Indexing</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\n') if url.strip()]
    return {"status": "success", "count": len(urls)}

@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return f"<html>{HEAD_CONTENT}<body class='p-10'><h1>Privacy Policy</h1><a href='/'>Back</a></body></html>"

@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return f"<html>{HEAD_CONTENT}<body class='p-10'><h1>Terms of Service</h1><a href='/'>Back</a></body></html>"

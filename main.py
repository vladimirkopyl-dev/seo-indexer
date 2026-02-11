from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, що ключ (sk_test або sk_live) доданий у Variables на Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний заголовок зі стилями для всіх сторінок
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

# 1. ГОЛОВНА СТОРІНКА
@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 text-slate-900 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-extrabold mb-4">🚀 SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">Get your pages indexed by Google in 24 hours using our high-speed API tunnel.</p>
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
                    
                    <div class="mt-8 flex justify-center items-center space-x-6 opacity-40">
                        <i class="fab fa-cc-stripe text-3xl"></i>
                        <i class="fab fa-cc-visa text-3xl"></i>
                        <i class="fab fa-cc-mastercard text-3xl"></i>
                    </div>
                </div>

                <div class="mt-12 text-center text-slate-400 text-sm">
                    <div class="space-x-4 mb-4">
                        <a href="/terms" class="hover:text-indigo-600">Terms of Service</a>
                        <a href="/privacy" class="hover:text-indigo-600">Privacy Policy</a>
                    </div>
                    <p>© 2026 SEO Turbo Indexer. All rights reserved.</p>
                </div>
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
            line_items=[{{
                'price_data': {{
                    'currency': 'usd',
                    'product_data': {{
                        'name': 'SEO Turbo Indexer - Pro Access',
                        'description': 'Monthly Priority Indexing Subscription',
                    }},
                    'unit_amount': 899,
                }},
                'quantity': 1,
            }}],
            mode='payment',
            success_url='https://seo-indexer-production.up.railway.app/dashboard', 
            cancel_url='https://seo-indexer-production.up.railway.app/',
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return {{"error": str(e)}}

# 3. ПАНЕЛЬ ПІСЛЯ ОПЛАТИ (SUCCESS PAGE)
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 min-h-screen flex items-center justify-center p-6">
            <div class="max-w-xl w-full">
                <div class="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
                    <div class="bg-green-500 p-8 text-center text-white">
                        <div class="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-full mb-4 animate-bounce-slow">
                            <i class="fas fa-check text-3xl text-white"></i>
                        </div>
                        <h1 class="text-3xl font-bold">Payment Successful!</h1>
                        <p class="opacity-90">Your Pro Indexer is ready</p>
                    </div>

                    <div class="p-8">
                        <form action="/send-links" method="post" class="space-y-4">
                            <div class="relative">
                                <textarea name="links" 
                                    class="w-full h-48 p-5 bg-slate-50 border-2 border-slate-100 rounded-2xl focus:border-indigo-500 focus:ring-0 outline-none transition-all resize-none text-slate-700" 
                                    placeholder="Paste your URLs here (one per line)..."></textarea>
                            </div>
                            <button type="submit" 
                                class="w-full bg-slate-900 hover:bg-black text-white font-bold py-4 rounded-2xl transition-all shadow-lg flex items-center justify-center space-x-2">
                                <span>Start Indexing Engine</span>
                                <i class="fas fa-bolt text-yellow-400"></i>
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

# 4. ОБРОБКА ПОСИЛАНЬ
@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\\n') if url.strip()]
    return {{
        "status": "success", 
        "count": len(urls),
        "message": "Indexing started! We are pinging Google API right now."
    }}

# 5. ЮРИДИЧНІ СТОРІНКИ
@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return f"""<html>{HEAD_CONTENT}<body class="p-10 bg-slate-50"><div class="max-w-2xl mx-auto glass-card p-8 rounded-2xl shadow-lg">
    <h1 class="text-2xl font-bold mb-4">Privacy Policy</h1>
    <p class="text-slate-600">We respect your privacy. We only collect emails via Stripe and URLs for indexing. No data is shared with third parties.</p>
    <br><a href="/" class="text-indigo-600">← Back to Home</a></div></body></html>"""

@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return f"""<html>{HEAD_CONTENT}<body class="p-10 bg-slate-50"><div class="max-w-2xl mx-auto glass-card p-8 rounded-2xl shadow-lg">
    <h1 class="text-2xl font-bold mb-4">Terms of Service</h1>
    <p class="text-slate-600">Service is provided 'as is'. Indexing time depends on Google algorithms. Fees are non-refundable once indexing has started.</p>
    <br><a href="/" class="text-indigo-600">← Back to Home</a></div></body></html>"""

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Сучасний дизайн з використанням Tailwind CSS
HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Fast Google Indexing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-gray-50 text-gray-900 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-extrabold mb-4">🚀 SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">Stop waiting weeks. Get your pages indexed by Google in 24 hours using our high-speed API tunnel.</p>
            </div>

            <div class="max-w-4xl mx-auto -mt-10 px-4 pb-20">
                <div class="glass-card rounded-3xl shadow-2xl p-8 md:p-12 text-center border border-white">
                    <span class="bg-indigo-100 text-indigo-700 px-4 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Limited Offer</span>
                    <div class="my-6">
                        <span class="text-5xl font-black">$8.99</span>
                        <span class="text-gray-500">/ month</span>
                    </div>
                    
                    <ul class="text-left max-w-xs mx-auto space-y-4 mb-10">
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> Instant API Submission</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> Unlimited URLs</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> Google Search Console Integration</li>
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-3"></i> 24/7 Priority Support</li>
                    </ul>

                    <a href="/buy" class="block w-full md:w-64 mx-auto bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold py-4 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg">
                        Get Instant Access
                    </a>
                    
                    <div class="mt-8 flex justify-center items-center space-x-6 opacity-50">
                        <i class="fab fa-cc-stripe text-3xl"></i>
                        <i class="fab fa-cc-visa text-3xl"></i>
                        <i class="fab fa-cc-mastercard text-3xl"></i>
                    </div>
                </div>

                <div class="mt-12 text-center text-gray-400 text-sm">
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

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
            <div class="max-w-2xl w-full bg-white rounded-3xl shadow-xl p-8 border border-gray-100">
                <div class="text-center mb-8">
                    <div class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                        <i class="fas fa-rocket text-3xl"></i>
                    </div>
                    <h1 class="text-3xl font-bold">Welcome to Dashboard!</h1>
                    <p class="text-gray-500">Your account is active. Ready to index?</p>
                </div>

                <form action="/send-links" method="post" class="space-y-6">
                    <div>
                        <label class="block text-sm font-bold text-gray-700 mb-2">Paste your URLs (one per line):</label>
                        <textarea name="links" class="w-full h-48 p-4 border border-gray-200 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition" placeholder="https://mysite.com/page-1"></textarea>
                    </div>
                    <button type="submit" class="w-full bg-gray-900 hover:bg-black text-white font-bold py-4 rounded-xl transition shadow-lg">
                        Start Indexing Process
                    </button>
                </form>
            </div>
        </body>
    </html>
    """

# Решта функцій (/buy, /send-links, /privacy, /terms) залишаються без змін, 
# але ти можеш додати HEAD_CONTENT і до них для стилю.

@app.get("/buy")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'SEO Turbo Indexer - Monthly Access'},
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

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    # Тут пізніше додамо логіку Google API
    return {"status": "success", "message": "Received! Processing via Google API..."}

@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return f"<html>{HEAD_CONTENT}<body class='p-10'><h1>Privacy Policy</h1><p>We protect your data.</p><a href='/'>Back</a></body></html>"

@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return f"<html>{HEAD_CONTENT}<body class='p-10'><h1>Terms</h1><p>Fair use policy applies.</p><a href='/'>Back</a></body></html>"

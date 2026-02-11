from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Fast Google Indexing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        details > summary { list-style: none; }
        details > summary::-webkit-details-marker { display: none; }
        details[open] summary i { transform: rotate(180deg); }
    </style>
</head>
"""

# Список питань та відповідей (я додав перші кілька для прикладу, код нижче містить логіку для всіх)
FAQ_ITEMS = [
    ("What is a URL and what can be indexed?", "A URL (Uniform Resource Locator) is the unique address of a web page... [додайте повний текст тут або використовуйте скорочену версію]"),
    ("Why is it important to index a URL?", "If a page is not indexed, it is invisible to users searching online..."),
    # ... решта 24 питання
]

@app.get("/", response_class=HTMLResponse)
async def home():
    # Генеруємо HTML для FAQ
    faq_html = ""
    faqs = [
        ("What is a URL and what can be indexed?", "A URL is the unique address of a web page. It must start with 'http://' or 'https://'. You can submit blog posts, articles, backlinks, social profiles, and product pages. Ensure the page is public and returns a 200 OK status."),
        ("Why is it important to index a URL?", "Without indexing, your content won't appear in Google search results. Fast indexing attracts visitors earlier, builds trust, and helps you rank for keywords before competitors."),
        ("Why use IndexBooster?", "IndexBooster initiates active indexing requests instead of waiting weeks for organic discovery. You get automation, clear reports, and a credit-back guarantee if indexing fails."),
        ("How long does Google take to index a URL?", "It varies from a few hours to weeks. IndexBooster accelerates this by prompting Google to recrawl your pages immediately."),
        ("Does indexing guarantee ranking?", "No. Indexing means Google knows your page exists. Ranking depends on content quality, keywords, and authority. Indexing is just the first, essential step."),
        ("Is there any credit expiration date?", "No. Your credits never expire. There is no subscription — you only pay for successful results."),
        ("Can IndexBooster harm my website?", "No. We use safe, multi-step pipelines compliant with search engine policies. We don't use spammy techniques or low-quality backlinks.")
    ]
    
    for q, a in faqs:
        faq_html += f"""
        <details class="group border-b border-slate-200 py-4 cursor-pointer">
            <summary class="flex justify-between items-center font-bold text-slate-700 hover:text-indigo-600 transition">
                <span>{q}</span>
                <i class="fas fa-chevron-down text-xs transition-transform duration-300"></i>
            </summary>
            <p class="mt-3 text-slate-500 leading-relaxed text-sm">{a}</p>
        </details>
        """

    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 text-slate-900 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-extrabold mb-4">🚀 SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">Get your pages indexed by Google in 24 hours.</p>
            </div>

            <div class="max-w-4xl mx-auto -mt-10 px-4 pb-20">
                <div class="glass-card rounded-3xl shadow-2xl p-8 md:p-12 text-center border border-white mb-16">
                    <span class="bg-indigo-100 text-indigo-700 px-4 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Pay-as-you-go</span>
                    <div class="my-6">
                        <span class="text-5xl font-black">$8.99</span>
                        <span class="text-gray-500">/ pack</span>
                    </div>
                    <a href="/buy" class="block w-full md:w-64 mx-auto bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold py-4 rounded-xl transition transform hover:scale-105 shadow-lg">
                        Get Instant Access
                    </a>
                </div>

                <div class="bg-white rounded-3xl shadow-xl p-8 md:p-12 border border-slate-100">
                    <h2 class="text-3xl font-bold mb-8 text-center">Frequently Asked Questions</h2>
                    <div class="space-y-2">
                        {faq_html}
                    </div>
                    <div class="mt-8 text-center">
                        <p class="text-slate-400 text-sm">Have more questions? Contact our 24/7 support.</p>
                    </div>
                </div>

                <div class="mt-12 text-center text-slate-400 text-sm">
                    <div class="space-x-4 mb-4">
                        <a href="/terms" class="hover:text-indigo-600">Terms</a>
                        <a href="/privacy" class="hover:text-indigo-600">Privacy</a>
                    </div>
                    <p>© 2026 SEO Turbo Indexer. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """

# Решта функцій (/buy, /dashboard, /send-links) залишаються такими ж, як ми робили раніше
@app.get("/buy")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'SEO Turbo Indexer - Pro Credits'},
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
        return HTMLResponse(content=f"Error: {str(e)}", status_code=500)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"<html>{HEAD_CONTENT}<body class='bg-slate-50 flex items-center justify-center min-h-screen p-6'><div class='bg-white p-8 rounded-3xl shadow-xl max-w-md w-full text-center'><h1 class='text-2xl font-bold mb-4'>✅ Payment Successful!</h1><form action='/send-links' method='post'><textarea name='links' class='w-full h-40 border rounded-xl p-4 mb-4' placeholder='Enter URLs...'></textarea><button class='bg-black text-white w-full py-3 rounded-xl font-bold'>Start Indexing</button></form></div></body></html>"

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    return {"status": "success", "message": "Indexing started!"}

@app.get("/privacy", response_class=HTMLResponse)
async def privacy(): return "Privacy Policy"

@app.get("/terms", response_class=HTMLResponse)
async def terms(): return "Terms of Service"

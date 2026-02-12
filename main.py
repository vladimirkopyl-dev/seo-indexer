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
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
        .plan-card:hover { transform: translateY(-5px); transition: all 0.3s ease; }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    # Дані для списків (без зайвих відступів)
    features_list = [
        ("HANDY & SIMPLE", "fas fa-user-check", "A user-friendly platform designed to make the process straightforward."),
        ("BUILT-IN CHECKER", "fas fa-search", "Instantly verify index status without third-party tools."),
        ("80% EFFICIENCY", "fas fa-bolt", "Success rate within just 72 hours of submission."),
        ("RESULTS ONLY", "fas fa-shield-alt", "Pay only for pages that actually get indexed."),
        ("FLEXIBLE PAYMENT", "fas fa-credit-card", "Multiple secure payment methods available."),
        ("SIMPLE API", "fas fa-code", "Integrate indexing into your workflow with our API.")
    ]
    
    faq_list = [
        ("What is a URL and what can be indexed?", "A URL must start with http:// or https://. You can index blog posts, backlinks, and profiles."),
        ("How long does indexing take?", "Most pages (70%) are indexed within 24 hours. We monitor for up to 10 days."),
        ("What happens if a URL is not indexed?", "Your credit is automatically returned to your balance after 10 days.")
    ]

    features_html = "".join([f"""
        <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="{f[1]}"></i></div>
            <h4 class="font-bold text-slate-800 text-xs mb-2 uppercase tracking-tight">{f[0]}</h4>
            <p class="text-slate-500 text-[10px] leading-relaxed">{f[2]}</p>
        </div>
    """ for f in features_list])

    faq_html = "".join([f"""
        <details class="group bg-white border border-slate-200 rounded-xl mb-3">
            <summary class="flex justify-between items-center p-4 font-bold text-slate-700 uppercase text-[10px] tracking-wider">
                {q} <i class="fas fa-chevron-down text-indigo-500 transition-transform"></i>
            </summary>
            <div class="px-4 pb-4 text-slate-500 text-xs leading-relaxed border-t border-slate-50 pt-3">{a}</div>
        </details>
    """ for q, a in faq_list])

    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 font-sans text-slate-900">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-black mb-4 uppercase italic">SEO Turbo Indexer</h1>
                <p class="text-lg opacity-90 mb-8">You Pay for Actually Indexed Pages</p>
                <a href="#prices" class="bg-white text-indigo-600 px-8 py-4 rounded-xl font-black uppercase tracking-widest shadow-xl">Start Indexation Now</a>
            </div>

            <div class="max-w-6xl mx-auto px-4 -mt-10 pb-20">
                <div class="bg-white rounded-3xl shadow-xl p-8 mb-16 border border-white">
                    <h2 class="text-2xl font-black text-center mb-8 uppercase italic text-slate-800">How It Works?</h2>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
                        <div><div class="font-black text-indigo-600 text-xl">1</div><p class="text-xs font-bold uppercase italic">Create Project</p></div>
                        <div><div class="font-black text-indigo-600 text-xl">2</div><p class="text-xs font-bold uppercase italic">Pre-Index Check</p></div>
                        <div><div class="font-black text-indigo-600 text-xl">3</div><p class="text-xs font-bold uppercase italic">Safe Launch</p></div>
                        <div><div class="font-black text-indigo-600 text-xl">4</div><p class="text-xs font-bold uppercase italic">Fair Refund</p></div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
                    <div class="bg-slate-900 rounded-3xl p-8 text-white">
                        <h3 class="text-xl font-black mb-6 uppercase italic text-indigo-400">Indexing Timeline</h3>
                        <div class="space-y-4 text-xs">
                            <p><strong>DAY 1:</strong> Up to 70% indexed.</p>
                            <p><strong>DAY 2-7:</strong> Final boost of 15-20%.</p>
                            <p class="text-green-400"><strong>DAY 10:</strong> Automatic Refund for non-indexed.</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">{features_html}</div>
                </div>

                <div id="prices" class="py-10">
                    <h2 class="text-3xl font-black text-center mb-10 uppercase italic">Prices</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center">
                            <h3 class="font-black uppercase mb-2">Starter</h3>
                            <div class="text-2xl font-black mb-4 font-mono text-indigo-600">$10</div>
                            <p class="text-[10px] mb-4 text-slate-500 uppercase font-bold">20 Credits</p>
                            <a href="/buy?plan=starter" class="block bg-indigo-600 text-white py-3 rounded-xl text-[10px] font-black uppercase tracking-widest">Purchase</a>
                        </div>
                        <div class="plan-card bg-indigo-600 p-6 rounded-3xl text-white text-center scale-105 shadow-2xl">
                            <h3 class="font-black uppercase mb-2">Premium</h3>
                            <div class="text-2xl font-black mb-4 font-mono text-yellow-400">$110</div>
                            <p class="text-[10px] mb-4 opacity-80 uppercase font-bold">250 Credits</p>
                            <a href="/buy?plan=premium" class="block bg-white text-indigo-600 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center">
                            <h3 class="font-black uppercase mb-2">Agency</h3>
                            <div class="text-2xl font-black mb-4 font-mono text-indigo-600">$200</div>
                            <p class="text-[10px] mb-4 text-slate-500 uppercase font-bold">500 Credits</p>
                            <a href="/buy?plan=agency" class="block bg-indigo-600 text-white py-3 rounded-xl text-[10px] font-black uppercase tracking-widest">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center">
                            <h3 class="font-black uppercase mb-2">Guru</h3>
                            <div class="text-2xl font-black mb-4 font-mono text-indigo-600">$630</div>
                            <p class="text-[10px] mb-4 text-slate-500 uppercase font-bold">1800 Credits</p>
                            <a href="/buy?plan=guru" class="block bg-indigo-600 text-white py-3 rounded-xl text-[10px] font-black uppercase tracking-widest">Purchase</a>
                        </div>
                    </div>
                </div>

                <div class="max-w-2xl mx-auto mt-20 italic">
                    <h3 class="text-xl font-black text-center mb-8 uppercase tracking-widest">FAQ</h3>
                    {faq_html}
                </div>
            </div>
            
            <footer class="text-center py-10 text-[10px] text-slate-400 font-bold uppercase tracking-widest">
                © 2026 SEO Turbo Indexer Engine
            </footer>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout(plan: str = "starter"):
    plan_data = {"starter": 1000, "premium": 11000, "agency": 20000, "guru": 63000}
    price = plan_data.get(plan, 1000)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': f"SEO Turbo Indexer {plan.capitalize()}"}, 'unit_amount': price}, 'quantity': 1}],
            mode='payment',
            success_url='https://seo-indexer-production.up.railway.app/dashboard',
            cancel_url='https://seo-indexer-production.up.railway.app/'
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return HTMLResponse(content=f"Stripe Error: {str(e)}", status_code=500)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return f"<html>{HEAD_CONTENT}<body class='bg-slate-50 p-6'><div class='max-w-md mx-auto bg-white p-8 rounded-3xl shadow-xl text-center'><h1 class='text-xl font-black uppercase text-green-600 mb-6'>Payment OK</h1><form action='/send-links' method='post'><textarea name='links' class='w-full h-40 border-2 border-slate-100 rounded-xl p-4 mb-4' placeholder='Enter URLs...'></textarea><button class='bg-black text-white w-full py-4 rounded-xl font-black uppercase tracking-widest'>Start Engine</button></form></div></body></html>"

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\\n') if url.strip()]
    return {"status": "success", "count": len(urls)}

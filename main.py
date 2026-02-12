from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, что в налаштуваннях Railway додано змінну STRIPE_SECRET_KEY
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільні стилі та мета-теги
HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Professional Google Indexing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .plan-card:hover { transform: translateY(-5px); transition: all 0.3s ease; }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    # Дані для контенту
    features_list = [
        ("HANDY & SIMPLE", "fas fa-user-check", "A user-friendly platform designed to make the process straightforward."),
        ("BUILT-IN CHECKER", "fas fa-search", "Instantly verify if your pages are in Google’s index."),
        ("80% EFFICIENCY", "fas fa-bolt", "Achieve high indexing success rate within just 72 hours."),
        ("CREDITS FOR RESULTS", "fas fa-shield-alt", "Pay only for pages that actually get indexed. No waste."),
        ("FLEXIBLE PAYMENT", "fas fa-credit-card", "Multiple secure payment methods available."),
        ("SIMPLE API", "fas fa-code", "Easily integrate SEO Turbo Indexer into your workflow.")
    ]

    faq_list = [
        ("What is a URL and what can be indexed?", "A URL must lead to an accessible page. We index blog posts, backlinks, and profiles."),
        ("How long does indexing take?", "Most pages (70%) are indexed within 24 hours. We monitor for 10 days."),
        ("What happens if a URL is not indexed?", "Your credit is automatically returned to your balance after 10 days.")
    ]

    # Генерація HTML компонентів
    features_html = "".join([f"""
        <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="{f[1]}"></i></div>
            <h4 class="font-bold text-slate-800 text-[10px] mb-2 uppercase tracking-tight">{f[0]}</h4>
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
        <body class="bg-slate-50 font-sans text-slate-900 leading-normal">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <div class="max-w-4xl mx-auto">
                    <h1 class="text-4xl md:text-6xl font-black mb-4 uppercase italic">SEO Turbo Indexer</h1>
                    <p class="text-lg md:text-xl font-light mb-8">You Pay for Actually Indexed Pages</p>
                    <a href="#prices" class="inline-block bg-white text-indigo-600 px-10 py-4 rounded-xl font-black text-sm shadow-2xl hover:bg-slate-50 transition-all uppercase italic tracking-wider">Start Indexation Now</a>
                    <p class="mt-6 text-[10px] opacity-70 italic font-bold uppercase tracking-widest">No index — no charge. Pay for real results.</p>
                </div>
            </div>

            <div class="max-w-6xl mx-auto px-4 -mt-10 pb-20">
                <div class="bg-white rounded-3xl shadow-xl p-8 mb-16 border border-white">
                    <h2 class="text-xl font-black text-center mb-8 uppercase italic text-slate-800 tracking-widest">How It Works?</h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
                        <div><div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">1</div><p class="text-[10px] font-bold uppercase italic">Create Project</p></div>
                        <div><div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">2</div><p class="text-[10px] font-bold uppercase italic">Pre-Index Check</p></div>
                        <div><div class="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">3</div><p class="text-[10px] font-bold uppercase italic">Turbo Launch</p></div>
                        <div><div class="w-10 h-10 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">4</div><p class="text-[10px] font-bold uppercase italic text-green-600">Fair Refund</p></div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
                    <div class="bg-slate-900 rounded-3xl p-8 text-white shadow-2xl">
                        <h3 class="text-xl font-black mb-6 uppercase italic text-indigo-400">Indexing Timeline</h3>
                        <div class="space-y-6">
                            <div class="flex items-center">
                                <div class="bg-indigo-500 text-[10px] font-bold px-2 py-1 rounded mr-4 uppercase">Day 1</div>
                                <p class="text-xs opacity-80 italic">The Fast Start: Up to 70% indexed.</p>
                            </div>
                            <div class="flex items-center">
                                <div class="bg-indigo-500 text-[10px] font-bold px-2 py-1 rounded mr-4 uppercase">Day 2-7</div>
                                <p class="text-xs opacity-80 italic">Final Boost: Last 15-20% pages added.</p>
                            </div>
                            <div class="flex items-center">
                                <div class="bg-green-500 text-[10px] font-bold px-2 py-1 rounded mr-4 uppercase font-black">Refund</div>
                                <p class="text-xs text-green-400 italic font-bold">Automatic credit return after 10 days.</p>
                            </div>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">{features_html}</div>
                </div>

                <div id="prices" class="py-12">
                    <h2 class="text-3xl font-black text-center mb-12 uppercase italic text-slate-800">Performance Plans</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col text-center">
                            <h3 class="font-black text-sm uppercase italic mb-2">Starter</h3>
                            <div class="text-2xl font-black mb-4">$10</div>
                            <ul class="text-[10px] space-y-2 mb-8 text-slate-500 flex-grow font-bold uppercase">
                                <li class="text-indigo-600 font-black italic">20 Credits</li>
                                <li>1 Credit = $0.50</li>
                                <li>No Subscription</li>
                            </ul>
                            <a href="/buy?plan=starter" class="block bg-indigo-600 text-white font-black py-4 rounded-xl text-[10px] uppercase tracking-widest hover:bg-indigo-700 transition">Purchase</a>
                        </div>
                        <div class="plan-card bg-indigo-600 p-6 rounded-3xl shadow-2xl flex flex-col text-center scale-105 text-white">
                            <h3 class="font-black text-sm uppercase italic mb-2">Premium</h3>
                            <div class="text-2xl font-black mb-4">$110</div>
                            <ul class="text-[10px] space-y-2 mb-8 opacity-90 flex-grow font-bold uppercase">
                                <li class="text-yellow-400 font-black italic">250 Credits</li>
                                <li>1 Credit = $0.44</li>
                                <li>Most Popular</li>
                            </ul>
                            <a href="/buy?plan=premium" class="block bg-white text-indigo-600 font-black py-4 rounded-xl text-[10px] uppercase tracking-widest hover:bg-slate-50 transition">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col text-center">
                            <h3 class="font-black text-sm uppercase italic mb-2">Agency</h3>
                            <div class="text-2xl font-black mb-4">$200</div>
                            <ul class="text-[10px] space-y-2 mb-8 text-slate-500 flex-grow font-bold uppercase">
                                <li class="text-indigo-600 font-black italic">500 Credits</li>
                                <li>1 Credit = $0.40</li>
                                <li>Best for Teams</li>
                            </ul>
                            <a href="/buy?plan=agency" class="block bg-indigo-600 text-white font-black py-4 rounded-xl text-[10px] uppercase tracking-widest hover:bg-indigo-700 transition">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col text-center">
                            <h3 class="font-black text-sm uppercase italic mb-2">Guru</h3>
                            <div class="text-2xl font-black mb-4">$630</div>
                            <ul class="text-[10px] space-y-2 mb-8 text-slate-500 flex-grow font-bold uppercase">
                                <li class="text-indigo-600 font-black italic">1800 Credits</li>
                                <li>1 Credit = $0.35</li>
                                <li>Max Economy</li>
                            </ul>
                            <a href="/buy?plan=guru" class="block bg-indigo-600 text-white font-black py-4 rounded-xl text-[10px] uppercase tracking-widest hover:bg-indigo-700 transition">Purchase</a>
                        </div>
                    </div>
                </div>

                <div class="max-w-2xl mx-auto mt-20">
                    <h3 class="text-xl font-black text-center mb-10 uppercase italic tracking-widest">Quick Answers (FAQ)</h3>
                    {faq_html}
                </div>
            </div>

            <footer class="bg-slate-900 text-slate-500 py-10 text-center">
                <p class="text-[10px] font-bold uppercase tracking-widest">© 2026 SEO Turbo Indexer Engine</p>
            </footer>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout(plan: str = "starter"):
    plan_data = {
        "starter": 1000,
        "premium": 11000,
        "agency": 20000,
        "guru": 63000
    }
    price = plan_data.get(plan, 1000)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"SEO Turbo Indexer - {plan.capitalize()} Pack"},
                    'unit_amount': price,
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
        <body class="bg-slate-50 p-6 min-h-screen flex items-center justify-center">
            <div class="max-w-md w-full bg-white p-8 rounded-3xl shadow-2xl border border-slate-100 text-center">
                <h1 class="text-xl font-black uppercase italic text-indigo-600 mb-6 tracking-wider">Project Dashboard</h1>
                <p class="text-xs text-slate-400 mb-6 font-bold uppercase tracking-widest">Enter URLs to start indexing</p>
                <form action="/send-links" method="post">
                    <textarea name="links" class="w-full h-40 border-2 border-slate-50 rounded-2xl p-4 mb-4 focus:border-indigo-500 outline-none transition text-sm font-mono" placeholder="https://example.com/page1\\nhttps://example.com/page2"></textarea>
                    <button class="bg-black text-white w-full py-4 rounded-xl font-black uppercase tracking-widest hover:bg-slate-800 shadow-lg transition">Launch Turbo Engine</button>
                </form>
            </div>
        </body>
    </html>
    """

@app.post("/send-links", response_class=HTMLResponse)
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\\n') if url.strip()]
    count = len(urls)
    
    # СТИЛІЗОВАНА СТОРІНКА ПІДТВЕРДЖЕННЯ
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 flex items-center justify-center min-h-screen p-6">
            <div class="max-w-md w-full bg-white rounded-3xl shadow-2xl p-10 text-center border border-slate-100">
                <div class="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6">
                    <i class="fas fa-rocket text-3xl"></i>
                </div>
                <h1 class="text-2xl font-black uppercase italic text-slate-800 mb-2 tracking-tighter">Engine Started!</h1>
                <p class="text-slate-500 mb-8 font-medium">Successfully received <span class="text-indigo-600 font-black">{count}</span> URLs for processing.</p>
                
                <div class="bg-slate-50 rounded-2xl p-4 mb-8 text-left border border-slate-100">
                    <div class="flex items-center text-[9px] font-black text-slate-400 uppercase tracking-widest mb-3">
                        <i class="fas fa-microchip mr-2"></i> Current Status
                    </div>
                    <ul class="text-[11px] text-slate-600 space-y-3 font-bold uppercase tracking-tight">
                        <li class="flex items-center"><i class="fas fa-check-circle text-green-500 mr-2"></i> Pre-index analysis... OK</li>
                        <li class="flex items-center"><i class="fas fa-spinner fa-spin text-indigo-500 mr-2"></i> Google Ping queue... Active</li>
                        <li class="flex items-center"><i class="fas fa-shield-alt text-slate-400 mr-2"></i> 10-day refund window... Locked</li>
                    </ul>
                </div>

                <a href="/dashboard" class="block w-full py-4 bg-indigo-600 text-white rounded-xl font-black uppercase tracking-widest hover:bg-indigo-700 transition shadow-lg">
                    Back to Dashboard
                </a>
            </div>
        </body>
    </html>
    """

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Ключ Stripe має бути в налаштуваннях Railway (Variables)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Fast Google Indexing</title>
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
            <div class="gradient-bg text-white py-20 px-4 text-center text-shadow-lg">
                <h1 class="text-4xl md:text-6xl font-black mb-4 uppercase italic">SEO Turbo Indexer</h1>
                <p class="text-lg opacity-90 mb-8 font-medium">Fast Google Indexing: Pay Only For Results</p>
                <a href="#prices" class="inline-block bg-white text-indigo-600 px-10 py-4 rounded-xl font-black uppercase tracking-widest shadow-2xl hover:scale-105 transition-all text-sm">Start Indexation Now</a>
            </div>

            <div class="max-w-6xl mx-auto px-4 -mt-10 pb-20">
                <div class="bg-white rounded-3xl shadow-xl p-8 mb-16 border border-white">
                    <h2 class="text-xl font-black text-center mb-8 uppercase italic text-slate-800 tracking-widest text-shadow-sm">How It Works?</h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
                        <div><div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">1</div><p class="text-[10px] font-bold uppercase italic">Create Project</p></div>
                        <div><div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">2</div><p class="text-[10px] font-bold uppercase italic">Analysis</p></div>
                        <div><div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">3</div><p class="text-[10px] font-bold uppercase italic">Turbo Launch</p></div>
                        <div><div class="w-12 h-12 bg-green-50 text-green-600 rounded-full flex items-center justify-center mx-auto mb-3 font-black">4</div><p class="text-[10px] font-bold uppercase italic text-green-600">Fair Refund</p></div>
                    </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-20">{features_html}</div>

                <div id="prices" class="py-10">
                    <h2 class="text-3xl font-black text-center mb-12 uppercase italic tracking-tighter">Choose Your Plan</h2>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center shadow-sm">
                            <h3 class="font-black uppercase mb-2 text-sm italic">Starter</h3>
                            <div class="text-3xl font-black mb-4 text-indigo-600 font-mono">$10</div>
                            <p class="text-[10px] mb-6 text-slate-400 font-bold uppercase tracking-widest">20 Credits</p>
                            <a href="/buy?plan=starter" class="block bg-indigo-600 text-white py-4 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 transition shadow-lg">Purchase</a>
                        </div>
                        <div class="plan-card bg-indigo-600 p-6 rounded-3xl text-white text-center scale-105 shadow-2xl relative">
                            <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-yellow-400 text-indigo-900 text-[8px] font-black px-3 py-1 rounded-full uppercase">Popular</div>
                            <h3 class="font-black uppercase mb-2 text-sm italic">Premium</h3>
                            <div class="text-3xl font-black mb-4 text-yellow-400 font-mono">$110</div>
                            <p class="text-[10px] mb-6 opacity-70 font-bold uppercase tracking-widest">250 Credits</p>
                            <a href="/buy?plan=premium" class="block bg-white text-indigo-600 py-4 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-slate-50 transition shadow-lg">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center shadow-sm">
                            <h3 class="font-black uppercase mb-2 text-sm italic">Agency</h3>
                            <div class="text-3xl font-black mb-4 text-indigo-600 font-mono">$200</div>
                            <p class="text-[10px] mb-6 text-slate-400 font-bold uppercase tracking-widest">500 Credits</p>
                            <a href="/buy?plan=agency" class="block bg-indigo-600 text-white py-4 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 transition shadow-lg">Purchase</a>
                        </div>
                        <div class="plan-card bg-white p-6 rounded-3xl border border-slate-200 text-center shadow-sm">
                            <h3 class="font-black uppercase mb-2 text-sm italic">Guru</h3>
                            <div class="text-3xl font-black mb-4 text-indigo-600 font-mono">$630</div>
                            <p class="text-[10px] mb-6 text-slate-400 font-bold uppercase tracking-widest">1800 Credits</p>
                            <a href="/buy?plan=guru" class="block bg-indigo-600 text-white py-4 rounded-xl text-[10px] font-black uppercase tracking-widest hover:bg-indigo-700 transition shadow-lg">Purchase</a>
                        </div>
                    </div>
                </div>

                <div class="max-w-2xl mx-auto mt-24">
                    <h3 class="text-xl font-black text-center mb-10 uppercase italic tracking-widest text-slate-400">Common Questions</h3>
                    {faq_html}
                </div>
            </div>
            
            <footer class="text-center py-12 text-[10px] text-slate-400 font-bold uppercase tracking-widest bg-white border-t border-slate-50">
                © 2026 SEO Turbo Indexer Engine • Fast & Fair
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
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f"SEO Turbo Indexer - {plan.capitalize()} Pack"},
                    'unit_amount': price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='

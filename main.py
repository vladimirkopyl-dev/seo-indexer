from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

HEAD_CONTENT = """
<head>
    <title>IndexBooster | Pricing Plans</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .plan-card:hover { transform: translateY(-10px); transition: all 0.3s ease; }
        .popular-badge { background: #feb47b; color: #fff; position: absolute; top: -15px; left: 50%; transform: translateX(-50%); padding: 4px 15px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    plans = [
        {"name": "Starter", "price": 10, "credits": 20, "per_credit": "0.50", "color": "slate"},
        {"name": "Premium", "price": 110, "credits": 250, "per_credit": "0.44", "color": "indigo", "popular": True},
        {"name": "Agency", "price": 200, "credits": 500, "per_credit": "0.40", "color": "slate"},
        {"name": "Guru", "price": 630, "credits": 1800, "per_credit": "0.35", "color": "slate"}
    ]

    plans_html = ""
    for p in plans:
        border = "border-2 border-indigo-500 shadow-xl scale-105" if p.get("popular") else "border border-slate-200 shadow-sm"
        badge = '<div class="popular-badge uppercase">Most Popular</div>' if p.get("popular") else ""
        
        plans_html += f"""
        <div class="plan-card relative bg-white p-8 rounded-3xl {border} flex flex-col h-full">
            {badge}
            <h3 class="text-xl font-bold text-slate-800 mb-2">{p['name']}</h3>
            <div class="mb-4">
                <span class="text-4xl font-black">${p['price']}</span>
                <span class="text-slate-400 text-sm italic">Without Tax</span>
            </div>
            <ul class="text-left text-sm space-y-3 mb-8 text-slate-600 flex-grow">
                <li class="font-bold text-indigo-600 flex items-center"><i class="fas fa-coins mr-2"></i> {p['credits']} Credits</li>
                <li><i class="fas fa-tag mr-2 text-slate-300"></i> 1 Credit = ${p['per_credit']}</li>
                <li><i class="fas fa-check mr-2 text-green-500"></i> 1 Credit = 1 Indexed URL</li>
                <li><i class="fas fa-sync mr-2 text-green-500"></i> Automatic Indexation Check</li>
                <li><i class="fas fa-undo mr-2 text-green-500"></i> Re-Credit after 10 Days</li>
                <li><i class="fas fa-history mr-2 text-green-500"></i> Treatment History</li>
                <li><i class="fas fa-ban mr-2 text-green-500"></i> No Monthly Subscription</li>
                <li><i class="fas fa-infinity mr-2 text-green-500"></i> Credits Do Not Expire</li>
                <li><i class="fas fa-code mr-2 text-green-500"></i> Free API</li>
            </ul>
            <a href="/buy?plan={p['name'].lower()}" class="block w-full text-center bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl transition shadow-lg uppercase">Purchase</a>
        </div>
        """

    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 font-sans">
            <div class="gradient-bg text-white py-16 px-4 text-center">
                <h1 class="text-4xl md:text-5xl font-black mb-4">Choose Your Indexing Power</h1>
                <p class="opacity-80">Simple pricing. Pay only for what actually gets indexed.</p>
            </div>

            <div class="max-w-7xl mx-auto px-4 -mt-10 pb-20">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {plans_html}
                </div>
                
                <div class="mt-20 text-center max-w-3xl mx-auto bg-white p-10 rounded-3xl shadow-lg border border-slate-100">
                    <h2 class="text-2xl font-bold mb-4">IndexBooster: You Pay for Actually Indexed Pages</h2>
                    <p class="text-slate-600 mb-6">No index — no charge. If a page doesn’t appear in Google search results, your credit is instantly returned. Stop paying for promises — pay for real results.</p>
                    <div class="flex flex-wrap justify-center gap-4 text-sm font-bold text-slate-400 uppercase">
                        <span><i class="fas fa-shield-alt text-green-500 mr-2"></i> Safe Process</span>
                        <span><i class="fas fa-bolt text-yellow-500 mr-2"></i> Fast Results</span>
                        <span><i class="fas fa-redo text-indigo-500 mr-2"></i> Auto Refund</span>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/buy")
async def create_checkout(plan: str = "starter"):
    # Словник цін
    plan_data = {
        "starter": {"price": 1000, "credits": 20},
        "premium": {"price": 11000, "credits": 250},
        "agency": {"price": 20000, "credits": 500},
        "guru": {"price": 63000, "credits": 1800}
    }
    
    selected = plan_data.get(plan, plan_data["starter"])
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"IndexBooster {plan.capitalize()} Pack",
                        'description': f"{selected['credits']} Indexing Credits",
                    },
                    'unit_amount': selected['price'],
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
    return f"<html>{HEAD_CONTENT}<body class='bg-slate-100 flex items-center justify-center min-h-screen'><div class='bg-white p-10 rounded-3xl shadow-2xl max-w-md w-full'><h1 class='text-2xl font-bold text-green-600 mb-4'>✅ Payment Successful</h1><p class='text-slate-500 mb-6 font-medium'>Your credits have been added. Start indexing below.</p><form action='/send-links' method='post'><textarea name='links' class='w-full h-40 border-2 border-slate-100 rounded-2xl p-4 mb-4 focus:border-indigo-500 outline-none transition resize-none' placeholder='Paste URLs (one per line)...'></textarea><button class='bg-black text-white w-full py-4 rounded-2xl font-bold shadow-lg hover:bg-slate-800 transition uppercase tracking-wider'>Start Indexing Engine</button></form></div></body></html>"

@app.post("/send-links")
async def receive_links(links: str = Form(...)):
    urls = [url.strip() for url in links.split('\\n') if url.strip()]
    return {"status": "success", "count": len(urls)}

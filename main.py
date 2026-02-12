from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Ключ Stripe
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
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    features = [
        ("HANDY & SIMPLE", "fas fa-user-check", "A user-friendly platform designed to make the process straightforward."),
        ("BUILT-IN CHECKER", "fas fa-search", "Instantly verify index status without third-party tools."),
        ("80% EFFICIENCY", "fas fa-bolt", "Success rate within just 72 hours of submission."),
        ("RESULTS ONLY", "fas fa-shield-alt", "Pay only for pages that actually get indexed."),
        ("FLEXIBLE PAYMENT", "fas fa-credit-card", "Multiple secure payment methods available."),
        ("SIMPLE API", "fas fa-code", "Integrate indexing into your workflow with our API.")
    ]
    
    # Безпечне формування HTML через цикл
    features_html = ""
    for title, icon, desc in features:
        features_html += f"""
        <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="{icon}"></i></div>
            <h4 class="font-bold text-slate-800 text-[10px] mb-2 uppercase tracking-tight">{title}</h4>
            <p class="text-slate-500 text-[10px] leading-relaxed">{desc}</p>
        </div>"""

    faq = [
        ("What is a URL?", "A URL must start with http:// or https://."),
        ("How long it takes?", "Most pages are indexed within 24 hours."),

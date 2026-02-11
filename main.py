from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Professional Google Indexing Service</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
        .plan-card:hover { transform: translateY(-5px); transition: all 0.3s ease; }
        details > summary { list-style: none; cursor: pointer; }
        details > summary::-webkit-details-marker { display: none; }
        details[open] summary i { transform: rotate(180deg); }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    # 1. Features Section
    features_list = [
        ("HANDY & SIMPLE", "fas fa-user-check", "A user-friendly platform designed to make the process straightforward."),
        ("BUILT-IN CHECKER", "fas fa-search", "Instantly verify if your pages are in Google’s index without third-party tools."),
        ("80% EFFICIENCY", "fas fa-bolt", "Achieve up to 80% indexing success rate within just 72 hours."),
        ("CREDITS FOR RESULTS", "fas fa-shield-alt", "Pay only for pages that actually get indexed. No wasted credits."),
        ("FLEXIBLE PAYMENT", "fas fa-credit-card", "Multiple secure payment methods to suit your preferences."),
        ("SIMPLE API", "fas fa-code", "Easily integrate indexing into your workflow with our SEO Turbo API.")
    ]
    features_html = "".join([f"""
        <div class="p-6 bg-white rounded-2xl border border-slate-100 shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="{f[1]}"></i></div>
            <h4 class="font-bold text-slate-800 text-sm mb-2 uppercase tracking-tight">{f[0]}</h4>
            <p class="text-slate-500 text-xs leading-relaxed">{f[2]}</p>
        </div>
    """ for f in features_list])

    # 2. FAQ Section
    faq_list = [
        ("What is a URL and what can be indexed?",

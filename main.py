from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Stripe Setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

HEAD = """
<head>
    <title>SEO Turbo Indexer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>.gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }</style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    # Простий конкатенований HTML, щоб уникнути SyntaxError з f-рядками
    features_html = """
    <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-20">
        <div class="p-6 bg-white rounded-2xl border shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="fas fa-bolt"></i></div>
            <h4 class="font-bold text-[10px] uppercase">80% Efficiency</h4>
            <p class="text-slate-500 text-[10px]">Indexed within 72 hours.</p>
        </div>
        <div class="p-6 bg-white rounded-2xl border shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="fas fa-shield-alt"></i></div>
            <h4 class="font-bold text-[10px] uppercase">Fair Refund</h4>
            <p class="text-slate-500 text-[10px]">Pay only for results.</p>
        </div>
        <div class="p-6 bg-white rounded-2xl border shadow-sm text-center">
            <div class="text-indigo-600 text-2xl mb-3"><i class="fas fa-user-check"></i></div>
            <h4 class="font-bold text-[10px] uppercase">Handy & Simple</h4>
            <p class="text-slate-500 text-[10px]">User-friendly platform.</p>
        </div>
    </div>
    """

    return f"""
    <html>
        {HEAD}
        <body class="bg-slate-50 font-sans text-slate-900">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl font-black mb-4 uppercase italic">SEO Turbo Indexer</h1>
                <p class="text-lg opacity-90 mb-8">Fast Google Indexing:

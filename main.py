from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Stripe Setup (Береться з налаштувань Railway)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний HEAD для всіх сторінок
HEAD = """
<head>
    <title>SEO Turbo Indexer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card:hover { transform: translateY(-5px); transition: 0.3s; }
    </style>
</head>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        {HEAD}
        <body class="bg-slate-50 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center shadow-lg">
                <h1 class="text-5xl font-black mb-4 uppercase italic tracking-tighter">SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 mb-8">Fast Google Indexing: Pay Only For Results</p>
                <a href="#prices" class="bg-white text-indigo-600 px-12 py-4 rounded-2xl font-black uppercase text-sm shadow-2xl hover:bg-slate-100 transition">Get Started</a>
            </div>

            <div class

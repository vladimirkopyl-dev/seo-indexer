from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, що ключ (sk_test або sk_live) доданий у Variables на Railway
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільний заголовок зі стилями для всіх сторінок
HEAD_CONTENT = """
<head>
    <title>SEO Turbo Indexer | Fast Google Indexing</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        @keyframes bounce-slow { 0%, 100% { transform: translateY(-5%); } 50% { transform: translateY(0); } }
        .animate-bounce-slow { animation: bounce-slow 2s infinite; }
    </style>
</head>
"""

# 1. ГОЛОВНА СТОРІНКА
@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        {HEAD_CONTENT}
        <body class="bg-slate-50 text-slate-900 font-sans">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl md:text-6xl font-extrabold mb-4">🚀 SEO Turbo Indexer</h1>
                <p class="text-xl opacity-90 max-w-2xl mx-auto">Get your pages indexed by Google in 24 hours using our high-speed API tunnel.</p>
            </div>

            <div class="max-w-4xl mx-auto -mt-10 px-4 pb-20">
                <div class="glass-card rounded-3xl shadow-2xl p-8 md:p-12 text-center border border

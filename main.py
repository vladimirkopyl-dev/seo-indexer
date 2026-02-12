from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Stripe Setup
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Константа з HEAD, щоб не повторювати
HEAD = """<head><title>SEO Turbo Indexer</title><meta name="viewport" content="width=device-width, initial-scale=1"><script src="https://cdn.tailwindcss.com"></script><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"><style>.gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }</style></head>"""

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = f"""
    <html>
        {HEAD}
        <body class="bg-slate-50 font-sans text-slate-900">
            <div class="gradient-bg text-white py-20 px-4 text-center">
                <h1 class="text-4xl font-black mb-4 uppercase italic">SEO Turbo Indexer</h1>
                <p class="text-lg opacity-90 mb-8">Fast Google Indexing: Pay Only For Results</p>
                <a href="#prices" class="bg-white text-indigo-600 px-10 py-4 rounded-xl font-black uppercase text-sm shadow-xl">Start Now</a>
            </div>
            <div class="max-w-6xl mx-auto px-4 -mt-10 pb-20">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-20 text-center">
                    <div class="p-6 bg-white rounded-2xl border shadow-sm"><i class="fas fa-bolt text-indigo-600 text-2xl mb-2"></i><h4 class="font-bold text-[10px] uppercase">80% Efficiency</h4></div>
                    <div class="p-6 bg-white rounded-2xl border shadow-sm"><i class="fas fa-shield-alt text-indigo-600 text-2xl mb-2"></i>

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
        ("What happens if a URL is not indexed?", "Your credit is

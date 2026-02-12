from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# Переконайтеся, що в налаштуваннях Railway додано змінну STRIPE_SECRET_KEY
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Спільні стилі для всього додатка
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
    # Списки переваг та FAQ
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

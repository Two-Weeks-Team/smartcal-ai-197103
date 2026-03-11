import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# Import router and DB setup (ensures tables are created)
from routes import router
from models import engine, Base

# Create tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartCal AI Backend")


@app.middleware("http")
async def normalize_api_prefix(request: Request, call_next):
    if request.scope.get("path", "").startswith("/api/"):
        request.scope["path"] = request.scope["path"][4:] or "/"
    return await call_next(request)

app.include_router(router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse, tags=["Root"])
async def root_page():
    html = """
    <html>
    <head>
        <title>SmartCal AI</title>
        <style>
            body {font-family: Arial, Helvetica, sans-serif; background:#121212; color:#e0e0e0; margin:0; padding:2rem;}
            h1 {color:#8e44ad;}
            a {color:#3498db; text-decoration:none;}
            .endpoint {margin-bottom:1rem;}
            .footer {margin-top:2rem; font-size:0.9rem; color:#777;}
        </style>
    </head>
    <body>
        <h1>SmartCal AI</h1>
        <p>Revolutionize your calorie tracking with AI‑powered personalization and smart food recognition.</p>
        <h2>Available API Endpoints</h2>
        <div class="endpoint"><strong>GET</strong> <code>/health</code> – health check</div>
        <div class="endpoint"><strong>GET</strong> <code>/items</code> – sample data items</div>
        <div class="endpoint"><strong>POST</strong> <code>/generate-meal-plan</code> – AI generated meal plan</div>
        <div class="endpoint"><strong>POST</strong> <code>/recognize-food</code> – AI food recognition from image</div>
        <h2>Tech Stack</h2>
        <ul>
            <li>FastAPI 0.115.0</li>
            <li>PostgreSQL via SQLAlchemy 2.0.35</li>
            <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
            <li>Python 3.12+</li>
        </ul>
        <p class="footer">Docs: <a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)

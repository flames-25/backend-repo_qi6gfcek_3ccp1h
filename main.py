import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Project, ContactMessage

app = FastAPI(title="Design Agency API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class APIMessage(BaseModel):
    message: str


@app.get("/", response_model=APIMessage)
async def read_root():
    return {"message": "Design Agency Backend is running"}


@app.get("/api/hello", response_model=APIMessage)
async def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
async def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    # Env echo
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ---------- Portfolio Projects ----------

SEED_PROJECTS: List[dict] = [
    {
        "title": "Neon Nexus UI Kit",
        "subtitle": "Design System",
        "description": "A modular UI system blending neon accents with brutalist structure.",
        "thumbnail": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop",
        "tags": ["UI", "Design System", "Figma"],
        "case_study_url": "https://example.com/case/neon-nexus",
        "client": "Internal",
        "featured": True,
    },
    {
        "title": "Orbit Commerce 3D",
        "subtitle": "Interactive Storefront",
        "description": "WebGL-powered product exploration with cinematic motion.",
        "thumbnail": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=1200&auto=format&fit=crop",
        "tags": ["Three.js", "WebGL", "Ecommerce"],
        "case_study_url": "https://example.com/case/orbit",
        "client": "Orbit",
        "featured": False,
    },
    {
        "title": "Astra Brand Portal",
        "subtitle": "Identity + Web",
        "description": "A dark, luminous brand portal with motion micro-interactions.",
        "thumbnail": "https://images.unsplash.com/photo-1542838686-73e3go9?ixid&auto=format&fit=crop&w=1200&q=80",
        "tags": ["Brand", "Web", "Motion"],
        "case_study_url": "https://example.com/case/astra",
        "client": "Astra",
        "featured": False,
    },
]


@app.get("/api/projects", response_model=List[Project])
async def list_projects(limit: Optional[int] = None):
    collection = "project"
    try:
        docs = get_documents(collection, {}, limit)
        if docs is not None and len(docs) == 0:
            # Seed demo data on first run for a great out-of-the-box experience
            for item in SEED_PROJECTS:
                try:
                    create_document(collection, item)
                except Exception:
                    pass
            docs = get_documents(collection, {}, limit)
        # Normalize Mongo _id to string and drop it for response schema compatibility
        cleaned = []
        for d in docs:
            d.pop("_id", None)
            cleaned.append(d)
        return cleaned
    except Exception:
        # If database is not configured, gracefully fall back to seed data
        fallback = []
        for item in SEED_PROJECTS[: limit or len(SEED_PROJECTS)]:
            fallback.append(item)
        return fallback


# ---------- Contact Messages ----------

class ContactResponse(BaseModel):
    status: str


@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact(payload: ContactMessage):
    try:
        create_document("contactmessage", payload)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

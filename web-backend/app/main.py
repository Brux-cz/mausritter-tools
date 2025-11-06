"""
Mausritter Web API - FastAPI Backend

Hlavní aplikace wrappující existující Python generátory pro web interface.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import generators

# Metadata
app = FastAPI(
    title="Mausritter API",
    description="REST API pro Mausritter generátory a campaign management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://mausritter-tools.vercel.app",
        "https://mausritter-tools-git-master-bruxs-projects.vercel.app",
        "https://*.vercel.app",  # Všechny Vercel preview URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generators.router, prefix="/api/v1/generate", tags=["generators"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint pro monitoring a deployment.
    """
    return {
        "status": "healthy",
        "service": "mausritter-api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """
    Root endpoint - redirect to docs.
    """
    return {
        "message": "Mausritter API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

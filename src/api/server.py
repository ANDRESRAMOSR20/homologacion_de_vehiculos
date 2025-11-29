from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config.settings import settings
from src.api.routers import matching_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Vehicle Matching API",
    description="API for homologating vehicle names using semantic search and LLMs.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(matching_router.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.server:app", host="0.0.0.0", port=8000, reload=True)

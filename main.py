# from Tools.scripts.patchcheck import status
from fastapi import FastAPI
from router import word_router

app = FastAPI(
    title = "Orba API",
    description = "AI-powered dictionary backend",
    version = "1.0.0"
)

app.include_router(word_router.router)

@app.get("/health")
def health_check():
    return { "status": "Orba is running"}
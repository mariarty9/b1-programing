from fastapi import FastAPI
from routes import users

app = FastAPI(
    title = "User Management API",
    description = "FastAPI backend for managing users",
    version = "1.0.0"
)

app.include_router(users.router, prefix="/users", tags = ["Users"])

@app.get("/")
def health_check():
    return{"status": "healthy", "message": "API is running"}

@app.get("/health")
def detailed_health():
    return {
        "status":  "healthy",
        "service": "User Management API",
        "version": "1.0.0"
    }
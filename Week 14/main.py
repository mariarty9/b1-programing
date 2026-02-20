from fastapi import FastAPI
from routes import users

app = FastAPI(
    title = "Week 14",
    description = "FastAPI backend with OOP UserStore class",
    version = "1.0.0"
)

app.include_router(users.router, prefix="/users", tags = ["Users"])

@app.get("/")
def health_check():
    return{"status": "healthy", "message": "Week 14 API is running"}

@app.get("/health")
def detailed_health():
    return {
        "status":  "healthy",
        "week": "14",
        "service": "User Management API with OOP",
        "version": "1.0.0"
    }
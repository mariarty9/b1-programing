from fastapi import FastAPI
from routes import users
from fastapi.staticfiles import StaticFiles 

app = FastAPI(
    title = "Week 15",
    description = "FastAPI backend with SQLite database",
    version = "1.0.0"
)

app.mount("/static", StaticFiles(directory = "static", html=True), name = "static")         # Makes fils in the 'static' folder accessible at the '/static' path; the 'html=True' argument allows it to automatically serve index.html

app.include_router(users.router, prefix="/users", tags = ["Users"])

@app.get("/")
def health_check():
    return{"status": "healthy", "message": "Week 15 API is running"}

@app.get("/health")
def detailed_health():
    return {
        "status":  "healthy",
        "week": "15",
        "service": "User Management API with SQLite",
        "version": "1.0.0"
    }
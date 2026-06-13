from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import employees, auth

# Database initialization
from app.models.database import engine, Base
Base.metadata.create_all(bind=engine)

# Import our new routes
from app.api.routes import employees

app = FastAPI(
    title="Smart Workforce Analytics API",
    description="Next-generation employment management and workplace analytics system.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the employee router to the application
app.include_router(auth.router)
app.include_router(employees.router)

@app.get("/", tags=["System Information"])
async def root():
    return {"message": "Welcome to the Smart Workforce API.", "status": "Operational"}

@app.get("/health", tags=["System Information"])
async def health_check():
    return {"status": "healthy"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, books

# Créer les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Manager API",
    description="API pour la gestion d'une bibliothèque personnelle",
    version="1.0.0"
)

# Configuration CORS
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(books.router, prefix="/books", tags=["Books"])

@app.get("/")
async def root():
    return {"message": "Book Manager API - Version 1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
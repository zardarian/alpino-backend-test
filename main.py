from fastapi import FastAPI
from src.payload.router import router as payload_router
from src.database import Base, engine
from src.config import settings

def create_app() -> FastAPI:
    # Initialize FastAPI
    app = FastAPI()

    # Include routers
    app.include_router(payload_router)

    # Create tables if not exists
    Base.metadata.create_all(bind=engine)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

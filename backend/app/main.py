from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="AI News Curator API")

app.include_router(router)


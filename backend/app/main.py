from fastapi import FastAPI

from app.core.config import settings
from app.db import Base, engine
from app.routers import auth, businesses, integrations, reviews


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(businesses.router, prefix=settings.api_prefix)
app.include_router(reviews.router, prefix=settings.api_prefix)
app.include_router(integrations.router, prefix=settings.api_prefix)


@app.get('/health')
def health_check():
    return {'status': 'ok'}

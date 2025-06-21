from fastapi import FastAPI, HTTPException, status
import logging
from routers import blog_router, user_router
from models import Base
from database import async_engine

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(blog_router.router)

app.include_router(user_router.router)

async def create_tables():

    async with async_engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

@app.on_event('startup')
async def startup():

    try:

        await create_tables()

    except Exception as e:

        logger.error(f'Error while creating tables {e}')

        raise HTTPException(status_code=500, detail='Tables not created')

@app.get('/')
async def root():

    try:

        return {'message': 'FastAPI is running'}
    
    except Exception as e:

        logger.error(f'Error in root endpoint {e}')


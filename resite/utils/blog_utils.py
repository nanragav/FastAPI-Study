from models import Blog
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy import select
from fastapi import HTTPException, status
from schemas import BlogCreateRequest, BlogGetRequest, BlogUpdateRequest, BlogDeleteRequest
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

async def create_new_blog(request: BlogCreateRequest, db: AsyncSession):

    try:

        blog = Blog(title=request.title, body=request.body)

        db.add(blog)

        await db.commit()

        await db.refresh(blog)

        return blog

    except SQLAlchemyError as se:

        logger.error(f'Error while creating a blog {se}')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail='Error while creating blog')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown Error')
    
async def get_blog_by_id(request: BlogGetRequest, db: AsyncSession):

    try:

        stmt = select(Blog).where(Blog.id == request.id)

        result = await db.execute(stmt)

        blog = result.scalar_one_or_none()

        if not blog:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
        
        return blog
    
    except SQLAlchemyError as se:

        logger.error(f'Error while getting a blog {se}')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail='Error while getting blog')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown Error')
    
async def update_blog_by_id(request: BlogUpdateRequest, db: AsyncSession):

    try:

        stmt = select(Blog).where(Blog.id == request.id)
        
        result = await db.execute(stmt)

        blog = result.scalar_one_or_none()

        if not blog:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
        
        if request.title is not None:

            blog.title = request.title

        if request.body is not None:

            blog.body = request.body

        db.add(blog)

        await db.commit()

        await db.refresh(blog)            

        return blog

    except SQLAlchemyError as se:

        logger.error(f'Error while updating a blog {se}')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail='Error while updating blog')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown Error')
    
async def delete_blog_by_id(request: BlogDeleteRequest, db: AsyncSession):

    try:

        stmt = select(Blog).where(Blog.id == request.id)

        result = await db.execute(stmt)

        blog = result.scalar_one_or_none()

        if not blog:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
        
        await db.delete(blog)

        await db.commit()

        return None
        
    except SQLAlchemyError as se:

        logger.error(f'Error while delting a blog {se}')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail='Error while deleting blog')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown Error')
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import BlogCreateRequest, BlogGetRequest, BlogGetResponse, BlogUpdateRequest, BlogDeleteRequest, BlogDeleteResponse
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from utils.blog_utils import create_new_blog, get_blog_by_id, update_blog_by_id, delete_blog_by_id
from utils.dependencies import get_current_user

logger = logging.getLogger(__name__)



router = APIRouter(tags=['Blog'])

@router.post('/create-blog', status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def create_blog(request: BlogCreateRequest, db: AsyncSession=Depends(get_db)):

    try:

        blog = await create_new_blog(request=request, db=db)

        if not blog:

            raise HTTPException(status_code=500, detail='Blog not created')

        return blog
        
    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@router.post('/get-blog', response_model=BlogGetResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def get_blog(request: BlogGetRequest, db: AsyncSession=Depends(get_db)):

    try:

        blog = await get_blog_by_id(request=request, db=db)

        if not blog:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
        
        return blog

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    

@router.put('/update-blog', status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def update_blog(request: BlogUpdateRequest, db: AsyncSession=Depends(get_db)):

    try:

        blog = await update_blog_by_id(request=request, db=db)

        if not blog:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')
        
        return blog

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@router.delete('/delete-blog', status_code=status.HTTP_200_OK, response_model=BlogDeleteResponse, dependencies=[Depends(get_current_user)])
async def delete_blog(request: BlogDeleteRequest, db: AsyncSession=Depends(get_db)):

    try:

        blog = await delete_blog_by_id(request=request, db=db)

        if not blog:

            return {'message': 'Blog deleted Successfully'}
        
        return {'message': 'Error Occured'}
    
    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas import UserCreateRequest, UserCreateResponse, UserGetRequest, UserGetResponse, UserLoginRequest, UserLoginResponse
from utils.user_utils import create_new_user, get_user_by_id, user_login
import logging
from utils.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(tags=['User'])

@router.post('/create-user', status_code=status.HTTP_201_CREATED, response_model=UserCreateResponse, dependencies=[Depends(get_current_user)])
async def create_user(request: UserCreateRequest, db: AsyncSession = Depends(get_db)):

    try:

        user = await create_new_user(request=request, db=db)

        if not user:

            raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail='User not created')
        
        return user
        
    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@router.post('/get-user', response_model=UserGetResponse, status_code=200, dependencies=[Depends(get_current_user)])
async def get_user(request: UserGetRequest, db: AsyncSession = Depends(get_db)):

    try:

        user = await get_user_by_id(request=request, db=db)

        if not user:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        return user

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
    
@router.post('/login', response_model=UserLoginResponse)
async def login(request: UserLoginRequest, db: AsyncSession = Depends(get_db)):

    try:

        token = await user_login(request=request, db=db)

        if not token:

            raise HTTPException(status_code=401, detail='Unauthorized')

        return {
            'access_token': token
        }
    
    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unhandled Error {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')
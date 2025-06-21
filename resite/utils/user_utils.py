from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreateRequest, UserGetRequest, UserLoginRequest
from models import User
from .security import get_hash, verify_password
from fastapi import HTTPException, status
import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from .auth import create_access_token


logger = logging.getLogger(__name__)


async def create_new_user(request: UserCreateRequest, db: AsyncSession):

    try:

        password = get_hash(request.password)

        user = User(name=request.name, password=password)

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user
    
    except SQLAlchemyError as se:

        logger.error(f'SQLAlshemyError while creating the user {se}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in user creation')
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Error while creating the user {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='User not created')
    
async def get_user_by_id(request: UserGetRequest, db: AsyncSession):

    try:

        stmt = select(User).where(User.id == request.id)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        return user

    except SQLAlchemyError as se:

        logger.error(f'SQLAlshemyError while getting the user {se}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in user retrival')
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Error while getting the user {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='User not retrived')
    
async def user_login(request: UserLoginRequest, db: AsyncSession):

    try:

        stmt = select(User).where(User.name == request.name)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        if not verify_password(plain_password=request.password, hashed_password=user.password):

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Username or Password is incorrect')
        
        token = await create_access_token(data={'name': user.name, 'id': user.id})

        return token

    except SQLAlchemyError as se:

        logger.error(f'SQLAlshemyError while login the user {se}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in user retrival')
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Error while login the user {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='User not loggedin')
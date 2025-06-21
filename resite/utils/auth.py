from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, UTC
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

load_dotenv()

ACCESS_TOKEN_EXPIRE = int(os.getenv('ACCESS_TOKEN_EXPIRE'))

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

ALGORITHM = os.getenv('ALGORITHM')

async def create_access_token(data: dict):

    try:

        to_encode = data.copy()

        expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

        to_encode.update({'exp': expire})

        token = jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=ALGORITHM)

        return token
    
    except JWTError as je:

        logger.error(f'Error while creating the JWT Token {je}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in token creation')
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Unknown error in token creation {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Error')
    

async def decode_access_token(token: str):

    try:

        data = jwt.decode(token=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])

        if data.get('exp') < datetime.now(UTC):

            raise HTTPException(status_code=401, detail='Expired or Malformed Token')
        
        return data
    
    except JWTError as je:

        logger.error(f'Error in Token decode {je}')

        raise HTTPException(status_code=500, detail='Token Decode Error')
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Unknown error in token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')
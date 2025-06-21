from passlib.context import CryptContext
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=['bcrypt'])

def get_hash(plain_password: str = 'password'):

    try:

        return pwd_context.hash(plain_password) 

    except Exception as e:

        logger.error(f'Error while hashing the password {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in Hashing the password')

def verify_password(plain_password: str, hashed_password: str):

    try:

        return pwd_context.verify(plain_password, hashed_password)
    
    except Exception as e:

        logger.error(f'Error while comparing the password {e}')

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error in comparing the password')





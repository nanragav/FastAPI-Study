from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from .auth import decode_access_token

import logging 

logger = logging.getLogger(__name__)

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/login')

async def get_current_user(token: str = Depends(oauth2_schema)):

    try:

        data = decode_access_token(token=token)

        return data
    
    except HTTPException as he:

        raise he
    
    except Exception as e:

        logger.error(f'Error in getting current user {e}')

        raise HTTPException(status_code=500, detail='Error while getting user details')
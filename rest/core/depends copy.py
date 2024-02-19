import os
import uuid
from contextvars import ContextVar
from typing import Optional, List, Union, Any

import requests as prequest
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from business import db_sync_session #, db_async_session
from core.logger import log

auth_schema = HTTPBearer()

zeauth_url = os.environ.get('ZEAUTH_URI')
zeauth_url = "https://auth.dev.zekoder.net"
if zeauth_url is None:
    raise ValueError("ZEAUTH_URI environment variable is not set. Please set it before running the application.")

user_session: ContextVar[str] = ContextVar('user_session', default=None)
user_roles: ContextVar[list] = ContextVar('user_roles', default=[])

async def get_async_db():
    """
    Return async engine to interact with datbase
    # async session is not supported by the current version of sqlalchemy (during mongosql integration)
    # so we are using the sync engine for now
    # this is a temporary fix
    """
    db = db_sync_session()
    try:
        # set session variables
        db.execute(f"SET zekoder.id = '{current_user_uuid()}'")
        db.execute(f"SET zekoder.roles = '{','.join(current_user_roles())}'")
        yield db
    finally:
        db.close()

    # async with db_async_session() as db:
    #     try:
    #         # set session variables
    #         await db.execute(f"SET zekoder.id = '{current_user_uuid()}'")
    #         await db.execute(f"SET zekoder.roles = '{','.join(current_user_roles())}'")

    #         yield db
    #     finally:
    #         await db.close()

def get_sync_db():
    """
    Return sync engine to interact with datbase
    """
    db = db_sync_session()
    try:
        # set session variables
        db.execute(f"SET zekoder.id = '{current_user_uuid()}'")
        db.execute(f"SET zekoder.roles = '{','.join(current_user_roles())}'")
        yield db
    finally:
        db.close()


class CommonDependencies:
    def __init__(self, page: Optional[str] = 1, size: Optional[int] = 20):
        self.page = page
        self.size = size
        self.offset = (int(page)-1) * int(size)


class Protect:
    def __init__(self, token: str = Depends(auth_schema), db: Session = Depends(get_sync_db)) -> None:
        self.credentials = token.credentials
        self.db = db

    def auth(self, method_required_roles: List[str])-> Union[None, dict]:
        """
        Authenticates the user based on the provided token and checks if the user has the required roles.

        Parameters:
        - method_required_roles (List[str]): A list of roles required to perform the action.

        Returns:
        - Union[None, dict]: The response from the authentication request.

        Raises:
        - HTTPException: Raises HTTPException with a 403 status code and an error message if authentication fails
                        or if the user is not authorized.
        """
        # return
        response = prequest.request("POST", f"{zeauth_url}/verify?token={self.credentials}", data={})
        if response.status_code != 200:
            raise HTTPException(403, "invalid token")
        print('authenticated by ZeAuth service.')
        user = response.json()
        user.update({'roles': method_required_roles})
        # user.update({'roles': ['l9pro-bbs-briefs-list']})
        # user.update({'roles': ['zekoder-new_verion-customers-get']})
        user.update({'id': str('3fa85f64-5717-4562-b3fc-2c963f66afa6')})
        # user.update({'id': str('3fa85f64-5717-4562-b3fc-2c963f66afa2')})

        request_roles = user.get('roles', [])
        # request_roles = method_required_roles
        if not any(role in request_roles for role in method_required_roles):
            raise HTTPException(403, "User not authorized to perform this action")
        
        self.set_current_user_uuid_in_contextvar(user)
        return response

    def set_current_user_uuid_in_contextvar(self, current_user: Any) -> None:
        """
        Extracts the current user information from the authentication response and sets it in context variables.

        Parameters:
        - response (Any): The response from the authentication request.

        Raises:
        - HTTPException: Raises HTTPException with a 403 status code and an error message if the user information
                         cannot be extracted or if there's an issue setting context variables.
        """
        try:
            # current_user = response.json()
            log.debug(f"current user: {current_user}")
            current_user_id = current_user.get("id")
            current_user_roles_ = current_user.get("roles", [])
            if not current_user_id:
                raise
            user_session.set(current_user_id)
            user_roles.set(current_user_roles_)
        except Exception as e:
            log.debug(e)
            raise HTTPException(403, "user not authorized to do this action")


def current_user_uuid() -> str:
    """
    get current user uuid from contextvar
    """
    log.debug(f"user_session: {user_session}")
    return user_session.get()


def current_user_roles() -> list:
    """
    get current user roles from contextvar
    """
    return user_roles.get()

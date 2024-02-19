from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_platforms_schema import *
from business.brief_platforms_model import Brief_PlatformModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_platforms_model import Brief_PlatformModel


router = APIRouter()



# list brief_platforms
@router.get('/', tags=['brief_platforms'], status_code=HTTP_200_OK, summary="List brief_platforms", response_model=ReadBrief_Platforms)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_platforms-list', 'zekoder-new_verion-brief_platforms-get'])
    try:
        obj = await Brief_PlatformModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_platform")

list.__doc__ = f" List brief_platforms".expandtabs()


# get brief_platform
@router.get('/brief_platform_id', tags=['brief_platforms'], status_code=HTTP_200_OK, summary="Get brief_platform with ID", response_model=ReadBrief_Platform)
async def get(request: Request, brief_platform_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-list', 'zekoder-new_verion-brief_platforms-get'])
    try:
        obj = await Brief_PlatformModel.objects(db)
        result = await obj.get(id=brief_platform_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_platform_id}",
                "message": f"<{brief_platform_id}> record not found in  brief_platforms"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_platform_id}>")

get.__doc__ = f" Get a specific brief_platform by its id".expandtabs()


# query brief_platforms
@router.post('/q', tags=['brief_platforms'], status_code=HTTP_200_OK, summary="Query brief_platforms: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-list', 'zekoder-new_verion-brief_platforms-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_PlatformModel)
        log.debug(q)
        allowed_aggregates = q.group
        result = jq.query(q, allowed_aggregates)
        return {
            'data': result.get("data", []),
            'aggregates': result.get("aggregates", []),
            'count': result.get("count", []),
            'page_size': size,
            'next_page': int(page) + 1
        }
    except UnkownOperator as e:
        log.debug(e)
        raise HTTPException(400, str(e))
    except ColumnNotFound as e:
        log.debug(e)
        raise HTTPException(400, str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of sessions due to unknown error")



# create brief_platform
@router.post('/', tags=['brief_platforms'], status_code=HTTP_201_CREATED, summary="Create new brief_platform", response_model=ReadBrief_Platform)
async def create(request: Request, brief_platform: CreateBrief_Platform, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-create'])

    try:
        new_data = brief_platform.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PlatformModel.objects(db)
        new_brief_platform = await obj.create(**kwargs)
        return new_brief_platform
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief platform failed")

create.__doc__ = f" Create a new brief_platform".expandtabs()


# create multiple brief_platforms
@router.post('/add-brief_platforms', tags=['brief_platforms'], status_code=HTTP_201_CREATED, summary="Create multiple brief_platforms", response_model=List[ReadBrief_Platform])
async def create_multiple_brief_platforms(request: Request, brief_platforms: List[CreateBrief_Platform], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-create'])

    new_items, errors_info = [], []
    try:
        for brief_platform_index, brief_platform in enumerate(brief_platforms):
            try:
                new_data = brief_platform.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_PlatformModel.objects(db)
                new_brief_platforms = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_platforms)
            except HTTPException as e:
                errors_info.append({"index": brief_platform_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief platforms failed")

create.__doc__ = f" Create multiple new brief_platforms".expandtabs()


# upsert multiple brief_platforms
@router.post('/upsert-multiple-brief_platforms', tags=['brief_platforms'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_platforms", response_model=List[ReadBrief_Platform])
async def upsert_multiple_brief_platforms(request: Request, brief_platforms: List[CreateBrief_Platform], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-create'])
    new_items, errors_info = [], []
    try:
        for brief_platform_index, brief_platform in enumerate(brief_platforms):
            try:
                new_data = brief_platform.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_PlatformModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_PlatformModel.objects(db)
                    updated_brief_platform = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_platforms)
                else:
                    obj = await Brief_PlatformModel.objects(db)
                    new_brief_platforms = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_platforms)
            except HTTPException as e:
                errors_info.append({"index": brief_platform_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief platforms failed")

upsert_multiple_brief_platforms.__doc__ = f" upsert multiple brief_platforms".expandtabs()


# update brief_platform
@router.put('/brief_platform_id', tags=['brief_platforms'], status_code=HTTP_201_CREATED, summary="Update brief_platform with ID")
async def update(request: Request, brief_platform_id: Union[str, int], brief_platform: UpdateBrief_Platform, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-update'])
    try:
        obj = await Brief_PlatformModel.objects(db)
        old_data = await obj.get(id=brief_platform_id)
        new_data = brief_platform.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PlatformModel.objects(db)
        result = await obj.update(obj_id=brief_platform_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_platform by its id and payload".expandtabs()


# delete brief_platform
@router.delete('/brief_platform_id', tags=['brief_platforms'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_platform with ID", response_class=Response)
async def delete(request: Request, brief_platform_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-delete'])
    try:
        obj = await Brief_PlatformModel.objects(db)
        old_data = await obj.get(id=brief_platform_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_platform_id}> record not found in brief_platforms"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PlatformModel.objects(db)
        await obj.delete(obj_id=brief_platform_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_platform by its id".expandtabs()


# delete multiple brief_platforms
@router.delete('/delete-brief_platforms', tags=['brief_platforms'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_platforms with IDs", response_class=Response)
async def delete_multiple_brief_platforms(request: Request, brief_platforms_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_platforms-delete'])
    try:
        all_old_data = Brief_PlatformModel.objects(db).get_multiple(obj_ids=brief_platforms_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_platforms_id}> record not found in brief_platforms"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PlatformModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_platforms_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_platforms_id <{brief_platforms_id}>")

delete.__doc__ = f" Delete multiple brief_platforms by list of ids".expandtabs()
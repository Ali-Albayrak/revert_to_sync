from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_audiences_schema import *
from business.brief_audiences_model import Brief_AudienceModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_audiences_model import Brief_AudienceModel


router = APIRouter()



# list brief_audiences
@router.get('/', tags=['brief_audiences'], status_code=HTTP_200_OK, summary="List brief_audiences", response_model=ReadBrief_Audiences)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_audiences-list', 'zekoder-new_verion-brief_audiences-get'])
    try:
        obj = await Brief_AudienceModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_audience")

list.__doc__ = f" List brief_audiences".expandtabs()


# get brief_audience
@router.get('/brief_audience_id', tags=['brief_audiences'], status_code=HTTP_200_OK, summary="Get brief_audience with ID", response_model=ReadBrief_Audience)
async def get(request: Request, brief_audience_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-list', 'zekoder-new_verion-brief_audiences-get'])
    try:
        obj = await Brief_AudienceModel.objects(db)
        result = await obj.get(id=brief_audience_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_audience_id}",
                "message": f"<{brief_audience_id}> record not found in  brief_audiences"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_audience_id}>")

get.__doc__ = f" Get a specific brief_audience by its id".expandtabs()


# query brief_audiences
@router.post('/q', tags=['brief_audiences'], status_code=HTTP_200_OK, summary="Query brief_audiences: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-list', 'zekoder-new_verion-brief_audiences-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_AudienceModel)
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



# create brief_audience
@router.post('/', tags=['brief_audiences'], status_code=HTTP_201_CREATED, summary="Create new brief_audience", response_model=ReadBrief_Audience)
async def create(request: Request, brief_audience: CreateBrief_Audience, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-create'])

    try:
        new_data = brief_audience.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_AudienceModel.objects(db)
        new_brief_audience = await obj.create(**kwargs)
        return new_brief_audience
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief audience failed")

create.__doc__ = f" Create a new brief_audience".expandtabs()


# create multiple brief_audiences
@router.post('/add-brief_audiences', tags=['brief_audiences'], status_code=HTTP_201_CREATED, summary="Create multiple brief_audiences", response_model=List[ReadBrief_Audience])
async def create_multiple_brief_audiences(request: Request, brief_audiences: List[CreateBrief_Audience], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-create'])

    new_items, errors_info = [], []
    try:
        for brief_audience_index, brief_audience in enumerate(brief_audiences):
            try:
                new_data = brief_audience.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_AudienceModel.objects(db)
                new_brief_audiences = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_audiences)
            except HTTPException as e:
                errors_info.append({"index": brief_audience_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief audiences failed")

create.__doc__ = f" Create multiple new brief_audiences".expandtabs()


# upsert multiple brief_audiences
@router.post('/upsert-multiple-brief_audiences', tags=['brief_audiences'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_audiences", response_model=List[ReadBrief_Audience])
async def upsert_multiple_brief_audiences(request: Request, brief_audiences: List[CreateBrief_Audience], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-create'])
    new_items, errors_info = [], []
    try:
        for brief_audience_index, brief_audience in enumerate(brief_audiences):
            try:
                new_data = brief_audience.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_AudienceModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_AudienceModel.objects(db)
                    updated_brief_audience = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_audiences)
                else:
                    obj = await Brief_AudienceModel.objects(db)
                    new_brief_audiences = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_audiences)
            except HTTPException as e:
                errors_info.append({"index": brief_audience_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief audiences failed")

upsert_multiple_brief_audiences.__doc__ = f" upsert multiple brief_audiences".expandtabs()


# update brief_audience
@router.put('/brief_audience_id', tags=['brief_audiences'], status_code=HTTP_201_CREATED, summary="Update brief_audience with ID")
async def update(request: Request, brief_audience_id: Union[str, int], brief_audience: UpdateBrief_Audience, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-update'])
    try:
        obj = await Brief_AudienceModel.objects(db)
        old_data = await obj.get(id=brief_audience_id)
        new_data = brief_audience.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_AudienceModel.objects(db)
        result = await obj.update(obj_id=brief_audience_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_audience by its id and payload".expandtabs()


# delete brief_audience
@router.delete('/brief_audience_id', tags=['brief_audiences'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_audience with ID", response_class=Response)
async def delete(request: Request, brief_audience_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-delete'])
    try:
        obj = await Brief_AudienceModel.objects(db)
        old_data = await obj.get(id=brief_audience_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_audience_id}> record not found in brief_audiences"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_AudienceModel.objects(db)
        await obj.delete(obj_id=brief_audience_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_audience by its id".expandtabs()


# delete multiple brief_audiences
@router.delete('/delete-brief_audiences', tags=['brief_audiences'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_audiences with IDs", response_class=Response)
async def delete_multiple_brief_audiences(request: Request, brief_audiences_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_audiences-delete'])
    try:
        all_old_data = Brief_AudienceModel.objects(db).get_multiple(obj_ids=brief_audiences_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_audiences_id}> record not found in brief_audiences"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_AudienceModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_audiences_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_audiences_id <{brief_audiences_id}>")

delete.__doc__ = f" Delete multiple brief_audiences by list of ids".expandtabs()
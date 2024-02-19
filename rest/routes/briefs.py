from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.briefs_schema import *
from business.briefs_model import BriefModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.briefs_model import BriefModel


router = APIRouter()



# list briefs
@router.get('/', tags=['briefs'], status_code=HTTP_200_OK, summary="List briefs", response_model=ReadBriefs)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-briefs-list', 'zekoder-new_verion-briefs-get'])
    try:
        obj = await BriefModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief")

list.__doc__ = f" List briefs".expandtabs()


# get brief
@router.get('/brief_id', tags=['briefs'], status_code=HTTP_200_OK, summary="Get brief with ID", response_model=ReadBrief)
async def get(request: Request, brief_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-list', 'zekoder-new_verion-briefs-get'])
    try:
        obj = await BriefModel.objects(db)
        result = await obj.get(id=brief_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_id}",
                "message": f"<{brief_id}> record not found in  briefs"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_id}>")

get.__doc__ = f" Get a specific brief by its id".expandtabs()


# query briefs
@router.post('/q', tags=['briefs'], status_code=HTTP_200_OK, summary="Query briefs: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-list', 'zekoder-new_verion-briefs-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, BriefModel)
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



# create brief
@router.post('/', tags=['briefs'], status_code=HTTP_201_CREATED, summary="Create new brief", response_model=ReadBrief)
async def create(request: Request, brief: CreateBrief, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-create'])

    try:
        new_data = brief.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await BriefModel.objects(db)
        new_brief = await obj.create(**kwargs)
        return new_brief
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief failed")

create.__doc__ = f" Create a new brief".expandtabs()


# create multiple briefs
@router.post('/add-briefs', tags=['briefs'], status_code=HTTP_201_CREATED, summary="Create multiple briefs", response_model=List[ReadBrief])
async def create_multiple_briefs(request: Request, briefs: List[CreateBrief], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-create'])

    new_items, errors_info = [], []
    try:
        for brief_index, brief in enumerate(briefs):
            try:
                new_data = brief.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await BriefModel.objects(db)
                new_briefs = await obj.create(only_add=True, **kwargs)
                new_items.append(new_briefs)
            except HTTPException as e:
                errors_info.append({"index": brief_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new briefs failed")

create.__doc__ = f" Create multiple new briefs".expandtabs()


# upsert multiple briefs
@router.post('/upsert-multiple-briefs', tags=['briefs'], status_code=HTTP_201_CREATED, summary="Upsert multiple briefs", response_model=List[ReadBrief])
async def upsert_multiple_briefs(request: Request, briefs: List[CreateBrief], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-create'])
    new_items, errors_info = [], []
    try:
        for brief_index, brief in enumerate(briefs):
            try:
                new_data = brief.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await BriefModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await BriefModel.objects(db)
                    updated_brief = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_briefs)
                else:
                    obj = await BriefModel.objects(db)
                    new_briefs = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_briefs)
            except HTTPException as e:
                errors_info.append({"index": brief_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple briefs failed")

upsert_multiple_briefs.__doc__ = f" upsert multiple briefs".expandtabs()


# update brief
@router.put('/brief_id', tags=['briefs'], status_code=HTTP_201_CREATED, summary="Update brief with ID")
async def update(request: Request, brief_id: Union[str, int], brief: UpdateBrief, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-update'])
    try:
        obj = await BriefModel.objects(db)
        old_data = await obj.get(id=brief_id)
        new_data = brief.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await BriefModel.objects(db)
        result = await obj.update(obj_id=brief_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief by its id and payload".expandtabs()


# delete brief
@router.delete('/brief_id', tags=['briefs'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief with ID", response_class=Response)
async def delete(request: Request, brief_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-delete'])
    try:
        obj = await BriefModel.objects(db)
        old_data = await obj.get(id=brief_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_id}> record not found in briefs"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await BriefModel.objects(db)
        await obj.delete(obj_id=brief_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief by its id".expandtabs()


# delete multiple briefs
@router.delete('/delete-briefs', tags=['briefs'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple briefs with IDs", response_class=Response)
async def delete_multiple_briefs(request: Request, briefs_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-briefs-delete'])
    try:
        all_old_data = BriefModel.objects(db).get_multiple(obj_ids=briefs_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{briefs_id}> record not found in briefs"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await BriefModel.objects(db)
        await obj.delete_multiple(obj_ids=briefs_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting briefs_id <{briefs_id}>")

delete.__doc__ = f" Delete multiple briefs by list of ids".expandtabs()
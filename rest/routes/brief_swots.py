from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_swots_schema import *
from business.brief_swots_model import Brief_SwotModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_swots_model import Brief_SwotModel


router = APIRouter()



# list brief_swots
@router.get('/', tags=['brief_swots'], status_code=HTTP_200_OK, summary="List brief_swots", response_model=ReadBrief_Swots)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_swots-list', 'zekoder-new_verion-brief_swots-get'])
    try:
        obj = await Brief_SwotModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_swot")

list.__doc__ = f" List brief_swots".expandtabs()


# get brief_swot
@router.get('/brief_swot_id', tags=['brief_swots'], status_code=HTTP_200_OK, summary="Get brief_swot with ID", response_model=ReadBrief_Swot)
async def get(request: Request, brief_swot_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-list', 'zekoder-new_verion-brief_swots-get'])
    try:
        obj = await Brief_SwotModel.objects(db)
        result = await obj.get(id=brief_swot_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_swot_id}",
                "message": f"<{brief_swot_id}> record not found in  brief_swots"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_swot_id}>")

get.__doc__ = f" Get a specific brief_swot by its id".expandtabs()


# query brief_swots
@router.post('/q', tags=['brief_swots'], status_code=HTTP_200_OK, summary="Query brief_swots: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-list', 'zekoder-new_verion-brief_swots-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_SwotModel)
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



# create brief_swot
@router.post('/', tags=['brief_swots'], status_code=HTTP_201_CREATED, summary="Create new brief_swot", response_model=ReadBrief_Swot)
async def create(request: Request, brief_swot: CreateBrief_Swot, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-create'])

    try:
        new_data = brief_swot.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_SwotModel.objects(db)
        new_brief_swot = await obj.create(**kwargs)
        return new_brief_swot
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief swot failed")

create.__doc__ = f" Create a new brief_swot".expandtabs()


# create multiple brief_swots
@router.post('/add-brief_swots', tags=['brief_swots'], status_code=HTTP_201_CREATED, summary="Create multiple brief_swots", response_model=List[ReadBrief_Swot])
async def create_multiple_brief_swots(request: Request, brief_swots: List[CreateBrief_Swot], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-create'])

    new_items, errors_info = [], []
    try:
        for brief_swot_index, brief_swot in enumerate(brief_swots):
            try:
                new_data = brief_swot.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_SwotModel.objects(db)
                new_brief_swots = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_swots)
            except HTTPException as e:
                errors_info.append({"index": brief_swot_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief swots failed")

create.__doc__ = f" Create multiple new brief_swots".expandtabs()


# upsert multiple brief_swots
@router.post('/upsert-multiple-brief_swots', tags=['brief_swots'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_swots", response_model=List[ReadBrief_Swot])
async def upsert_multiple_brief_swots(request: Request, brief_swots: List[CreateBrief_Swot], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-create'])
    new_items, errors_info = [], []
    try:
        for brief_swot_index, brief_swot in enumerate(brief_swots):
            try:
                new_data = brief_swot.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_SwotModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_SwotModel.objects(db)
                    updated_brief_swot = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_swots)
                else:
                    obj = await Brief_SwotModel.objects(db)
                    new_brief_swots = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_swots)
            except HTTPException as e:
                errors_info.append({"index": brief_swot_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief swots failed")

upsert_multiple_brief_swots.__doc__ = f" upsert multiple brief_swots".expandtabs()


# update brief_swot
@router.put('/brief_swot_id', tags=['brief_swots'], status_code=HTTP_201_CREATED, summary="Update brief_swot with ID")
async def update(request: Request, brief_swot_id: Union[str, int], brief_swot: UpdateBrief_Swot, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-update'])
    try:
        obj = await Brief_SwotModel.objects(db)
        old_data = await obj.get(id=brief_swot_id)
        new_data = brief_swot.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_SwotModel.objects(db)
        result = await obj.update(obj_id=brief_swot_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_swot by its id and payload".expandtabs()


# delete brief_swot
@router.delete('/brief_swot_id', tags=['brief_swots'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_swot with ID", response_class=Response)
async def delete(request: Request, brief_swot_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-delete'])
    try:
        obj = await Brief_SwotModel.objects(db)
        old_data = await obj.get(id=brief_swot_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_swot_id}> record not found in brief_swots"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_SwotModel.objects(db)
        await obj.delete(obj_id=brief_swot_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_swot by its id".expandtabs()


# delete multiple brief_swots
@router.delete('/delete-brief_swots', tags=['brief_swots'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_swots with IDs", response_class=Response)
async def delete_multiple_brief_swots(request: Request, brief_swots_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_swots-delete'])
    try:
        all_old_data = Brief_SwotModel.objects(db).get_multiple(obj_ids=brief_swots_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_swots_id}> record not found in brief_swots"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_SwotModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_swots_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_swots_id <{brief_swots_id}>")

delete.__doc__ = f" Delete multiple brief_swots by list of ids".expandtabs()
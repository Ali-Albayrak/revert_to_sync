from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_extras_schema import *
from business.brief_extras_model import Brief_ExtraModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_extras_model import Brief_ExtraModel


router = APIRouter()



# list brief_extras
@router.get('/', tags=['brief_extras'], status_code=HTTP_200_OK, summary="List brief_extras", response_model=ReadBrief_Extras)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_extras-list', 'zekoder-new_verion-brief_extras-get'])
    try:
        obj = await Brief_ExtraModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_extra")

list.__doc__ = f" List brief_extras".expandtabs()


# get brief_extra
@router.get('/brief_extra_id', tags=['brief_extras'], status_code=HTTP_200_OK, summary="Get brief_extra with ID", response_model=ReadBrief_Extra)
async def get(request: Request, brief_extra_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-list', 'zekoder-new_verion-brief_extras-get'])
    try:
        obj = await Brief_ExtraModel.objects(db)
        result = await obj.get(id=brief_extra_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_extra_id}",
                "message": f"<{brief_extra_id}> record not found in  brief_extras"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_extra_id}>")

get.__doc__ = f" Get a specific brief_extra by its id".expandtabs()


# query brief_extras
@router.post('/q', tags=['brief_extras'], status_code=HTTP_200_OK, summary="Query brief_extras: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-list', 'zekoder-new_verion-brief_extras-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_ExtraModel)
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



# create brief_extra
@router.post('/', tags=['brief_extras'], status_code=HTTP_201_CREATED, summary="Create new brief_extra", response_model=ReadBrief_Extra)
async def create(request: Request, brief_extra: CreateBrief_Extra, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-create'])

    try:
        new_data = brief_extra.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ExtraModel.objects(db)
        new_brief_extra = await obj.create(**kwargs)
        return new_brief_extra
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief extra failed")

create.__doc__ = f" Create a new brief_extra".expandtabs()


# create multiple brief_extras
@router.post('/add-brief_extras', tags=['brief_extras'], status_code=HTTP_201_CREATED, summary="Create multiple brief_extras", response_model=List[ReadBrief_Extra])
async def create_multiple_brief_extras(request: Request, brief_extras: List[CreateBrief_Extra], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-create'])

    new_items, errors_info = [], []
    try:
        for brief_extra_index, brief_extra in enumerate(brief_extras):
            try:
                new_data = brief_extra.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ExtraModel.objects(db)
                new_brief_extras = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_extras)
            except HTTPException as e:
                errors_info.append({"index": brief_extra_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief extras failed")

create.__doc__ = f" Create multiple new brief_extras".expandtabs()


# upsert multiple brief_extras
@router.post('/upsert-multiple-brief_extras', tags=['brief_extras'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_extras", response_model=List[ReadBrief_Extra])
async def upsert_multiple_brief_extras(request: Request, brief_extras: List[CreateBrief_Extra], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-create'])
    new_items, errors_info = [], []
    try:
        for brief_extra_index, brief_extra in enumerate(brief_extras):
            try:
                new_data = brief_extra.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ExtraModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_ExtraModel.objects(db)
                    updated_brief_extra = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_extras)
                else:
                    obj = await Brief_ExtraModel.objects(db)
                    new_brief_extras = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_extras)
            except HTTPException as e:
                errors_info.append({"index": brief_extra_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief extras failed")

upsert_multiple_brief_extras.__doc__ = f" upsert multiple brief_extras".expandtabs()


# update brief_extra
@router.put('/brief_extra_id', tags=['brief_extras'], status_code=HTTP_201_CREATED, summary="Update brief_extra with ID")
async def update(request: Request, brief_extra_id: Union[str, int], brief_extra: UpdateBrief_Extra, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-update'])
    try:
        obj = await Brief_ExtraModel.objects(db)
        old_data = await obj.get(id=brief_extra_id)
        new_data = brief_extra.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ExtraModel.objects(db)
        result = await obj.update(obj_id=brief_extra_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_extra by its id and payload".expandtabs()


# delete brief_extra
@router.delete('/brief_extra_id', tags=['brief_extras'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_extra with ID", response_class=Response)
async def delete(request: Request, brief_extra_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-delete'])
    try:
        obj = await Brief_ExtraModel.objects(db)
        old_data = await obj.get(id=brief_extra_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_extra_id}> record not found in brief_extras"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ExtraModel.objects(db)
        await obj.delete(obj_id=brief_extra_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_extra by its id".expandtabs()


# delete multiple brief_extras
@router.delete('/delete-brief_extras', tags=['brief_extras'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_extras with IDs", response_class=Response)
async def delete_multiple_brief_extras(request: Request, brief_extras_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_extras-delete'])
    try:
        all_old_data = Brief_ExtraModel.objects(db).get_multiple(obj_ids=brief_extras_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_extras_id}> record not found in brief_extras"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ExtraModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_extras_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_extras_id <{brief_extras_id}>")

delete.__doc__ = f" Delete multiple brief_extras by list of ids".expandtabs()
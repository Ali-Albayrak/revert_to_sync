from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_marketings_schema import *
from business.brief_marketings_model import Brief_MarketingModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_marketings_model import Brief_MarketingModel


router = APIRouter()



# list brief_marketings
@router.get('/', tags=['brief_marketings'], status_code=HTTP_200_OK, summary="List brief_marketings", response_model=ReadBrief_Marketings)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_marketings-list', 'zekoder-new_verion-brief_marketings-get'])
    try:
        obj = await Brief_MarketingModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_marketing")

list.__doc__ = f" List brief_marketings".expandtabs()


# get brief_marketing
@router.get('/brief_marketing_id', tags=['brief_marketings'], status_code=HTTP_200_OK, summary="Get brief_marketing with ID", response_model=ReadBrief_Marketing)
async def get(request: Request, brief_marketing_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-list', 'zekoder-new_verion-brief_marketings-get'])
    try:
        obj = await Brief_MarketingModel.objects(db)
        result = await obj.get(id=brief_marketing_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_marketing_id}",
                "message": f"<{brief_marketing_id}> record not found in  brief_marketings"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_marketing_id}>")

get.__doc__ = f" Get a specific brief_marketing by its id".expandtabs()


# query brief_marketings
@router.post('/q', tags=['brief_marketings'], status_code=HTTP_200_OK, summary="Query brief_marketings: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-list', 'zekoder-new_verion-brief_marketings-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_MarketingModel)
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



# create brief_marketing
@router.post('/', tags=['brief_marketings'], status_code=HTTP_201_CREATED, summary="Create new brief_marketing", response_model=ReadBrief_Marketing)
async def create(request: Request, brief_marketing: CreateBrief_Marketing, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-create'])

    try:
        new_data = brief_marketing.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_MarketingModel.objects(db)
        new_brief_marketing = await obj.create(**kwargs)
        return new_brief_marketing
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief marketing failed")

create.__doc__ = f" Create a new brief_marketing".expandtabs()


# create multiple brief_marketings
@router.post('/add-brief_marketings', tags=['brief_marketings'], status_code=HTTP_201_CREATED, summary="Create multiple brief_marketings", response_model=List[ReadBrief_Marketing])
async def create_multiple_brief_marketings(request: Request, brief_marketings: List[CreateBrief_Marketing], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-create'])

    new_items, errors_info = [], []
    try:
        for brief_marketing_index, brief_marketing in enumerate(brief_marketings):
            try:
                new_data = brief_marketing.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_MarketingModel.objects(db)
                new_brief_marketings = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_marketings)
            except HTTPException as e:
                errors_info.append({"index": brief_marketing_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief marketings failed")

create.__doc__ = f" Create multiple new brief_marketings".expandtabs()


# upsert multiple brief_marketings
@router.post('/upsert-multiple-brief_marketings', tags=['brief_marketings'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_marketings", response_model=List[ReadBrief_Marketing])
async def upsert_multiple_brief_marketings(request: Request, brief_marketings: List[CreateBrief_Marketing], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-create'])
    new_items, errors_info = [], []
    try:
        for brief_marketing_index, brief_marketing in enumerate(brief_marketings):
            try:
                new_data = brief_marketing.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_MarketingModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_MarketingModel.objects(db)
                    updated_brief_marketing = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_marketings)
                else:
                    obj = await Brief_MarketingModel.objects(db)
                    new_brief_marketings = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_marketings)
            except HTTPException as e:
                errors_info.append({"index": brief_marketing_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief marketings failed")

upsert_multiple_brief_marketings.__doc__ = f" upsert multiple brief_marketings".expandtabs()


# update brief_marketing
@router.put('/brief_marketing_id', tags=['brief_marketings'], status_code=HTTP_201_CREATED, summary="Update brief_marketing with ID")
async def update(request: Request, brief_marketing_id: Union[str, int], brief_marketing: UpdateBrief_Marketing, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-update'])
    try:
        obj = await Brief_MarketingModel.objects(db)
        old_data = await obj.get(id=brief_marketing_id)
        new_data = brief_marketing.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_MarketingModel.objects(db)
        result = await obj.update(obj_id=brief_marketing_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_marketing by its id and payload".expandtabs()


# delete brief_marketing
@router.delete('/brief_marketing_id', tags=['brief_marketings'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_marketing with ID", response_class=Response)
async def delete(request: Request, brief_marketing_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-delete'])
    try:
        obj = await Brief_MarketingModel.objects(db)
        old_data = await obj.get(id=brief_marketing_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_marketing_id}> record not found in brief_marketings"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_MarketingModel.objects(db)
        await obj.delete(obj_id=brief_marketing_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_marketing by its id".expandtabs()


# delete multiple brief_marketings
@router.delete('/delete-brief_marketings', tags=['brief_marketings'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_marketings with IDs", response_class=Response)
async def delete_multiple_brief_marketings(request: Request, brief_marketings_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_marketings-delete'])
    try:
        all_old_data = Brief_MarketingModel.objects(db).get_multiple(obj_ids=brief_marketings_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_marketings_id}> record not found in brief_marketings"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_MarketingModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_marketings_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_marketings_id <{brief_marketings_id}>")

delete.__doc__ = f" Delete multiple brief_marketings by list of ids".expandtabs()
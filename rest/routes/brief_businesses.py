from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_businesses_schema import *
from business.brief_businesses_model import Brief_BusinessModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_businesses_model import Brief_BusinessModel


router = APIRouter()



# list brief_businesses
@router.get('/', tags=['brief_businesses'], status_code=HTTP_200_OK, summary="List brief_businesses", response_model=ReadBrief_Businesses)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_businesses-list', 'zekoder-new_verion-brief_businesses-get'])
    try:
        obj = await Brief_BusinessModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_business")

list.__doc__ = f" List brief_businesses".expandtabs()


# get brief_business
@router.get('/brief_business_id', tags=['brief_businesses'], status_code=HTTP_200_OK, summary="Get brief_business with ID", response_model=ReadBrief_Business)
async def get(request: Request, brief_business_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-list', 'zekoder-new_verion-brief_businesses-get'])
    try:
        obj = await Brief_BusinessModel.objects(db)
        result = await obj.get(id=brief_business_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_business_id}",
                "message": f"<{brief_business_id}> record not found in  brief_businesses"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_business_id}>")

get.__doc__ = f" Get a specific brief_business by its id".expandtabs()


# query brief_businesses
@router.post('/q', tags=['brief_businesses'], status_code=HTTP_200_OK, summary="Query brief_businesses: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-list', 'zekoder-new_verion-brief_businesses-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_BusinessModel)
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



# create brief_business
@router.post('/', tags=['brief_businesses'], status_code=HTTP_201_CREATED, summary="Create new brief_business", response_model=ReadBrief_Business)
async def create(request: Request, brief_business: CreateBrief_Business, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-create'])

    try:
        new_data = brief_business.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_BusinessModel.objects(db)
        new_brief_business = await obj.create(**kwargs)
        return new_brief_business
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief business failed")

create.__doc__ = f" Create a new brief_business".expandtabs()


# create multiple brief_businesses
@router.post('/add-brief_businesses', tags=['brief_businesses'], status_code=HTTP_201_CREATED, summary="Create multiple brief_businesses", response_model=List[ReadBrief_Business])
async def create_multiple_brief_businesses(request: Request, brief_businesses: List[CreateBrief_Business], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-create'])

    new_items, errors_info = [], []
    try:
        for brief_business_index, brief_business in enumerate(brief_businesses):
            try:
                new_data = brief_business.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_BusinessModel.objects(db)
                new_brief_businesses = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_businesses)
            except HTTPException as e:
                errors_info.append({"index": brief_business_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief businesses failed")

create.__doc__ = f" Create multiple new brief_businesses".expandtabs()


# upsert multiple brief_businesses
@router.post('/upsert-multiple-brief_businesses', tags=['brief_businesses'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_businesses", response_model=List[ReadBrief_Business])
async def upsert_multiple_brief_businesses(request: Request, brief_businesses: List[CreateBrief_Business], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-create'])
    new_items, errors_info = [], []
    try:
        for brief_business_index, brief_business in enumerate(brief_businesses):
            try:
                new_data = brief_business.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_BusinessModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_BusinessModel.objects(db)
                    updated_brief_business = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_businesses)
                else:
                    obj = await Brief_BusinessModel.objects(db)
                    new_brief_businesses = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_businesses)
            except HTTPException as e:
                errors_info.append({"index": brief_business_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief businesses failed")

upsert_multiple_brief_businesses.__doc__ = f" upsert multiple brief_businesses".expandtabs()


# update brief_business
@router.put('/brief_business_id', tags=['brief_businesses'], status_code=HTTP_201_CREATED, summary="Update brief_business with ID")
async def update(request: Request, brief_business_id: Union[str, int], brief_business: UpdateBrief_Business, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-update'])
    try:
        obj = await Brief_BusinessModel.objects(db)
        old_data = await obj.get(id=brief_business_id)
        new_data = brief_business.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_BusinessModel.objects(db)
        result = await obj.update(obj_id=brief_business_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_business by its id and payload".expandtabs()


# delete brief_business
@router.delete('/brief_business_id', tags=['brief_businesses'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_business with ID", response_class=Response)
async def delete(request: Request, brief_business_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-delete'])
    try:
        obj = await Brief_BusinessModel.objects(db)
        old_data = await obj.get(id=brief_business_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_business_id}> record not found in brief_businesses"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_BusinessModel.objects(db)
        await obj.delete(obj_id=brief_business_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_business by its id".expandtabs()


# delete multiple brief_businesses
@router.delete('/delete-brief_businesses', tags=['brief_businesses'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_businesses with IDs", response_class=Response)
async def delete_multiple_brief_businesses(request: Request, brief_businesses_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_businesses-delete'])
    try:
        all_old_data = Brief_BusinessModel.objects(db).get_multiple(obj_ids=brief_businesses_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_businesses_id}> record not found in brief_businesses"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_BusinessModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_businesses_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_businesses_id <{brief_businesses_id}>")

delete.__doc__ = f" Delete multiple brief_businesses by list of ids".expandtabs()
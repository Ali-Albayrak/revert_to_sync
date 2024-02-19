from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategy_audiences_schema import *
from business.strategy_audiences_model import Strategy_AudienceModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.strategy_audiences_model import Strategy_AudienceModel


router = APIRouter()



# list strategy_audiences
@router.get('/', tags=['strategy_audiences'], status_code=HTTP_200_OK, summary="List strategy_audiences", response_model=ReadStrategy_Audiences)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategy_audiences-list', 'zekoder-new_verion-strategy_audiences-get'])
    try:
        obj = await Strategy_AudienceModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy_audience")

list.__doc__ = f" List strategy_audiences".expandtabs()


# get strategy_audience
@router.get('/strategy_audience_id', tags=['strategy_audiences'], status_code=HTTP_200_OK, summary="Get strategy_audience with ID", response_model=ReadStrategy_Audience)
async def get(request: Request, strategy_audience_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-list', 'zekoder-new_verion-strategy_audiences-get'])
    try:
        obj = await Strategy_AudienceModel.objects(db)
        result = await obj.get(id=strategy_audience_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_audience_id}",
                "message": f"<{strategy_audience_id}> record not found in  strategy_audiences"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_audience_id}>")

get.__doc__ = f" Get a specific strategy_audience by its id".expandtabs()


# query strategy_audiences
@router.post('/q', tags=['strategy_audiences'], status_code=HTTP_200_OK, summary="Query strategy_audiences: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-list', 'zekoder-new_verion-strategy_audiences-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Strategy_AudienceModel)
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



# create strategy_audience
@router.post('/', tags=['strategy_audiences'], status_code=HTTP_201_CREATED, summary="Create new strategy_audience", response_model=ReadStrategy_Audience)
async def create(request: Request, strategy_audience: CreateStrategy_Audience, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-create'])

    try:
        new_data = strategy_audience.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_AudienceModel.objects(db)
        new_strategy_audience = await obj.create(**kwargs)
        return new_strategy_audience
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy audience failed")

create.__doc__ = f" Create a new strategy_audience".expandtabs()


# create multiple strategy_audiences
@router.post('/add-strategy_audiences', tags=['strategy_audiences'], status_code=HTTP_201_CREATED, summary="Create multiple strategy_audiences", response_model=List[ReadStrategy_Audience])
async def create_multiple_strategy_audiences(request: Request, strategy_audiences: List[CreateStrategy_Audience], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-create'])

    new_items, errors_info = [], []
    try:
        for strategy_audience_index, strategy_audience in enumerate(strategy_audiences):
            try:
                new_data = strategy_audience.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_AudienceModel.objects(db)
                new_strategy_audiences = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategy_audiences)
            except HTTPException as e:
                errors_info.append({"index": strategy_audience_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy audiences failed")

create.__doc__ = f" Create multiple new strategy_audiences".expandtabs()


# upsert multiple strategy_audiences
@router.post('/upsert-multiple-strategy_audiences', tags=['strategy_audiences'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategy_audiences", response_model=List[ReadStrategy_Audience])
async def upsert_multiple_strategy_audiences(request: Request, strategy_audiences: List[CreateStrategy_Audience], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-create'])
    new_items, errors_info = [], []
    try:
        for strategy_audience_index, strategy_audience in enumerate(strategy_audiences):
            try:
                new_data = strategy_audience.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_AudienceModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Strategy_AudienceModel.objects(db)
                    updated_strategy_audience = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategy_audiences)
                else:
                    obj = await Strategy_AudienceModel.objects(db)
                    new_strategy_audiences = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategy_audiences)
            except HTTPException as e:
                errors_info.append({"index": strategy_audience_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategy audiences failed")

upsert_multiple_strategy_audiences.__doc__ = f" upsert multiple strategy_audiences".expandtabs()


# update strategy_audience
@router.put('/strategy_audience_id', tags=['strategy_audiences'], status_code=HTTP_201_CREATED, summary="Update strategy_audience with ID")
async def update(request: Request, strategy_audience_id: Union[str, int], strategy_audience: UpdateStrategy_Audience, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-update'])
    try:
        obj = await Strategy_AudienceModel.objects(db)
        old_data = await obj.get(id=strategy_audience_id)
        new_data = strategy_audience.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_AudienceModel.objects(db)
        result = await obj.update(obj_id=strategy_audience_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy_audience by its id and payload".expandtabs()


# delete strategy_audience
@router.delete('/strategy_audience_id', tags=['strategy_audiences'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy_audience with ID", response_class=Response)
async def delete(request: Request, strategy_audience_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-delete'])
    try:
        obj = await Strategy_AudienceModel.objects(db)
        old_data = await obj.get(id=strategy_audience_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_audience_id}> record not found in strategy_audiences"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_AudienceModel.objects(db)
        await obj.delete(obj_id=strategy_audience_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy_audience by its id".expandtabs()


# delete multiple strategy_audiences
@router.delete('/delete-strategy_audiences', tags=['strategy_audiences'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategy_audiences with IDs", response_class=Response)
async def delete_multiple_strategy_audiences(request: Request, strategy_audiences_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_audiences-delete'])
    try:
        all_old_data = Strategy_AudienceModel.objects(db).get_multiple(obj_ids=strategy_audiences_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategy_audiences_id}> record not found in strategy_audiences"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_AudienceModel.objects(db)
        await obj.delete_multiple(obj_ids=strategy_audiences_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategy_audiences_id <{strategy_audiences_id}>")

delete.__doc__ = f" Delete multiple strategy_audiences by list of ids".expandtabs()
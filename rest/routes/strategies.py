from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategies_schema import *
from business.strategies_model import StrategyModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.strategies_model import StrategyModel


router = APIRouter()



# list strategies
@router.get('/', tags=['strategies'], status_code=HTTP_200_OK, summary="List strategies", response_model=ReadStrategies)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategies-list', 'zekoder-new_verion-strategies-get'])
    try:
        obj = await StrategyModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy")

list.__doc__ = f" List strategies".expandtabs()


# get strategy
@router.get('/strategy_id', tags=['strategies'], status_code=HTTP_200_OK, summary="Get strategy with ID", response_model=ReadStrategy)
async def get(request: Request, strategy_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-list', 'zekoder-new_verion-strategies-get'])
    try:
        obj = await StrategyModel.objects(db)
        result = await obj.get(id=strategy_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_id}",
                "message": f"<{strategy_id}> record not found in  strategies"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_id}>")

get.__doc__ = f" Get a specific strategy by its id".expandtabs()


# query strategies
@router.post('/q', tags=['strategies'], status_code=HTTP_200_OK, summary="Query strategies: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-list', 'zekoder-new_verion-strategies-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, StrategyModel)
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



# create strategy
@router.post('/', tags=['strategies'], status_code=HTTP_201_CREATED, summary="Create new strategy", response_model=ReadStrategy)
async def create(request: Request, strategy: CreateStrategy, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-create'])

    try:
        new_data = strategy.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await StrategyModel.objects(db)
        new_strategy = await obj.create(**kwargs)
        return new_strategy
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy failed")

create.__doc__ = f" Create a new strategy".expandtabs()


# create multiple strategies
@router.post('/add-strategies', tags=['strategies'], status_code=HTTP_201_CREATED, summary="Create multiple strategies", response_model=List[ReadStrategy])
async def create_multiple_strategies(request: Request, strategies: List[CreateStrategy], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-create'])

    new_items, errors_info = [], []
    try:
        for strategy_index, strategy in enumerate(strategies):
            try:
                new_data = strategy.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await StrategyModel.objects(db)
                new_strategies = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategies)
            except HTTPException as e:
                errors_info.append({"index": strategy_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategies failed")

create.__doc__ = f" Create multiple new strategies".expandtabs()


# upsert multiple strategies
@router.post('/upsert-multiple-strategies', tags=['strategies'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategies", response_model=List[ReadStrategy])
async def upsert_multiple_strategies(request: Request, strategies: List[CreateStrategy], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-create'])
    new_items, errors_info = [], []
    try:
        for strategy_index, strategy in enumerate(strategies):
            try:
                new_data = strategy.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await StrategyModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await StrategyModel.objects(db)
                    updated_strategy = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategies)
                else:
                    obj = await StrategyModel.objects(db)
                    new_strategies = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategies)
            except HTTPException as e:
                errors_info.append({"index": strategy_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategies failed")

upsert_multiple_strategies.__doc__ = f" upsert multiple strategies".expandtabs()


# update strategy
@router.put('/strategy_id', tags=['strategies'], status_code=HTTP_201_CREATED, summary="Update strategy with ID")
async def update(request: Request, strategy_id: Union[str, int], strategy: UpdateStrategy, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-update'])
    try:
        obj = await StrategyModel.objects(db)
        old_data = await obj.get(id=strategy_id)
        new_data = strategy.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await StrategyModel.objects(db)
        result = await obj.update(obj_id=strategy_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy by its id and payload".expandtabs()


# delete strategy
@router.delete('/strategy_id', tags=['strategies'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy with ID", response_class=Response)
async def delete(request: Request, strategy_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-delete'])
    try:
        obj = await StrategyModel.objects(db)
        old_data = await obj.get(id=strategy_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_id}> record not found in strategies"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await StrategyModel.objects(db)
        await obj.delete(obj_id=strategy_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy by its id".expandtabs()


# delete multiple strategies
@router.delete('/delete-strategies', tags=['strategies'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategies with IDs", response_class=Response)
async def delete_multiple_strategies(request: Request, strategies_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategies-delete'])
    try:
        all_old_data = StrategyModel.objects(db).get_multiple(obj_ids=strategies_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategies_id}> record not found in strategies"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await StrategyModel.objects(db)
        await obj.delete_multiple(obj_ids=strategies_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategies_id <{strategies_id}>")

delete.__doc__ = f" Delete multiple strategies by list of ids".expandtabs()
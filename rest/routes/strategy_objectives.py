from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategy_objectives_schema import *
from business.strategy_objectives_model import Strategy_ObjectiveModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.strategy_objectives_model import Strategy_ObjectiveModel


router = APIRouter()



# list strategy_objectives
@router.get('/', tags=['strategy_objectives'], status_code=HTTP_200_OK, summary="List strategy_objectives", response_model=ReadStrategy_Objectives)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategy_objectives-list', 'zekoder-new_verion-strategy_objectives-get'])
    try:
        obj = await Strategy_ObjectiveModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy_objective")

list.__doc__ = f" List strategy_objectives".expandtabs()


# get strategy_objective
@router.get('/strategy_objective_id', tags=['strategy_objectives'], status_code=HTTP_200_OK, summary="Get strategy_objective with ID", response_model=ReadStrategy_Objective)
async def get(request: Request, strategy_objective_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-list', 'zekoder-new_verion-strategy_objectives-get'])
    try:
        obj = await Strategy_ObjectiveModel.objects(db)
        result = await obj.get(id=strategy_objective_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_objective_id}",
                "message": f"<{strategy_objective_id}> record not found in  strategy_objectives"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_objective_id}>")

get.__doc__ = f" Get a specific strategy_objective by its id".expandtabs()


# query strategy_objectives
@router.post('/q', tags=['strategy_objectives'], status_code=HTTP_200_OK, summary="Query strategy_objectives: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-list', 'zekoder-new_verion-strategy_objectives-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Strategy_ObjectiveModel)
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



# create strategy_objective
@router.post('/', tags=['strategy_objectives'], status_code=HTTP_201_CREATED, summary="Create new strategy_objective", response_model=ReadStrategy_Objective)
async def create(request: Request, strategy_objective: CreateStrategy_Objective, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-create'])

    try:
        new_data = strategy_objective.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ObjectiveModel.objects(db)
        new_strategy_objective = await obj.create(**kwargs)
        return new_strategy_objective
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy objective failed")

create.__doc__ = f" Create a new strategy_objective".expandtabs()


# create multiple strategy_objectives
@router.post('/add-strategy_objectives', tags=['strategy_objectives'], status_code=HTTP_201_CREATED, summary="Create multiple strategy_objectives", response_model=List[ReadStrategy_Objective])
async def create_multiple_strategy_objectives(request: Request, strategy_objectives: List[CreateStrategy_Objective], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-create'])

    new_items, errors_info = [], []
    try:
        for strategy_objective_index, strategy_objective in enumerate(strategy_objectives):
            try:
                new_data = strategy_objective.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_ObjectiveModel.objects(db)
                new_strategy_objectives = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategy_objectives)
            except HTTPException as e:
                errors_info.append({"index": strategy_objective_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy objectives failed")

create.__doc__ = f" Create multiple new strategy_objectives".expandtabs()


# upsert multiple strategy_objectives
@router.post('/upsert-multiple-strategy_objectives', tags=['strategy_objectives'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategy_objectives", response_model=List[ReadStrategy_Objective])
async def upsert_multiple_strategy_objectives(request: Request, strategy_objectives: List[CreateStrategy_Objective], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-create'])
    new_items, errors_info = [], []
    try:
        for strategy_objective_index, strategy_objective in enumerate(strategy_objectives):
            try:
                new_data = strategy_objective.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_ObjectiveModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Strategy_ObjectiveModel.objects(db)
                    updated_strategy_objective = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategy_objectives)
                else:
                    obj = await Strategy_ObjectiveModel.objects(db)
                    new_strategy_objectives = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategy_objectives)
            except HTTPException as e:
                errors_info.append({"index": strategy_objective_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategy objectives failed")

upsert_multiple_strategy_objectives.__doc__ = f" upsert multiple strategy_objectives".expandtabs()


# update strategy_objective
@router.put('/strategy_objective_id', tags=['strategy_objectives'], status_code=HTTP_201_CREATED, summary="Update strategy_objective with ID")
async def update(request: Request, strategy_objective_id: Union[str, int], strategy_objective: UpdateStrategy_Objective, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-update'])
    try:
        obj = await Strategy_ObjectiveModel.objects(db)
        old_data = await obj.get(id=strategy_objective_id)
        new_data = strategy_objective.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ObjectiveModel.objects(db)
        result = await obj.update(obj_id=strategy_objective_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy_objective by its id and payload".expandtabs()


# delete strategy_objective
@router.delete('/strategy_objective_id', tags=['strategy_objectives'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy_objective with ID", response_class=Response)
async def delete(request: Request, strategy_objective_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-delete'])
    try:
        obj = await Strategy_ObjectiveModel.objects(db)
        old_data = await obj.get(id=strategy_objective_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_objective_id}> record not found in strategy_objectives"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ObjectiveModel.objects(db)
        await obj.delete(obj_id=strategy_objective_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy_objective by its id".expandtabs()


# delete multiple strategy_objectives
@router.delete('/delete-strategy_objectives', tags=['strategy_objectives'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategy_objectives with IDs", response_class=Response)
async def delete_multiple_strategy_objectives(request: Request, strategy_objectives_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_objectives-delete'])
    try:
        all_old_data = Strategy_ObjectiveModel.objects(db).get_multiple(obj_ids=strategy_objectives_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategy_objectives_id}> record not found in strategy_objectives"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ObjectiveModel.objects(db)
        await obj.delete_multiple(obj_ids=strategy_objectives_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategy_objectives_id <{strategy_objectives_id}>")

delete.__doc__ = f" Delete multiple strategy_objectives by list of ids".expandtabs()
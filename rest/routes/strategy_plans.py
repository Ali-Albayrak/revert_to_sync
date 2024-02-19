from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategy_plans_schema import *
from business.strategy_plans_model import Strategy_PlanModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.strategy_plans_model import Strategy_PlanModel


router = APIRouter()



# list strategy_plans
@router.get('/', tags=['strategy_plans'], status_code=HTTP_200_OK, summary="List strategy_plans", response_model=ReadStrategy_Plans)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategy_plans-list', 'zekoder-new_verion-strategy_plans-get'])
    try:
        obj = await Strategy_PlanModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy_plan")

list.__doc__ = f" List strategy_plans".expandtabs()


# get strategy_plan
@router.get('/strategy_plan_id', tags=['strategy_plans'], status_code=HTTP_200_OK, summary="Get strategy_plan with ID", response_model=ReadStrategy_Plan)
async def get(request: Request, strategy_plan_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-list', 'zekoder-new_verion-strategy_plans-get'])
    try:
        obj = await Strategy_PlanModel.objects(db)
        result = await obj.get(id=strategy_plan_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_plan_id}",
                "message": f"<{strategy_plan_id}> record not found in  strategy_plans"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_plan_id}>")

get.__doc__ = f" Get a specific strategy_plan by its id".expandtabs()


# query strategy_plans
@router.post('/q', tags=['strategy_plans'], status_code=HTTP_200_OK, summary="Query strategy_plans: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-list', 'zekoder-new_verion-strategy_plans-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Strategy_PlanModel)
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



# create strategy_plan
@router.post('/', tags=['strategy_plans'], status_code=HTTP_201_CREATED, summary="Create new strategy_plan", response_model=ReadStrategy_Plan)
async def create(request: Request, strategy_plan: CreateStrategy_Plan, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-create'])

    try:
        new_data = strategy_plan.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PlanModel.objects(db)
        new_strategy_plan = await obj.create(**kwargs)
        return new_strategy_plan
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy plan failed")

create.__doc__ = f" Create a new strategy_plan".expandtabs()


# create multiple strategy_plans
@router.post('/add-strategy_plans', tags=['strategy_plans'], status_code=HTTP_201_CREATED, summary="Create multiple strategy_plans", response_model=List[ReadStrategy_Plan])
async def create_multiple_strategy_plans(request: Request, strategy_plans: List[CreateStrategy_Plan], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-create'])

    new_items, errors_info = [], []
    try:
        for strategy_plan_index, strategy_plan in enumerate(strategy_plans):
            try:
                new_data = strategy_plan.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_PlanModel.objects(db)
                new_strategy_plans = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategy_plans)
            except HTTPException as e:
                errors_info.append({"index": strategy_plan_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy plans failed")

create.__doc__ = f" Create multiple new strategy_plans".expandtabs()


# upsert multiple strategy_plans
@router.post('/upsert-multiple-strategy_plans', tags=['strategy_plans'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategy_plans", response_model=List[ReadStrategy_Plan])
async def upsert_multiple_strategy_plans(request: Request, strategy_plans: List[CreateStrategy_Plan], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-create'])
    new_items, errors_info = [], []
    try:
        for strategy_plan_index, strategy_plan in enumerate(strategy_plans):
            try:
                new_data = strategy_plan.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_PlanModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Strategy_PlanModel.objects(db)
                    updated_strategy_plan = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategy_plans)
                else:
                    obj = await Strategy_PlanModel.objects(db)
                    new_strategy_plans = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategy_plans)
            except HTTPException as e:
                errors_info.append({"index": strategy_plan_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategy plans failed")

upsert_multiple_strategy_plans.__doc__ = f" upsert multiple strategy_plans".expandtabs()


# update strategy_plan
@router.put('/strategy_plan_id', tags=['strategy_plans'], status_code=HTTP_201_CREATED, summary="Update strategy_plan with ID")
async def update(request: Request, strategy_plan_id: Union[str, int], strategy_plan: UpdateStrategy_Plan, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-update'])
    try:
        obj = await Strategy_PlanModel.objects(db)
        old_data = await obj.get(id=strategy_plan_id)
        new_data = strategy_plan.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PlanModel.objects(db)
        result = await obj.update(obj_id=strategy_plan_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy_plan by its id and payload".expandtabs()


# delete strategy_plan
@router.delete('/strategy_plan_id', tags=['strategy_plans'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy_plan with ID", response_class=Response)
async def delete(request: Request, strategy_plan_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-delete'])
    try:
        obj = await Strategy_PlanModel.objects(db)
        old_data = await obj.get(id=strategy_plan_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_plan_id}> record not found in strategy_plans"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PlanModel.objects(db)
        await obj.delete(obj_id=strategy_plan_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy_plan by its id".expandtabs()


# delete multiple strategy_plans
@router.delete('/delete-strategy_plans', tags=['strategy_plans'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategy_plans with IDs", response_class=Response)
async def delete_multiple_strategy_plans(request: Request, strategy_plans_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_plans-delete'])
    try:
        all_old_data = Strategy_PlanModel.objects(db).get_multiple(obj_ids=strategy_plans_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategy_plans_id}> record not found in strategy_plans"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PlanModel.objects(db)
        await obj.delete_multiple(obj_ids=strategy_plans_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategy_plans_id <{strategy_plans_id}>")

delete.__doc__ = f" Delete multiple strategy_plans by list of ids".expandtabs()
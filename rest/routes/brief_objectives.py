from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_objectives_schema import *
from business.brief_objectives_model import Brief_ObjectiveModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_objectives_model import Brief_ObjectiveModel


router = APIRouter()



# list brief_objectives
@router.get('/', tags=['brief_objectives'], status_code=HTTP_200_OK, summary="List brief_objectives", response_model=ReadBrief_Objectives)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_objectives-list', 'zekoder-new_verion-brief_objectives-get'])
    try:
        obj = await Brief_ObjectiveModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_objective")

list.__doc__ = f" List brief_objectives".expandtabs()


# get brief_objective
@router.get('/brief_objective_id', tags=['brief_objectives'], status_code=HTTP_200_OK, summary="Get brief_objective with ID", response_model=ReadBrief_Objective)
async def get(request: Request, brief_objective_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-list', 'zekoder-new_verion-brief_objectives-get'])
    try:
        obj = await Brief_ObjectiveModel.objects(db)
        result = await obj.get(id=brief_objective_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_objective_id}",
                "message": f"<{brief_objective_id}> record not found in  brief_objectives"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_objective_id}>")

get.__doc__ = f" Get a specific brief_objective by its id".expandtabs()


# query brief_objectives
@router.post('/q', tags=['brief_objectives'], status_code=HTTP_200_OK, summary="Query brief_objectives: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-list', 'zekoder-new_verion-brief_objectives-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_ObjectiveModel)
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



# create brief_objective
@router.post('/', tags=['brief_objectives'], status_code=HTTP_201_CREATED, summary="Create new brief_objective", response_model=ReadBrief_Objective)
async def create(request: Request, brief_objective: CreateBrief_Objective, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-create'])

    try:
        new_data = brief_objective.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ObjectiveModel.objects(db)
        new_brief_objective = await obj.create(**kwargs)
        return new_brief_objective
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief objective failed")

create.__doc__ = f" Create a new brief_objective".expandtabs()


# create multiple brief_objectives
@router.post('/add-brief_objectives', tags=['brief_objectives'], status_code=HTTP_201_CREATED, summary="Create multiple brief_objectives", response_model=List[ReadBrief_Objective])
async def create_multiple_brief_objectives(request: Request, brief_objectives: List[CreateBrief_Objective], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-create'])

    new_items, errors_info = [], []
    try:
        for brief_objective_index, brief_objective in enumerate(brief_objectives):
            try:
                new_data = brief_objective.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ObjectiveModel.objects(db)
                new_brief_objectives = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_objectives)
            except HTTPException as e:
                errors_info.append({"index": brief_objective_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief objectives failed")

create.__doc__ = f" Create multiple new brief_objectives".expandtabs()


# upsert multiple brief_objectives
@router.post('/upsert-multiple-brief_objectives', tags=['brief_objectives'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_objectives", response_model=List[ReadBrief_Objective])
async def upsert_multiple_brief_objectives(request: Request, brief_objectives: List[CreateBrief_Objective], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-create'])
    new_items, errors_info = [], []
    try:
        for brief_objective_index, brief_objective in enumerate(brief_objectives):
            try:
                new_data = brief_objective.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ObjectiveModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_ObjectiveModel.objects(db)
                    updated_brief_objective = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_objectives)
                else:
                    obj = await Brief_ObjectiveModel.objects(db)
                    new_brief_objectives = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_objectives)
            except HTTPException as e:
                errors_info.append({"index": brief_objective_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief objectives failed")

upsert_multiple_brief_objectives.__doc__ = f" upsert multiple brief_objectives".expandtabs()


# update brief_objective
@router.put('/brief_objective_id', tags=['brief_objectives'], status_code=HTTP_201_CREATED, summary="Update brief_objective with ID")
async def update(request: Request, brief_objective_id: Union[str, int], brief_objective: UpdateBrief_Objective, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-update'])
    try:
        obj = await Brief_ObjectiveModel.objects(db)
        old_data = await obj.get(id=brief_objective_id)
        new_data = brief_objective.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ObjectiveModel.objects(db)
        result = await obj.update(obj_id=brief_objective_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_objective by its id and payload".expandtabs()


# delete brief_objective
@router.delete('/brief_objective_id', tags=['brief_objectives'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_objective with ID", response_class=Response)
async def delete(request: Request, brief_objective_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-delete'])
    try:
        obj = await Brief_ObjectiveModel.objects(db)
        old_data = await obj.get(id=brief_objective_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_objective_id}> record not found in brief_objectives"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ObjectiveModel.objects(db)
        await obj.delete(obj_id=brief_objective_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_objective by its id".expandtabs()


# delete multiple brief_objectives
@router.delete('/delete-brief_objectives', tags=['brief_objectives'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_objectives with IDs", response_class=Response)
async def delete_multiple_brief_objectives(request: Request, brief_objectives_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_objectives-delete'])
    try:
        all_old_data = Brief_ObjectiveModel.objects(db).get_multiple(obj_ids=brief_objectives_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_objectives_id}> record not found in brief_objectives"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ObjectiveModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_objectives_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_objectives_id <{brief_objectives_id}>")

delete.__doc__ = f" Delete multiple brief_objectives by list of ids".expandtabs()
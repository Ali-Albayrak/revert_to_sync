from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategy_personas_schema import *
from business.strategy_personas_model import Strategy_PersonaModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.strategy_personas_model import Strategy_PersonaModel


router = APIRouter()



# list strategy_personas
@router.get('/', tags=['strategy_personas'], status_code=HTTP_200_OK, summary="List strategy_personas", response_model=ReadStrategy_Personas)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategy_personas-list', 'zekoder-new_verion-strategy_personas-get'])
    try:
        obj = await Strategy_PersonaModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy_persona")

list.__doc__ = f" List strategy_personas".expandtabs()


# get strategy_persona
@router.get('/strategy_persona_id', tags=['strategy_personas'], status_code=HTTP_200_OK, summary="Get strategy_persona with ID", response_model=ReadStrategy_Persona)
async def get(request: Request, strategy_persona_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-list', 'zekoder-new_verion-strategy_personas-get'])
    try:
        obj = await Strategy_PersonaModel.objects(db)
        result = await obj.get(id=strategy_persona_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_persona_id}",
                "message": f"<{strategy_persona_id}> record not found in  strategy_personas"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_persona_id}>")

get.__doc__ = f" Get a specific strategy_persona by its id".expandtabs()


# query strategy_personas
@router.post('/q', tags=['strategy_personas'], status_code=HTTP_200_OK, summary="Query strategy_personas: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-list', 'zekoder-new_verion-strategy_personas-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Strategy_PersonaModel)
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



# create strategy_persona
@router.post('/', tags=['strategy_personas'], status_code=HTTP_201_CREATED, summary="Create new strategy_persona", response_model=ReadStrategy_Persona)
async def create(request: Request, strategy_persona: CreateStrategy_Persona, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-create'])

    try:
        new_data = strategy_persona.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PersonaModel.objects(db)
        new_strategy_persona = await obj.create(**kwargs)
        return new_strategy_persona
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy persona failed")

create.__doc__ = f" Create a new strategy_persona".expandtabs()


# create multiple strategy_personas
@router.post('/add-strategy_personas', tags=['strategy_personas'], status_code=HTTP_201_CREATED, summary="Create multiple strategy_personas", response_model=List[ReadStrategy_Persona])
async def create_multiple_strategy_personas(request: Request, strategy_personas: List[CreateStrategy_Persona], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-create'])

    new_items, errors_info = [], []
    try:
        for strategy_persona_index, strategy_persona in enumerate(strategy_personas):
            try:
                new_data = strategy_persona.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_PersonaModel.objects(db)
                new_strategy_personas = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategy_personas)
            except HTTPException as e:
                errors_info.append({"index": strategy_persona_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy personas failed")

create.__doc__ = f" Create multiple new strategy_personas".expandtabs()


# upsert multiple strategy_personas
@router.post('/upsert-multiple-strategy_personas', tags=['strategy_personas'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategy_personas", response_model=List[ReadStrategy_Persona])
async def upsert_multiple_strategy_personas(request: Request, strategy_personas: List[CreateStrategy_Persona], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-create'])
    new_items, errors_info = [], []
    try:
        for strategy_persona_index, strategy_persona in enumerate(strategy_personas):
            try:
                new_data = strategy_persona.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_PersonaModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Strategy_PersonaModel.objects(db)
                    updated_strategy_persona = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategy_personas)
                else:
                    obj = await Strategy_PersonaModel.objects(db)
                    new_strategy_personas = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategy_personas)
            except HTTPException as e:
                errors_info.append({"index": strategy_persona_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategy personas failed")

upsert_multiple_strategy_personas.__doc__ = f" upsert multiple strategy_personas".expandtabs()


# update strategy_persona
@router.put('/strategy_persona_id', tags=['strategy_personas'], status_code=HTTP_201_CREATED, summary="Update strategy_persona with ID")
async def update(request: Request, strategy_persona_id: Union[str, int], strategy_persona: UpdateStrategy_Persona, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-update'])
    try:
        obj = await Strategy_PersonaModel.objects(db)
        old_data = await obj.get(id=strategy_persona_id)
        new_data = strategy_persona.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PersonaModel.objects(db)
        result = await obj.update(obj_id=strategy_persona_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy_persona by its id and payload".expandtabs()


# delete strategy_persona
@router.delete('/strategy_persona_id', tags=['strategy_personas'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy_persona with ID", response_class=Response)
async def delete(request: Request, strategy_persona_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-delete'])
    try:
        obj = await Strategy_PersonaModel.objects(db)
        old_data = await obj.get(id=strategy_persona_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_persona_id}> record not found in strategy_personas"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PersonaModel.objects(db)
        await obj.delete(obj_id=strategy_persona_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy_persona by its id".expandtabs()


# delete multiple strategy_personas
@router.delete('/delete-strategy_personas', tags=['strategy_personas'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategy_personas with IDs", response_class=Response)
async def delete_multiple_strategy_personas(request: Request, strategy_personas_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_personas-delete'])
    try:
        all_old_data = Strategy_PersonaModel.objects(db).get_multiple(obj_ids=strategy_personas_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategy_personas_id}> record not found in strategy_personas"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_PersonaModel.objects(db)
        await obj.delete_multiple(obj_ids=strategy_personas_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategy_personas_id <{strategy_personas_id}>")

delete.__doc__ = f" Delete multiple strategy_personas by list of ids".expandtabs()
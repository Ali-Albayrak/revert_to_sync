from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_personas_schema import *
from business.brief_personas_model import Brief_PersonaModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_personas_model import Brief_PersonaModel


router = APIRouter()



# list brief_personas
@router.get('/', tags=['brief_personas'], status_code=HTTP_200_OK, summary="List brief_personas", response_model=ReadBrief_Personas)
async def list(request: Request, token: str = Depends(Protect), db: Session = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_personas-list', 'zekoder-new_verion-brief_personas-get'])
    try:
        obj = await Brief_PersonaModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_persona")

list.__doc__ = f" List brief_personas".expandtabs()


# get brief_persona
@router.get('/brief_persona_id', tags=['brief_personas'], status_code=HTTP_200_OK, summary="Get brief_persona with ID", response_model=ReadBrief_Persona)
async def get(request: Request, brief_persona_id: str, db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-list', 'zekoder-new_verion-brief_personas-get'])
    try:
        obj = await Brief_PersonaModel.objects(db)
        result = await obj.get(id=brief_persona_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_persona_id}",
                "message": f"<{brief_persona_id}> record not found in  brief_personas"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_persona_id}>")

get.__doc__ = f" Get a specific brief_persona by its id".expandtabs()


# query brief_personas
@router.post('/q', tags=['brief_personas'], status_code=HTTP_200_OK, summary="Query brief_personas: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-list', 'zekoder-new_verion-brief_personas-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_PersonaModel)
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



# create brief_persona
@router.post('/', tags=['brief_personas'], status_code=HTTP_201_CREATED, summary="Create new brief_persona", response_model=ReadBrief_Persona)
async def create(request: Request, brief_persona: CreateBrief_Persona, db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-create'])

    try:
        new_data = brief_persona.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PersonaModel.objects(db)
        new_brief_persona = await obj.create(**kwargs)
        return new_brief_persona
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief persona failed")

create.__doc__ = f" Create a new brief_persona".expandtabs()


# create multiple brief_personas
@router.post('/add-brief_personas', tags=['brief_personas'], status_code=HTTP_201_CREATED, summary="Create multiple brief_personas", response_model=List[ReadBrief_Persona])
async def create_multiple_brief_personas(request: Request, brief_personas: List[CreateBrief_Persona], db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-create'])

    new_items, errors_info = [], []
    try:
        for brief_persona_index, brief_persona in enumerate(brief_personas):
            try:
                new_data = brief_persona.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_PersonaModel.objects(db)
                new_brief_personas = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_personas)
            except HTTPException as e:
                errors_info.append({"index": brief_persona_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief personas failed")

create.__doc__ = f" Create multiple new brief_personas".expandtabs()


# upsert multiple brief_personas
@router.post('/upsert-multiple-brief_personas', tags=['brief_personas'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_personas", response_model=List[ReadBrief_Persona])
async def upsert_multiple_brief_personas(request: Request, brief_personas: List[CreateBrief_Persona], db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-create'])
    new_items, errors_info = [], []
    try:
        for brief_persona_index, brief_persona in enumerate(brief_personas):
            try:
                new_data = brief_persona.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_PersonaModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_PersonaModel.objects(db)
                    await obj.update(obj_id=new_data['id'], **kwargs)
                    updated_brief_personas = await obj.get(id=new_data['id'])
                    new_items.append(updated_brief_personas)
                else:
                    obj = await Brief_PersonaModel.objects(db)
                    new_brief_personas = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_personas)
            except HTTPException as e:
                errors_info.append({"index": brief_persona_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief personas failed")

upsert_multiple_brief_personas.__doc__ = f" upsert multiple brief_personas".expandtabs()


# update brief_persona
@router.put('/brief_persona_id', tags=['brief_personas'], status_code=HTTP_201_CREATED, summary="Update brief_persona with ID")
async def update(request: Request, brief_persona_id: Union[str, int], brief_persona: UpdateBrief_Persona, db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-update'])
    try:
        obj = await Brief_PersonaModel.objects(db)
        old_data = await obj.get(id=brief_persona_id)
        new_data = brief_persona.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PersonaModel.objects(db)
        await obj.update(obj_id=brief_persona_id, **kwargs)
        result = await obj.get(id=brief_persona_id)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_persona by its id and payload".expandtabs()


# delete brief_persona
@router.delete('/brief_persona_id', tags=['brief_personas'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_persona with ID", response_class=Response)
async def delete(request: Request, brief_persona_id: Union[str, int], db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-delete'])
    try:
        obj = await Brief_PersonaModel.objects(db)
        old_data = await obj.get(id=brief_persona_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_persona_id}> record not found in brief_personas"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PersonaModel.objects(db)
        await obj.delete(obj_id=brief_persona_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_persona by its id".expandtabs()


# delete multiple brief_personas
@router.delete('/delete-brief_personas', tags=['brief_personas'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_personas with IDs", response_class=Response)
async def delete_multiple_brief_personas(request: Request, brief_personas_id: List[str] = QueryParam(), db: Session = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_personas-delete'])
    try:
        obj = await Brief_PersonaModel.objects(db)
        all_old_data = await obj.get_multiple(obj_ids=brief_personas_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_personas_id}> record not found in brief_personas"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_PersonaModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_personas_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_personas_id <{brief_personas_id}>")

delete.__doc__ = f" Delete multiple brief_personas by list of ids".expandtabs()
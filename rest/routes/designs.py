from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.designs_schema import *
from business.designs_model import DesignModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.designs_model import DesignModel


router = APIRouter()



# list designs
@router.get('/', tags=['designs'], status_code=HTTP_200_OK, summary="List designs", response_model=ReadDesigns)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-designs-list', 'zekoder-new_verion-designs-get'])
    try:
        obj = await DesignModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of design")

list.__doc__ = f" List designs".expandtabs()


# get design
@router.get('/design_id', tags=['designs'], status_code=HTTP_200_OK, summary="Get design with ID", response_model=ReadDesign)
async def get(request: Request, design_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-list', 'zekoder-new_verion-designs-get'])
    try:
        obj = await DesignModel.objects(db)
        result = await obj.get(id=design_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{design_id}",
                "message": f"<{design_id}> record not found in  designs"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{design_id}>")

get.__doc__ = f" Get a specific design by its id".expandtabs()


# query designs
@router.post('/q', tags=['designs'], status_code=HTTP_200_OK, summary="Query designs: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-list', 'zekoder-new_verion-designs-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, DesignModel)
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



# create design
@router.post('/', tags=['designs'], status_code=HTTP_201_CREATED, summary="Create new design", response_model=ReadDesign)
async def create(request: Request, design: CreateDesign, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-create'])

    try:
        new_data = design.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await DesignModel.objects(db)
        new_design = await obj.create(**kwargs)
        return new_design
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new design failed")

create.__doc__ = f" Create a new design".expandtabs()


# create multiple designs
@router.post('/add-designs', tags=['designs'], status_code=HTTP_201_CREATED, summary="Create multiple designs", response_model=List[ReadDesign])
async def create_multiple_designs(request: Request, designs: List[CreateDesign], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-create'])

    new_items, errors_info = [], []
    try:
        for design_index, design in enumerate(designs):
            try:
                new_data = design.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await DesignModel.objects(db)
                new_designs = await obj.create(only_add=True, **kwargs)
                new_items.append(new_designs)
            except HTTPException as e:
                errors_info.append({"index": design_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new designs failed")

create.__doc__ = f" Create multiple new designs".expandtabs()


# upsert multiple designs
@router.post('/upsert-multiple-designs', tags=['designs'], status_code=HTTP_201_CREATED, summary="Upsert multiple designs", response_model=List[ReadDesign])
async def upsert_multiple_designs(request: Request, designs: List[CreateDesign], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-create'])
    new_items, errors_info = [], []
    try:
        for design_index, design in enumerate(designs):
            try:
                new_data = design.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await DesignModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await DesignModel.objects(db)
                    updated_design = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_designs)
                else:
                    obj = await DesignModel.objects(db)
                    new_designs = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_designs)
            except HTTPException as e:
                errors_info.append({"index": design_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple designs failed")

upsert_multiple_designs.__doc__ = f" upsert multiple designs".expandtabs()


# update design
@router.put('/design_id', tags=['designs'], status_code=HTTP_201_CREATED, summary="Update design with ID")
async def update(request: Request, design_id: Union[str, int], design: UpdateDesign, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-update'])
    try:
        obj = await DesignModel.objects(db)
        old_data = await obj.get(id=design_id)
        new_data = design.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await DesignModel.objects(db)
        result = await obj.update(obj_id=design_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a design by its id and payload".expandtabs()


# delete design
@router.delete('/design_id', tags=['designs'], status_code=HTTP_204_NO_CONTENT, summary="Delete design with ID", response_class=Response)
async def delete(request: Request, design_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-delete'])
    try:
        obj = await DesignModel.objects(db)
        old_data = await obj.get(id=design_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{design_id}> record not found in designs"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await DesignModel.objects(db)
        await obj.delete(obj_id=design_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a design by its id".expandtabs()


# delete multiple designs
@router.delete('/delete-designs', tags=['designs'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple designs with IDs", response_class=Response)
async def delete_multiple_designs(request: Request, designs_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-designs-delete'])
    try:
        all_old_data = DesignModel.objects(db).get_multiple(obj_ids=designs_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{designs_id}> record not found in designs"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await DesignModel.objects(db)
        await obj.delete_multiple(obj_ids=designs_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting designs_id <{designs_id}>")

delete.__doc__ = f" Delete multiple designs by list of ids".expandtabs()
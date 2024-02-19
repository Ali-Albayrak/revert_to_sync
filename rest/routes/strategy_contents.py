from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.strategy_contents_schema import *
from business.strategy_contents_model import Strategy_ContentModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *
from actions import content_ready
from business.strategy_contents_model import Strategy_ContentModel


router = APIRouter()



# list strategy_contents
@router.get('/', tags=['strategy_contents'], status_code=HTTP_200_OK, summary="List strategy_contents", response_model=ReadStrategy_Contents)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-strategy_contents-list', 'zekoder-new_verion-strategy_contents-get'])
    try:
        obj = await Strategy_ContentModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of strategy_content")

list.__doc__ = f" List strategy_contents".expandtabs()


# get strategy_content
@router.get('/strategy_content_id', tags=['strategy_contents'], status_code=HTTP_200_OK, summary="Get strategy_content with ID", response_model=ReadStrategy_Content)
async def get(request: Request, strategy_content_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-list', 'zekoder-new_verion-strategy_contents-get'])
    try:
        obj = await Strategy_ContentModel.objects(db)
        result = await obj.get(id=strategy_content_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{strategy_content_id}",
                "message": f"<{strategy_content_id}> record not found in  strategy_contents"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{strategy_content_id}>")

get.__doc__ = f" Get a specific strategy_content by its id".expandtabs()


# query strategy_contents
@router.post('/q', tags=['strategy_contents'], status_code=HTTP_200_OK, summary="Query strategy_contents: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-list', 'zekoder-new_verion-strategy_contents-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Strategy_ContentModel)
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



# create strategy_content
@router.post('/', tags=['strategy_contents'], status_code=HTTP_201_CREATED, summary="Create new strategy_content", response_model=ReadStrategy_Content)
async def create(request: Request, strategy_content: CreateStrategy_Content, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-create'])

    try:
        new_data = strategy_content.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ContentModel.objects(db)
        new_strategy_content = await obj.create(**kwargs)
        return new_strategy_content
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy content failed")

create.__doc__ = f" Create a new strategy_content".expandtabs()


# create multiple strategy_contents
@router.post('/add-strategy_contents', tags=['strategy_contents'], status_code=HTTP_201_CREATED, summary="Create multiple strategy_contents", response_model=List[ReadStrategy_Content])
async def create_multiple_strategy_contents(request: Request, strategy_contents: List[CreateStrategy_Content], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-create'])

    new_items, errors_info = [], []
    try:
        for strategy_content_index, strategy_content in enumerate(strategy_contents):
            try:
                new_data = strategy_content.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_ContentModel.objects(db)
                new_strategy_contents = await obj.create(only_add=True, **kwargs)
                new_items.append(new_strategy_contents)
            except HTTPException as e:
                errors_info.append({"index": strategy_content_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new strategy contents failed")

create.__doc__ = f" Create multiple new strategy_contents".expandtabs()


# upsert multiple strategy_contents
@router.post('/upsert-multiple-strategy_contents', tags=['strategy_contents'], status_code=HTTP_201_CREATED, summary="Upsert multiple strategy_contents", response_model=List[ReadStrategy_Content])
async def upsert_multiple_strategy_contents(request: Request, strategy_contents: List[CreateStrategy_Content], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-create'])
    new_items, errors_info = [], []
    try:
        for strategy_content_index, strategy_content in enumerate(strategy_contents):
            try:
                new_data = strategy_content.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Strategy_ContentModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Strategy_ContentModel.objects(db)
                    updated_strategy_content = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_strategy_contents)
                else:
                    obj = await Strategy_ContentModel.objects(db)
                    new_strategy_contents = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_strategy_contents)
            except HTTPException as e:
                errors_info.append({"index": strategy_content_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple strategy contents failed")

upsert_multiple_strategy_contents.__doc__ = f" upsert multiple strategy_contents".expandtabs()


# update strategy_content
@router.put('/strategy_content_id', tags=['strategy_contents'], status_code=HTTP_201_CREATED, summary="Update strategy_content with ID")
async def update(request: Request, strategy_content_id: Union[str, int], strategy_content: UpdateStrategy_Content, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-update'])
    try:
        obj = await Strategy_ContentModel.objects(db)
        old_data = await obj.get(id=strategy_content_id)
        new_data = strategy_content.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ContentModel.objects(db)
        result = await obj.update(obj_id=strategy_content_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a strategy_content by its id and payload".expandtabs()


# delete strategy_content
@router.delete('/strategy_content_id', tags=['strategy_contents'], status_code=HTTP_204_NO_CONTENT, summary="Delete strategy_content with ID", response_class=Response)
async def delete(request: Request, strategy_content_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-delete'])
    try:
        obj = await Strategy_ContentModel.objects(db)
        old_data = await obj.get(id=strategy_content_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{strategy_content_id}> record not found in strategy_contents"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ContentModel.objects(db)
        await obj.delete(obj_id=strategy_content_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a strategy_content by its id".expandtabs()


# delete multiple strategy_contents
@router.delete('/delete-strategy_contents', tags=['strategy_contents'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple strategy_contents with IDs", response_class=Response)
async def delete_multiple_strategy_contents(request: Request, strategy_contents_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-strategy_contents-delete'])
    try:
        all_old_data = Strategy_ContentModel.objects(db).get_multiple(obj_ids=strategy_contents_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{strategy_contents_id}> record not found in strategy_contents"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Strategy_ContentModel.objects(db)
        await obj.delete_multiple(obj_ids=strategy_contents_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting strategy_contents_id <{strategy_contents_id}>")

delete.__doc__ = f" Delete multiple strategy_contents by list of ids".expandtabs()
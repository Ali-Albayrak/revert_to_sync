from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_competitors_schema import *
from business.brief_competitors_model import Brief_CompetitorModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_competitors_model import Brief_CompetitorModel


router = APIRouter()



# list brief_competitors
@router.get('/', tags=['brief_competitors'], status_code=HTTP_200_OK, summary="List brief_competitors", response_model=ReadBrief_Competitors)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_competitors-list', 'zekoder-new_verion-brief_competitors-get'])
    try:
        obj = await Brief_CompetitorModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_competitor")

list.__doc__ = f" List brief_competitors".expandtabs()


# get brief_competitor
@router.get('/brief_competitor_id', tags=['brief_competitors'], status_code=HTTP_200_OK, summary="Get brief_competitor with ID", response_model=ReadBrief_Competitor)
async def get(request: Request, brief_competitor_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-list', 'zekoder-new_verion-brief_competitors-get'])
    try:
        obj = await Brief_CompetitorModel.objects(db)
        result = await obj.get(id=brief_competitor_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_competitor_id}",
                "message": f"<{brief_competitor_id}> record not found in  brief_competitors"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_competitor_id}>")

get.__doc__ = f" Get a specific brief_competitor by its id".expandtabs()


# query brief_competitors
@router.post('/q', tags=['brief_competitors'], status_code=HTTP_200_OK, summary="Query brief_competitors: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-list', 'zekoder-new_verion-brief_competitors-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_CompetitorModel)
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



# create brief_competitor
@router.post('/', tags=['brief_competitors'], status_code=HTTP_201_CREATED, summary="Create new brief_competitor", response_model=ReadBrief_Competitor)
async def create(request: Request, brief_competitor: CreateBrief_Competitor, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-create'])

    try:
        new_data = brief_competitor.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_CompetitorModel.objects(db)
        new_brief_competitor = await obj.create(**kwargs)
        return new_brief_competitor
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief competitor failed")

create.__doc__ = f" Create a new brief_competitor".expandtabs()


# create multiple brief_competitors
@router.post('/add-brief_competitors', tags=['brief_competitors'], status_code=HTTP_201_CREATED, summary="Create multiple brief_competitors", response_model=List[ReadBrief_Competitor])
async def create_multiple_brief_competitors(request: Request, brief_competitors: List[CreateBrief_Competitor], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-create'])

    new_items, errors_info = [], []
    try:
        for brief_competitor_index, brief_competitor in enumerate(brief_competitors):
            try:
                new_data = brief_competitor.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_CompetitorModel.objects(db)
                new_brief_competitors = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_competitors)
            except HTTPException as e:
                errors_info.append({"index": brief_competitor_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief competitors failed")

create.__doc__ = f" Create multiple new brief_competitors".expandtabs()


# upsert multiple brief_competitors
@router.post('/upsert-multiple-brief_competitors', tags=['brief_competitors'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_competitors", response_model=List[ReadBrief_Competitor])
async def upsert_multiple_brief_competitors(request: Request, brief_competitors: List[CreateBrief_Competitor], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-create'])
    new_items, errors_info = [], []
    try:
        for brief_competitor_index, brief_competitor in enumerate(brief_competitors):
            try:
                new_data = brief_competitor.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_CompetitorModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_CompetitorModel.objects(db)
                    updated_brief_competitor = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_competitors)
                else:
                    obj = await Brief_CompetitorModel.objects(db)
                    new_brief_competitors = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_competitors)
            except HTTPException as e:
                errors_info.append({"index": brief_competitor_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief competitors failed")

upsert_multiple_brief_competitors.__doc__ = f" upsert multiple brief_competitors".expandtabs()


# update brief_competitor
@router.put('/brief_competitor_id', tags=['brief_competitors'], status_code=HTTP_201_CREATED, summary="Update brief_competitor with ID")
async def update(request: Request, brief_competitor_id: Union[str, int], brief_competitor: UpdateBrief_Competitor, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-update'])
    try:
        obj = await Brief_CompetitorModel.objects(db)
        old_data = await obj.get(id=brief_competitor_id)
        new_data = brief_competitor.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_CompetitorModel.objects(db)
        result = await obj.update(obj_id=brief_competitor_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_competitor by its id and payload".expandtabs()


# delete brief_competitor
@router.delete('/brief_competitor_id', tags=['brief_competitors'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_competitor with ID", response_class=Response)
async def delete(request: Request, brief_competitor_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-delete'])
    try:
        obj = await Brief_CompetitorModel.objects(db)
        old_data = await obj.get(id=brief_competitor_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_competitor_id}> record not found in brief_competitors"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_CompetitorModel.objects(db)
        await obj.delete(obj_id=brief_competitor_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_competitor by its id".expandtabs()


# delete multiple brief_competitors
@router.delete('/delete-brief_competitors', tags=['brief_competitors'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_competitors with IDs", response_class=Response)
async def delete_multiple_brief_competitors(request: Request, brief_competitors_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_competitors-delete'])
    try:
        all_old_data = Brief_CompetitorModel.objects(db).get_multiple(obj_ids=brief_competitors_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_competitors_id}> record not found in brief_competitors"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_CompetitorModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_competitors_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_competitors_id <{brief_competitors_id}>")

delete.__doc__ = f" Delete multiple brief_competitors by list of ids".expandtabs()
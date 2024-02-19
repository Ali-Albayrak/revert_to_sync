from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.deep_analytics_schema import *
from business.deep_analytics_model import Deep_AnalysisModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.deep_analytics_model import Deep_AnalysisModel


router = APIRouter()



# list deep_analytics
@router.get('/', tags=['deep_analytics'], status_code=HTTP_200_OK, summary="List deep_analytics", response_model=ReadDeep_Analytics)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-deep_analytics-list', 'zekoder-new_verion-deep_analytics-get'])
    try:
        obj = await Deep_AnalysisModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of deep_analysis")

list.__doc__ = f" List deep_analytics".expandtabs()


# get deep_analysis
@router.get('/deep_analysis_id', tags=['deep_analytics'], status_code=HTTP_200_OK, summary="Get deep_analysis with ID", response_model=ReadDeep_Analysis)
async def get(request: Request, deep_analysis_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-list', 'zekoder-new_verion-deep_analytics-get'])
    try:
        obj = await Deep_AnalysisModel.objects(db)
        result = await obj.get(id=deep_analysis_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{deep_analysis_id}",
                "message": f"<{deep_analysis_id}> record not found in  deep_analytics"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{deep_analysis_id}>")

get.__doc__ = f" Get a specific deep_analysis by its id".expandtabs()


# query deep_analytics
@router.post('/q', tags=['deep_analytics'], status_code=HTTP_200_OK, summary="Query deep_analytics: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-list', 'zekoder-new_verion-deep_analytics-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Deep_AnalysisModel)
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



# create deep_analysis
@router.post('/', tags=['deep_analytics'], status_code=HTTP_201_CREATED, summary="Create new deep_analysis", response_model=ReadDeep_Analysis)
async def create(request: Request, deep_analysis: CreateDeep_Analysis, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-create'])

    try:
        new_data = deep_analysis.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Deep_AnalysisModel.objects(db)
        new_deep_analysis = await obj.create(**kwargs)
        return new_deep_analysis
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new deep analysis failed")

create.__doc__ = f" Create a new deep_analysis".expandtabs()


# create multiple deep_analytics
@router.post('/add-deep_analytics', tags=['deep_analytics'], status_code=HTTP_201_CREATED, summary="Create multiple deep_analytics", response_model=List[ReadDeep_Analysis])
async def create_multiple_deep_analytics(request: Request, deep_analytics: List[CreateDeep_Analysis], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-create'])

    new_items, errors_info = [], []
    try:
        for deep_analysis_index, deep_analysis in enumerate(deep_analytics):
            try:
                new_data = deep_analysis.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Deep_AnalysisModel.objects(db)
                new_deep_analytics = await obj.create(only_add=True, **kwargs)
                new_items.append(new_deep_analytics)
            except HTTPException as e:
                errors_info.append({"index": deep_analysis_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new deep analytics failed")

create.__doc__ = f" Create multiple new deep_analytics".expandtabs()


# upsert multiple deep_analytics
@router.post('/upsert-multiple-deep_analytics', tags=['deep_analytics'], status_code=HTTP_201_CREATED, summary="Upsert multiple deep_analytics", response_model=List[ReadDeep_Analysis])
async def upsert_multiple_deep_analytics(request: Request, deep_analytics: List[CreateDeep_Analysis], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-create'])
    new_items, errors_info = [], []
    try:
        for deep_analysis_index, deep_analysis in enumerate(deep_analytics):
            try:
                new_data = deep_analysis.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Deep_AnalysisModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Deep_AnalysisModel.objects(db)
                    updated_deep_analysis = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_deep_analytics)
                else:
                    obj = await Deep_AnalysisModel.objects(db)
                    new_deep_analytics = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_deep_analytics)
            except HTTPException as e:
                errors_info.append({"index": deep_analysis_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple deep analytics failed")

upsert_multiple_deep_analytics.__doc__ = f" upsert multiple deep_analytics".expandtabs()


# update deep_analysis
@router.put('/deep_analysis_id', tags=['deep_analytics'], status_code=HTTP_201_CREATED, summary="Update deep_analysis with ID")
async def update(request: Request, deep_analysis_id: Union[str, int], deep_analysis: UpdateDeep_Analysis, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-update'])
    try:
        obj = await Deep_AnalysisModel.objects(db)
        old_data = await obj.get(id=deep_analysis_id)
        new_data = deep_analysis.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Deep_AnalysisModel.objects(db)
        result = await obj.update(obj_id=deep_analysis_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a deep_analysis by its id and payload".expandtabs()


# delete deep_analysis
@router.delete('/deep_analysis_id', tags=['deep_analytics'], status_code=HTTP_204_NO_CONTENT, summary="Delete deep_analysis with ID", response_class=Response)
async def delete(request: Request, deep_analysis_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-delete'])
    try:
        obj = await Deep_AnalysisModel.objects(db)
        old_data = await obj.get(id=deep_analysis_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{deep_analysis_id}> record not found in deep_analytics"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Deep_AnalysisModel.objects(db)
        await obj.delete(obj_id=deep_analysis_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a deep_analysis by its id".expandtabs()


# delete multiple deep_analytics
@router.delete('/delete-deep_analytics', tags=['deep_analytics'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple deep_analytics with IDs", response_class=Response)
async def delete_multiple_deep_analytics(request: Request, deep_analytics_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-deep_analytics-delete'])
    try:
        all_old_data = Deep_AnalysisModel.objects(db).get_multiple(obj_ids=deep_analytics_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{deep_analytics_id}> record not found in deep_analytics"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Deep_AnalysisModel.objects(db)
        await obj.delete_multiple(obj_ids=deep_analytics_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting deep_analytics_id <{deep_analytics_id}>")

delete.__doc__ = f" Delete multiple deep_analytics by list of ids".expandtabs()
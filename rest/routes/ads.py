from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.ads_schema import *
from business.ads_model import AdModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.ads_model import AdModel


router = APIRouter()



# list ads
@router.get('/', tags=['ads'], status_code=HTTP_200_OK, summary="List ads", response_model=ReadAds)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-ads-list', 'zekoder-new_verion-ads-get'])
    try:
        obj = await AdModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of ad")

list.__doc__ = f" List ads".expandtabs()


# get ad
@router.get('/ad_id', tags=['ads'], status_code=HTTP_200_OK, summary="Get ad with ID", response_model=ReadAd)
async def get(request: Request, ad_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-list', 'zekoder-new_verion-ads-get'])
    try:
        obj = await AdModel.objects(db)
        result = await obj.get(id=ad_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{ad_id}",
                "message": f"<{ad_id}> record not found in  ads"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{ad_id}>")

get.__doc__ = f" Get a specific ad by its id".expandtabs()


# query ads
@router.post('/q', tags=['ads'], status_code=HTTP_200_OK, summary="Query ads: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-list', 'zekoder-new_verion-ads-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, AdModel)
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



# create ad
@router.post('/', tags=['ads'], status_code=HTTP_201_CREATED, summary="Create new ad", response_model=ReadAd)
async def create(request: Request, ad: CreateAd, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-create'])

    try:
        new_data = ad.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AdModel.objects(db)
        new_ad = await obj.create(**kwargs)
        return new_ad
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new ad failed")

create.__doc__ = f" Create a new ad".expandtabs()


# create multiple ads
@router.post('/add-ads', tags=['ads'], status_code=HTTP_201_CREATED, summary="Create multiple ads", response_model=List[ReadAd])
async def create_multiple_ads(request: Request, ads: List[CreateAd], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-create'])

    new_items, errors_info = [], []
    try:
        for ad_index, ad in enumerate(ads):
            try:
                new_data = ad.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await AdModel.objects(db)
                new_ads = await obj.create(only_add=True, **kwargs)
                new_items.append(new_ads)
            except HTTPException as e:
                errors_info.append({"index": ad_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new ads failed")

create.__doc__ = f" Create multiple new ads".expandtabs()


# upsert multiple ads
@router.post('/upsert-multiple-ads', tags=['ads'], status_code=HTTP_201_CREATED, summary="Upsert multiple ads", response_model=List[ReadAd])
async def upsert_multiple_ads(request: Request, ads: List[CreateAd], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-create'])
    new_items, errors_info = [], []
    try:
        for ad_index, ad in enumerate(ads):
            try:
                new_data = ad.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await AdModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await AdModel.objects(db)
                    updated_ad = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_ads)
                else:
                    obj = await AdModel.objects(db)
                    new_ads = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_ads)
            except HTTPException as e:
                errors_info.append({"index": ad_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple ads failed")

upsert_multiple_ads.__doc__ = f" upsert multiple ads".expandtabs()


# update ad
@router.put('/ad_id', tags=['ads'], status_code=HTTP_201_CREATED, summary="Update ad with ID")
async def update(request: Request, ad_id: Union[str, int], ad: UpdateAd, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-update'])
    try:
        obj = await AdModel.objects(db)
        old_data = await obj.get(id=ad_id)
        new_data = ad.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AdModel.objects(db)
        result = await obj.update(obj_id=ad_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a ad by its id and payload".expandtabs()


# delete ad
@router.delete('/ad_id', tags=['ads'], status_code=HTTP_204_NO_CONTENT, summary="Delete ad with ID", response_class=Response)
async def delete(request: Request, ad_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-delete'])
    try:
        obj = await AdModel.objects(db)
        old_data = await obj.get(id=ad_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{ad_id}> record not found in ads"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AdModel.objects(db)
        await obj.delete(obj_id=ad_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a ad by its id".expandtabs()


# delete multiple ads
@router.delete('/delete-ads', tags=['ads'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple ads with IDs", response_class=Response)
async def delete_multiple_ads(request: Request, ads_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-ads-delete'])
    try:
        all_old_data = AdModel.objects(db).get_multiple(obj_ids=ads_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{ads_id}> record not found in ads"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AdModel.objects(db)
        await obj.delete_multiple(obj_ids=ads_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting ads_id <{ads_id}>")

delete.__doc__ = f" Delete multiple ads by list of ids".expandtabs()
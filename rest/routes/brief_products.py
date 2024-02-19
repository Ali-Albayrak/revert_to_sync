from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.brief_products_schema import *
from business.brief_products_model import Brief_ProductModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.brief_products_model import Brief_ProductModel


router = APIRouter()



# list brief_products
@router.get('/', tags=['brief_products'], status_code=HTTP_200_OK, summary="List brief_products", response_model=ReadBrief_Products)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-brief_products-list', 'zekoder-new_verion-brief_products-get'])
    try:
        obj = await Brief_ProductModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of brief_product")

list.__doc__ = f" List brief_products".expandtabs()


# get brief_product
@router.get('/brief_product_id', tags=['brief_products'], status_code=HTTP_200_OK, summary="Get brief_product with ID", response_model=ReadBrief_Product)
async def get(request: Request, brief_product_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-list', 'zekoder-new_verion-brief_products-get'])
    try:
        obj = await Brief_ProductModel.objects(db)
        result = await obj.get(id=brief_product_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{brief_product_id}",
                "message": f"<{brief_product_id}> record not found in  brief_products"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{brief_product_id}>")

get.__doc__ = f" Get a specific brief_product by its id".expandtabs()


# query brief_products
@router.post('/q', tags=['brief_products'], status_code=HTTP_200_OK, summary="Query brief_products: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-list', 'zekoder-new_verion-brief_products-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Brief_ProductModel)
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



# create brief_product
@router.post('/', tags=['brief_products'], status_code=HTTP_201_CREATED, summary="Create new brief_product", response_model=ReadBrief_Product)
async def create(request: Request, brief_product: CreateBrief_Product, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-create'])

    try:
        new_data = brief_product.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ProductModel.objects(db)
        new_brief_product = await obj.create(**kwargs)
        return new_brief_product
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief product failed")

create.__doc__ = f" Create a new brief_product".expandtabs()


# create multiple brief_products
@router.post('/add-brief_products', tags=['brief_products'], status_code=HTTP_201_CREATED, summary="Create multiple brief_products", response_model=List[ReadBrief_Product])
async def create_multiple_brief_products(request: Request, brief_products: List[CreateBrief_Product], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-create'])

    new_items, errors_info = [], []
    try:
        for brief_product_index, brief_product in enumerate(brief_products):
            try:
                new_data = brief_product.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ProductModel.objects(db)
                new_brief_products = await obj.create(only_add=True, **kwargs)
                new_items.append(new_brief_products)
            except HTTPException as e:
                errors_info.append({"index": brief_product_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new brief products failed")

create.__doc__ = f" Create multiple new brief_products".expandtabs()


# upsert multiple brief_products
@router.post('/upsert-multiple-brief_products', tags=['brief_products'], status_code=HTTP_201_CREATED, summary="Upsert multiple brief_products", response_model=List[ReadBrief_Product])
async def upsert_multiple_brief_products(request: Request, brief_products: List[CreateBrief_Product], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-create'])
    new_items, errors_info = [], []
    try:
        for brief_product_index, brief_product in enumerate(brief_products):
            try:
                new_data = brief_product.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Brief_ProductModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Brief_ProductModel.objects(db)
                    updated_brief_product = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_brief_products)
                else:
                    obj = await Brief_ProductModel.objects(db)
                    new_brief_products = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_brief_products)
            except HTTPException as e:
                errors_info.append({"index": brief_product_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple brief products failed")

upsert_multiple_brief_products.__doc__ = f" upsert multiple brief_products".expandtabs()


# update brief_product
@router.put('/brief_product_id', tags=['brief_products'], status_code=HTTP_201_CREATED, summary="Update brief_product with ID")
async def update(request: Request, brief_product_id: Union[str, int], brief_product: UpdateBrief_Product, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-update'])
    try:
        obj = await Brief_ProductModel.objects(db)
        old_data = await obj.get(id=brief_product_id)
        new_data = brief_product.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ProductModel.objects(db)
        result = await obj.update(obj_id=brief_product_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a brief_product by its id and payload".expandtabs()


# delete brief_product
@router.delete('/brief_product_id', tags=['brief_products'], status_code=HTTP_204_NO_CONTENT, summary="Delete brief_product with ID", response_class=Response)
async def delete(request: Request, brief_product_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-delete'])
    try:
        obj = await Brief_ProductModel.objects(db)
        old_data = await obj.get(id=brief_product_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{brief_product_id}> record not found in brief_products"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ProductModel.objects(db)
        await obj.delete(obj_id=brief_product_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a brief_product by its id".expandtabs()


# delete multiple brief_products
@router.delete('/delete-brief_products', tags=['brief_products'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple brief_products with IDs", response_class=Response)
async def delete_multiple_brief_products(request: Request, brief_products_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-brief_products-delete'])
    try:
        all_old_data = Brief_ProductModel.objects(db).get_multiple(obj_ids=brief_products_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{brief_products_id}> record not found in brief_products"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Brief_ProductModel.objects(db)
        await obj.delete_multiple(obj_ids=brief_products_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting brief_products_id <{brief_products_id}>")

delete.__doc__ = f" Delete multiple brief_products by list of ids".expandtabs()
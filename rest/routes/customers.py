from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.customers_schema import *
from business.customers_model import CustomerModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *
from actions import attach_customer_to_new_user, create_brief_strategy_id, delete_user_after_customer
from business.customers_model import CustomerModel


router = APIRouter()



# list customers
@router.get('/', tags=['customers'], status_code=HTTP_200_OK, summary="List customers", response_model=ReadCustomers)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-customers-list', 'zekoder-new_verion-customers-get'])
    try:
        obj = await CustomerModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of customer")

list.__doc__ = f" List customers".expandtabs()


# get customer
@router.get('/customer_id', tags=['customers'], status_code=HTTP_200_OK, summary="Get customer with ID", response_model=ReadCustomer)
async def get(request: Request, customer_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-list', 'zekoder-new_verion-customers-get'])
    try:
        obj = await CustomerModel.objects(db)
        result = await obj.get(id=customer_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{customer_id}",
                "message": f"<{customer_id}> record not found in  customers"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{customer_id}>")

get.__doc__ = f" Get a specific customer by its id".expandtabs()


# query customers
@router.post('/q', tags=['customers'], status_code=HTTP_200_OK, summary="Query customers: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-list', 'zekoder-new_verion-customers-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, CustomerModel)
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



# create customer
@router.post('/', tags=['customers'], status_code=HTTP_201_CREATED, summary="Create new customer", response_model=ReadCustomer)
async def create(request: Request, customer: CreateCustomer, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-create'])

    try:
        await CustomerModel.validate_unique_brand_name(db, customer.brand_name)
        await CustomerModel.validate_unique_business_number(db, customer.business_number)
        new_data = customer.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await CustomerModel.objects(db)
        new_customer = await obj.create(**kwargs)
        return new_customer
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new customer failed")

create.__doc__ = f" Create a new customer".expandtabs()


# create multiple customers
@router.post('/add-customers', tags=['customers'], status_code=HTTP_201_CREATED, summary="Create multiple customers", response_model=List[ReadCustomer])
async def create_multiple_customers(request: Request, customers: List[CreateCustomer], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-create'])

    new_items, errors_info = [], []
    try:
        for customer_index, customer in enumerate(customers):
            try:
                await CustomerModel.validate_unique_brand_name(db, customer.brand_name)
                await CustomerModel.validate_unique_business_number(db, customer.business_number)
                new_data = customer.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await CustomerModel.objects(db)
                new_customers = await obj.create(only_add=True, **kwargs)
                new_items.append(new_customers)
            except HTTPException as e:
                errors_info.append({"index": customer_index, "errors": e.detail})

        if errors_info:
            return JSONResponse(errors_info, 422)
        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new customers failed")

create.__doc__ = f" Create multiple new customers".expandtabs()


# upsert multiple customers
@router.post('/upsert-multiple-customers', tags=['customers'], status_code=HTTP_201_CREATED, summary="Upsert multiple customers", response_model=List[ReadCustomer])
async def upsert_multiple_customers(request: Request, customers: List[CreateCustomer], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-create'])
    new_items, errors_info = [], []
    try:
        for customer_index, customer in enumerate(customers):
            try:
                await CustomerModel.validate_unique_brand_name(db, customer.brand_name)
                await CustomerModel.validate_unique_business_number(db, customer.business_number)
                new_data = customer.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await CustomerModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await CustomerModel.objects(db)
                    updated_customer = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_customers)
                else:
                    obj = await CustomerModel.objects(db)
                    new_customers = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_customers)
            except HTTPException as e:
                errors_info.append({"index": customer_index, "errors": e.detail})

        if errors_info:
            return JSONResponse(errors_info, 422)
        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple customers failed")

upsert_multiple_customers.__doc__ = f" upsert multiple customers".expandtabs()


# update customer
@router.put('/customer_id', tags=['customers'], status_code=HTTP_201_CREATED, summary="Update customer with ID")
async def update(request: Request, customer_id: Union[str, int], customer: UpdateCustomer, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-update'])
    try:
        await CustomerModel.validate_unique_brand_name(db, customer.brand_name, customer_id)
        await CustomerModel.validate_unique_business_number(db, customer.business_number, customer_id)
        obj = await CustomerModel.objects(db)
        old_data = await obj.get(id=customer_id)
        new_data = customer.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await CustomerModel.objects(db)
        result = await obj.update(obj_id=customer_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a customer by its id and payload".expandtabs()


# delete customer
@router.delete('/customer_id', tags=['customers'], status_code=HTTP_204_NO_CONTENT, summary="Delete customer with ID", response_class=Response)
async def delete(request: Request, customer_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-delete'])
    try:
        obj = await CustomerModel.objects(db)
        old_data = await obj.get(id=customer_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{customer_id}> record not found in customers"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await CustomerModel.objects(db)
        await obj.delete(obj_id=customer_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a customer by its id".expandtabs()


# delete multiple customers
@router.delete('/delete-customers', tags=['customers'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple customers with IDs", response_class=Response)
async def delete_multiple_customers(request: Request, customers_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-customers-delete'])
    try:
        all_old_data = CustomerModel.objects(db).get_multiple(obj_ids=customers_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{customers_id}> record not found in customers"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await CustomerModel.objects(db)
        await obj.delete_multiple(obj_ids=customers_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting customers_id <{customers_id}>")

delete.__doc__ = f" Delete multiple customers by list of ids".expandtabs()
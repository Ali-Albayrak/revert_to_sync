from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.appointments_schema import *
from business.appointments_model import AppointmentModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.appointments_model import AppointmentModel


router = APIRouter()



# list appointments
@router.get('/', tags=['appointments'], status_code=HTTP_200_OK, summary="List appointments", response_model=ReadAppointments)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-appointments-list', 'zekoder-new_verion-appointments-get'])
    try:
        obj = await AppointmentModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of appointment")

list.__doc__ = f" List appointments".expandtabs()


# get appointment
@router.get('/appointment_id', tags=['appointments'], status_code=HTTP_200_OK, summary="Get appointment with ID", response_model=ReadAppointment)
async def get(request: Request, appointment_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-list', 'zekoder-new_verion-appointments-get'])
    try:
        obj = await AppointmentModel.objects(db)
        result = await obj.get(id=appointment_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{appointment_id}",
                "message": f"<{appointment_id}> record not found in  appointments"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{appointment_id}>")

get.__doc__ = f" Get a specific appointment by its id".expandtabs()


# query appointments
@router.post('/q', tags=['appointments'], status_code=HTTP_200_OK, summary="Query appointments: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-list', 'zekoder-new_verion-appointments-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, AppointmentModel)
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



# create appointment
@router.post('/', tags=['appointments'], status_code=HTTP_201_CREATED, summary="Create new appointment", response_model=ReadAppointment)
async def create(request: Request, appointment: CreateAppointment, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-create'])

    try:
        new_data = appointment.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AppointmentModel.objects(db)
        new_appointment = await obj.create(**kwargs)
        return new_appointment
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new appointment failed")

create.__doc__ = f" Create a new appointment".expandtabs()


# create multiple appointments
@router.post('/add-appointments', tags=['appointments'], status_code=HTTP_201_CREATED, summary="Create multiple appointments", response_model=List[ReadAppointment])
async def create_multiple_appointments(request: Request, appointments: List[CreateAppointment], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-create'])

    new_items, errors_info = [], []
    try:
        for appointment_index, appointment in enumerate(appointments):
            try:
                new_data = appointment.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await AppointmentModel.objects(db)
                new_appointments = await obj.create(only_add=True, **kwargs)
                new_items.append(new_appointments)
            except HTTPException as e:
                errors_info.append({"index": appointment_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new appointments failed")

create.__doc__ = f" Create multiple new appointments".expandtabs()


# upsert multiple appointments
@router.post('/upsert-multiple-appointments', tags=['appointments'], status_code=HTTP_201_CREATED, summary="Upsert multiple appointments", response_model=List[ReadAppointment])
async def upsert_multiple_appointments(request: Request, appointments: List[CreateAppointment], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-create'])
    new_items, errors_info = [], []
    try:
        for appointment_index, appointment in enumerate(appointments):
            try:
                new_data = appointment.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await AppointmentModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await AppointmentModel.objects(db)
                    updated_appointment = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_appointments)
                else:
                    obj = await AppointmentModel.objects(db)
                    new_appointments = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_appointments)
            except HTTPException as e:
                errors_info.append({"index": appointment_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple appointments failed")

upsert_multiple_appointments.__doc__ = f" upsert multiple appointments".expandtabs()


# update appointment
@router.put('/appointment_id', tags=['appointments'], status_code=HTTP_201_CREATED, summary="Update appointment with ID")
async def update(request: Request, appointment_id: Union[str, int], appointment: UpdateAppointment, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-update'])
    try:
        obj = await AppointmentModel.objects(db)
        old_data = await obj.get(id=appointment_id)
        new_data = appointment.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AppointmentModel.objects(db)
        result = await obj.update(obj_id=appointment_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a appointment by its id and payload".expandtabs()


# delete appointment
@router.delete('/appointment_id', tags=['appointments'], status_code=HTTP_204_NO_CONTENT, summary="Delete appointment with ID", response_class=Response)
async def delete(request: Request, appointment_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-delete'])
    try:
        obj = await AppointmentModel.objects(db)
        old_data = await obj.get(id=appointment_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{appointment_id}> record not found in appointments"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AppointmentModel.objects(db)
        await obj.delete(obj_id=appointment_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a appointment by its id".expandtabs()


# delete multiple appointments
@router.delete('/delete-appointments', tags=['appointments'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple appointments with IDs", response_class=Response)
async def delete_multiple_appointments(request: Request, appointments_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-appointments-delete'])
    try:
        all_old_data = AppointmentModel.objects(db).get_multiple(obj_ids=appointments_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{appointments_id}> record not found in appointments"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await AppointmentModel.objects(db)
        await obj.delete_multiple(obj_ids=appointments_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting appointments_id <{appointments_id}>")

delete.__doc__ = f" Delete multiple appointments by list of ids".expandtabs()
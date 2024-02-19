from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.folders_schema import *
from business.folders_model import FolderModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.folders_model import FolderModel


router = APIRouter()



# list folders
@router.get('/', tags=['folders'], status_code=HTTP_200_OK, summary="List folders", response_model=ReadFolders)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-folders-list', 'zekoder-new_verion-folders-get'])
    try:
        obj = await FolderModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of folder")

list.__doc__ = f" List folders".expandtabs()


# get folder
@router.get('/folder_id', tags=['folders'], status_code=HTTP_200_OK, summary="Get folder with ID", response_model=ReadFolder)
async def get(request: Request, folder_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-list', 'zekoder-new_verion-folders-get'])
    try:
        obj = await FolderModel.objects(db)
        result = await obj.get(id=folder_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{folder_id}",
                "message": f"<{folder_id}> record not found in  folders"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{folder_id}>")

get.__doc__ = f" Get a specific folder by its id".expandtabs()


# query folders
@router.post('/q', tags=['folders'], status_code=HTTP_200_OK, summary="Query folders: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-list', 'zekoder-new_verion-folders-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, FolderModel)
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



# create folder
@router.post('/', tags=['folders'], status_code=HTTP_201_CREATED, summary="Create new folder", response_model=ReadFolder)
async def create(request: Request, folder: CreateFolder, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-create'])

    try:
        new_data = folder.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await FolderModel.objects(db)
        new_folder = await obj.create(**kwargs)
        return new_folder
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new folder failed")

create.__doc__ = f" Create a new folder".expandtabs()


# create multiple folders
@router.post('/add-folders', tags=['folders'], status_code=HTTP_201_CREATED, summary="Create multiple folders", response_model=List[ReadFolder])
async def create_multiple_folders(request: Request, folders: List[CreateFolder], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-create'])

    new_items, errors_info = [], []
    try:
        for folder_index, folder in enumerate(folders):
            try:
                new_data = folder.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await FolderModel.objects(db)
                new_folders = await obj.create(only_add=True, **kwargs)
                new_items.append(new_folders)
            except HTTPException as e:
                errors_info.append({"index": folder_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new folders failed")

create.__doc__ = f" Create multiple new folders".expandtabs()


# upsert multiple folders
@router.post('/upsert-multiple-folders', tags=['folders'], status_code=HTTP_201_CREATED, summary="Upsert multiple folders", response_model=List[ReadFolder])
async def upsert_multiple_folders(request: Request, folders: List[CreateFolder], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-create'])
    new_items, errors_info = [], []
    try:
        for folder_index, folder in enumerate(folders):
            try:
                new_data = folder.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await FolderModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await FolderModel.objects(db)
                    updated_folder = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_folders)
                else:
                    obj = await FolderModel.objects(db)
                    new_folders = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_folders)
            except HTTPException as e:
                errors_info.append({"index": folder_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple folders failed")

upsert_multiple_folders.__doc__ = f" upsert multiple folders".expandtabs()


# update folder
@router.put('/folder_id', tags=['folders'], status_code=HTTP_201_CREATED, summary="Update folder with ID")
async def update(request: Request, folder_id: Union[str, int], folder: UpdateFolder, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-update'])
    try:
        obj = await FolderModel.objects(db)
        old_data = await obj.get(id=folder_id)
        new_data = folder.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await FolderModel.objects(db)
        result = await obj.update(obj_id=folder_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a folder by its id and payload".expandtabs()


# delete folder
@router.delete('/folder_id', tags=['folders'], status_code=HTTP_204_NO_CONTENT, summary="Delete folder with ID", response_class=Response)
async def delete(request: Request, folder_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-delete'])
    try:
        obj = await FolderModel.objects(db)
        old_data = await obj.get(id=folder_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{folder_id}> record not found in folders"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await FolderModel.objects(db)
        await obj.delete(obj_id=folder_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a folder by its id".expandtabs()


# delete multiple folders
@router.delete('/delete-folders', tags=['folders'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple folders with IDs", response_class=Response)
async def delete_multiple_folders(request: Request, folders_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-folders-delete'])
    try:
        all_old_data = FolderModel.objects(db).get_multiple(obj_ids=folders_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{folders_id}> record not found in folders"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await FolderModel.objects(db)
        await obj.delete_multiple(obj_ids=folders_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting folders_id <{folders_id}>")

delete.__doc__ = f" Delete multiple folders by list of ids".expandtabs()
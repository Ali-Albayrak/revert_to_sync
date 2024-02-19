from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.file_assets_schema import *
from business.file_assets_model import File_AssetModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.file_assets_model import File_AssetModel


router = APIRouter()



# list file_assets
@router.get('/', tags=['file_assets'], status_code=HTTP_200_OK, summary="List file_assets", response_model=ReadFile_Assets)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-file_assets-list', 'zekoder-new_verion-file_assets-get'])
    try:
        obj = await File_AssetModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of file_asset")

list.__doc__ = f" List file_assets".expandtabs()


# get file_asset
@router.get('/file_asset_id', tags=['file_assets'], status_code=HTTP_200_OK, summary="Get file_asset with ID", response_model=ReadFile_Asset)
async def get(request: Request, file_asset_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-list', 'zekoder-new_verion-file_assets-get'])
    try:
        obj = await File_AssetModel.objects(db)
        result = await obj.get(id=file_asset_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{file_asset_id}",
                "message": f"<{file_asset_id}> record not found in  file_assets"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{file_asset_id}>")

get.__doc__ = f" Get a specific file_asset by its id".expandtabs()


# query file_assets
@router.post('/q', tags=['file_assets'], status_code=HTTP_200_OK, summary="Query file_assets: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-list', 'zekoder-new_verion-file_assets-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, File_AssetModel)
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



# create file_asset
@router.post('/', tags=['file_assets'], status_code=HTTP_201_CREATED, summary="Create new file_asset", response_model=ReadFile_Asset)
async def create(request: Request, file_asset: CreateFile_Asset, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-create'])

    try:
        new_data = file_asset.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await File_AssetModel.objects(db)
        new_file_asset = await obj.create(**kwargs)
        return new_file_asset
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new file asset failed")

create.__doc__ = f" Create a new file_asset".expandtabs()


# create multiple file_assets
@router.post('/add-file_assets', tags=['file_assets'], status_code=HTTP_201_CREATED, summary="Create multiple file_assets", response_model=List[ReadFile_Asset])
async def create_multiple_file_assets(request: Request, file_assets: List[CreateFile_Asset], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-create'])

    new_items, errors_info = [], []
    try:
        for file_asset_index, file_asset in enumerate(file_assets):
            try:
                new_data = file_asset.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await File_AssetModel.objects(db)
                new_file_assets = await obj.create(only_add=True, **kwargs)
                new_items.append(new_file_assets)
            except HTTPException as e:
                errors_info.append({"index": file_asset_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new file assets failed")

create.__doc__ = f" Create multiple new file_assets".expandtabs()


# upsert multiple file_assets
@router.post('/upsert-multiple-file_assets', tags=['file_assets'], status_code=HTTP_201_CREATED, summary="Upsert multiple file_assets", response_model=List[ReadFile_Asset])
async def upsert_multiple_file_assets(request: Request, file_assets: List[CreateFile_Asset], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-create'])
    new_items, errors_info = [], []
    try:
        for file_asset_index, file_asset in enumerate(file_assets):
            try:
                new_data = file_asset.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await File_AssetModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await File_AssetModel.objects(db)
                    updated_file_asset = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_file_assets)
                else:
                    obj = await File_AssetModel.objects(db)
                    new_file_assets = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_file_assets)
            except HTTPException as e:
                errors_info.append({"index": file_asset_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple file assets failed")

upsert_multiple_file_assets.__doc__ = f" upsert multiple file_assets".expandtabs()


# update file_asset
@router.put('/file_asset_id', tags=['file_assets'], status_code=HTTP_201_CREATED, summary="Update file_asset with ID")
async def update(request: Request, file_asset_id: Union[str, int], file_asset: UpdateFile_Asset, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-update'])
    try:
        obj = await File_AssetModel.objects(db)
        old_data = await obj.get(id=file_asset_id)
        new_data = file_asset.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await File_AssetModel.objects(db)
        result = await obj.update(obj_id=file_asset_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a file_asset by its id and payload".expandtabs()


# delete file_asset
@router.delete('/file_asset_id', tags=['file_assets'], status_code=HTTP_204_NO_CONTENT, summary="Delete file_asset with ID", response_class=Response)
async def delete(request: Request, file_asset_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-delete'])
    try:
        obj = await File_AssetModel.objects(db)
        old_data = await obj.get(id=file_asset_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{file_asset_id}> record not found in file_assets"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await File_AssetModel.objects(db)
        await obj.delete(obj_id=file_asset_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a file_asset by its id".expandtabs()


# delete multiple file_assets
@router.delete('/delete-file_assets', tags=['file_assets'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple file_assets with IDs", response_class=Response)
async def delete_multiple_file_assets(request: Request, file_assets_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-file_assets-delete'])
    try:
        all_old_data = File_AssetModel.objects(db).get_multiple(obj_ids=file_assets_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{file_assets_id}> record not found in file_assets"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await File_AssetModel.objects(db)
        await obj.delete_multiple(obj_ids=file_assets_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting file_assets_id <{file_assets_id}>")

delete.__doc__ = f" Delete multiple file_assets by list of ids".expandtabs()
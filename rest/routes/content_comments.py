from typing import Union, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, Query as QueryParam
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_201_CREATED

from business.content_comments_schema import *
from business.content_comments_model import Content_CommentModel

from core.depends import CommonDependencies, get_async_db, get_sync_db, Protect, zeauth_url
from core.logger import log
from core.query import *

from business.content_comments_model import Content_CommentModel


router = APIRouter()



# list content_comments
@router.get('/', tags=['content_comments'], status_code=HTTP_200_OK, summary="List content_comments", response_model=ReadContent_Comments)
async def list(request: Request, token: str = Depends(Protect), db: AsyncSession = Depends(get_async_db), commons: CommonDependencies = Depends(CommonDependencies)):

    token.auth(['zekoder-new_verion-content_comments-list', 'zekoder-new_verion-content_comments-get'])
    try:
        obj = await Content_CommentModel.objects(db)
        result = await obj.all(offset=commons.offset, limit=commons.size)
        return {
            'data': result,
            'page_size': commons.size,
            'next_page': int(commons.page) + 1
        }
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch list of content_comment")

list.__doc__ = f" List content_comments".expandtabs()


# get content_comment
@router.get('/content_comment_id', tags=['content_comments'], status_code=HTTP_200_OK, summary="Get content_comment with ID", response_model=ReadContent_Comment)
async def get(request: Request, content_comment_id: str, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-list', 'zekoder-new_verion-content_comments-get'])
    try:
        obj = await Content_CommentModel.objects(db)
        result = await obj.get(id=content_comment_id)
        if result:
            return result
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={
                "field_name": "{content_comment_id}",
                "message": f"<{content_comment_id}> record not found in  content_comments"
            })
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "could not fetch record <{content_comment_id}>")

get.__doc__ = f" Get a specific content_comment by its id".expandtabs()


# query content_comments
@router.post('/q', tags=['content_comments'], status_code=HTTP_200_OK, summary="Query content_comments: Projection, Limit/skips, Sorting, Filters, Joins, Aggregates, Count, Group")
async def query(request: Request, q: QuerySchema, db: Session = Depends(get_sync_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-list', 'zekoder-new_verion-content_comments-get'])

    try:
        size = q.limit if q.limit else 20
        page = int(q.skip)/size if q.skip else 1
        jq = JSONQ(db, Content_CommentModel)
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



# create content_comment
@router.post('/', tags=['content_comments'], status_code=HTTP_201_CREATED, summary="Create new content_comment", response_model=ReadContent_Comment)
async def create(request: Request, content_comment: CreateContent_Comment, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-create'])

    try:
        new_data = content_comment.dict()
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Content_CommentModel.objects(db)
        new_content_comment = await obj.create(**kwargs)
        return new_content_comment
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new content comment failed")

create.__doc__ = f" Create a new content_comment".expandtabs()


# create multiple content_comments
@router.post('/add-content_comments', tags=['content_comments'], status_code=HTTP_201_CREATED, summary="Create multiple content_comments", response_model=List[ReadContent_Comment])
async def create_multiple_content_comments(request: Request, content_comments: List[CreateContent_Comment], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-create'])

    new_items, errors_info = [], []
    try:
        for content_comment_index, content_comment in enumerate(content_comments):
            try:
                new_data = content_comment.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Content_CommentModel.objects(db)
                new_content_comments = await obj.create(only_add=True, **kwargs)
                new_items.append(new_content_comments)
            except HTTPException as e:
                errors_info.append({"index": content_comment_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"creation of new content comments failed")

create.__doc__ = f" Create multiple new content_comments".expandtabs()


# upsert multiple content_comments
@router.post('/upsert-multiple-content_comments', tags=['content_comments'], status_code=HTTP_201_CREATED, summary="Upsert multiple content_comments", response_model=List[ReadContent_Comment])
async def upsert_multiple_content_comments(request: Request, content_comments: List[CreateContent_Comment], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-create'])
    new_items, errors_info = [], []
    try:
        for content_comment_index, content_comment in enumerate(content_comments):
            try:
                new_data = content_comment.dict()
                kwargs = {
                    "model_data": new_data,
                    "signal_data": {
                        "jwt": token.credentials,
                        "new_data": new_data,
                        "old_data": {},
                        "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
                    }
                }
                obj = await Content_CommentModel.objects(db)
                old_data = await obj.get(id=new_data['id'])
                if old_data:
                    kwargs['signal_data']['old_data'] = dict(old_data.__dict__) if old_data else {}
                    obj = await Content_CommentModel.objects(db)
                    updated_content_comment = await obj.update(obj_id=new_data['id'], **kwargs)
                    new_items.append(updated_content_comments)
                else:
                    obj = await Content_CommentModel.objects(db)
                    new_content_comments = await obj.create(only_add=True, **kwargs)
                    new_items.append(new_content_comments)
            except HTTPException as e:
                errors_info.append({"index": content_comment_index, "errors": e.detail})

        return new_items
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"upsert multiple content comments failed")

upsert_multiple_content_comments.__doc__ = f" upsert multiple content_comments".expandtabs()


# update content_comment
@router.put('/content_comment_id', tags=['content_comments'], status_code=HTTP_201_CREATED, summary="Update content_comment with ID")
async def update(request: Request, content_comment_id: Union[str, int], content_comment: UpdateContent_Comment, db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-update'])
    try:
        obj = await Content_CommentModel.objects(db)
        old_data = await obj.get(id=content_comment_id)
        new_data = content_comment.dict(exclude_unset=True)
        kwargs = {
            "model_data": new_data,
            "signal_data": {
                "jwt": token.credentials,
                "new_data": new_data,
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Content_CommentModel.objects(db)
        result = await obj.update(obj_id=content_comment_id, **kwargs)
        return result
    except HTTPException as e:
        raise e
    except IntegrityError as e:
        raise HTTPException(422, e.orig.args[-1])
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

update.__doc__ = f" Update a content_comment by its id and payload".expandtabs()


# delete content_comment
@router.delete('/content_comment_id', tags=['content_comments'], status_code=HTTP_204_NO_CONTENT, summary="Delete content_comment with ID", response_class=Response)
async def delete(request: Request, content_comment_id: Union[str, int], db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-delete'])
    try:
        obj = await Content_CommentModel.objects(db)
        old_data = await obj.get(id=content_comment_id)
        if not old_data:
            return JSONResponse(content={"message": f"<{content_comment_id}> record not found in content_comments"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": dict(old_data.__dict__) if old_data else {},
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Content_CommentModel.objects(db)
        await obj.delete(obj_id=content_comment_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, "failed updating session with id <{session_id}>")

delete.__doc__ = f" Delete a content_comment by its id".expandtabs()


# delete multiple content_comments
@router.delete('/delete-content_comments', tags=['content_comments'], status_code=HTTP_204_NO_CONTENT, summary="Delete multiple content_comments with IDs", response_class=Response)
async def delete_multiple_content_comments(request: Request, content_comments_id: List[str] = QueryParam(), db: AsyncSession = Depends(get_async_db), token: str = Depends(Protect)):

    token.auth(['zekoder-new_verion-content_comments-delete'])
    try:
        all_old_data = Content_CommentModel.objects(db).get_multiple(obj_ids=content_comments_id)
        if not all_old_data:
            return JSONResponse(content={"message": f"<{content_comments_id}> record not found in content_comments"}, status_code=400)
        kwargs = {
            "model_data": {},
            "signal_data": {
                "jwt": token.credentials,
                "new_data": {},
                "old_data": all_old_data if len(all_old_data) > 0 else [],
                "well_known_urls": {"zeauth": zeauth_url, "self": str(request.base_url)}
            }
        }
        obj = await Content_CommentModel.objects(db)
        await obj.delete_multiple(obj_ids=content_comments_id, **kwargs)
    except Exception as e:
        log.debug(e)
        raise HTTPException(500, f"failed deleting content_comments_id <{content_comments_id}>")

delete.__doc__ = f" Delete multiple content_comments by list of ids".expandtabs()
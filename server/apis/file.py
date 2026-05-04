

from typing import Optional, List
from pathlib import Path

from fastapi import APIRouter, Depends, Path as PathParam, Request, Query, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from annotation.auth import Auth, AuthController
from annotation.log import Log, OperationType
from models.file import SystemFile, get_file_type
from schemas.common import BaseResponse, DeleteListParams
from utils.response import ResponseUtil
from utils.storage import StorageFactory
from utils.log import logger

fileAPI = APIRouter(prefix="/file")

#  # (description)
fileAccessAPI = APIRouter()


# ====================  # (description)

@fileAccessAPI.get("/files/{path:path}", response_class=FileResponse, summary="")
async def get_local_file(request: Request, path: str):
    """Serve local storage files"""
    dynamic_config = request.app.state.dynamic_config
    base_path = await dynamic_config.get("upload_local_path", "uploads")
    file_path = Path(base_path) / path
    
    if not file_path.exists():
        return JSONResponse(status_code=404, content={"success": False, "msg": "File not found"})
    
    return FileResponse(file_path)


# ====================  # (description)

authFileAPI = APIRouter(
    prefix="/file",
    dependencies=[Depends(AuthController.get_current_user)],
)


class FileSearchParams(BaseModel):
    """File search parameters"""
    page: int = 1
    pageSize: int = 20
    name: Optional[str] = None
    file_type: Optional[str] = None
    folder: Optional[str] = None
    storage_type: Optional[str] = None


@authFileAPI.get("/list", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.SELECT)
@Auth(permission_list=["file:btn:list", "GET:/file/list"])
async def get_file_list(
    request: Request,
    page: int = Query(default=1, description=""),
    pageSize: int = Query(default=20, description=""),
    name: Optional[str] = Query(default=None, description="File name"),
    file_type: Optional[str] = Query(default=None, description=""),
    folder: Optional[str] = Query(default=None, description="Folder"),
    storage_type: Optional[str] = Query(default=None, description=""),
):
    """Get file list"""
    filter_args = {"is_del": False}
    
    if name:
        filter_args["name__contains"] = name
    if file_type:
        filter_args["file_type"] = file_type
    if folder is not None:
        filter_args["folder"] = folder
    if storage_type:
        filter_args["storage_type"] = storage_type
    
    total = await SystemFile.filter(**filter_args).count()
    files = await SystemFile.filter(**filter_args).order_by("-created_at").offset(
        (page - 1) * pageSize
    ).limit(pageSize).values(
        "id", "name", "key", "url", "size", "file_type", "mime_type",
        "extension", "hash", "storage_type", "folder", "uploader_id",
        "uploader_name", "remark", "created_at", "updated_at"
    )
    
    return ResponseUtil.success(data={
        "total": total,
        "result": files,
        "page": page,
        "pageSize": pageSize
    })


@authFileAPI.post("/upload", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.INSERT)
@Auth(permission_list=["file:btn:upload", "POST:/file/upload"])
async def upload_file(
    request: Request,
    file: UploadFile = File(..., description="File"),
    folder: str = Query(default="", description="Folder"),
    current_user: dict = Depends(AuthController.get_current_user)
):
    """Upload file"""
    dynamic_config = request.app.state.dynamic_config
    
    #  # (description)
    max_size = await dynamic_config.get_int("upload_max_size", 100)
    content = await file.read()
    await file.seek(0)  # 
    
    if len(content) > max_size * 1024 * 1024:
        return ResponseUtil.error(msg=f"File size exceeds {max_size}MB")
    
    #  # (description)
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    allowed_extensions = await dynamic_config.get_list("upload_allowed_extensions")
    if allowed_extensions and ext not in allowed_extensions:
        return ResponseUtil.error(msg=f": {ext}")
    
    try:
        #  # (description)
        storage = await StorageFactory.create(dynamic_config)
        storage_type = await dynamic_config.get("upload_storage_type", "local")
        
        #  # (description)
        result = await storage.upload(file, folder)
        
        #  # (description)
        file_record = await SystemFile.create(
            name=file.filename,
            key=result["key"],
            url=result["url"],
            size=result["size"],
            file_type=get_file_type(file.filename),
            mime_type=file.content_type,
            extension=ext,
            hash=result.get("hash"),
            storage_type=storage_type,
            folder=folder,
            uploader_id=current_user.get("id"),
            uploader_name=current_user.get("username")
        )
        
        return ResponseUtil.success(msg="", data={
            "id": file_record.id,
            "name": file_record.name,
            "url": file_record.url,
            "key": file_record.key,
            "size": file_record.size,
            "file_type": file_record.file_type
        })
    except Exception as e:
        logger.error(f": {e}")
        return ResponseUtil.error(msg=f": {str(e)}")


@authFileAPI.post("/upload/batch", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.INSERT)
@Auth(permission_list=["file:btn:upload", "POST:/file/upload/batch"])
async def upload_files(
    request: Request,
    files: List[UploadFile] = File(..., description="Files"),
    folder: str = Query(default="", description="Folder"),
    current_user: dict = Depends(AuthController.get_current_user)
):
    """Batch upload files"""
    dynamic_config = request.app.state.dynamic_config
    storage = await StorageFactory.create(dynamic_config)
    storage_type = await dynamic_config.get("upload_storage_type", "local")
    max_size = await dynamic_config.get_int("upload_max_size", 100)
    allowed_extensions = await dynamic_config.get_list("upload_allowed_extensions")
    
    results = []
    errors = []
    
    for file in files:
        try:
            #  # (description)
            content = await file.read()
            await file.seek(0)
            
            if len(content) > max_size * 1024 * 1024:
                errors.append({"name": file.filename, "error": f"File size exceeds {max_size}MB"})
                continue
            
            #  # (description)
            ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
            if allowed_extensions and ext not in allowed_extensions:
                errors.append({"name": file.filename, "error": f": {ext}"})
                continue
            
            #  # (description)
            result = await storage.upload(file, folder)
            
            #  # (description)
            file_record = await SystemFile.create(
                name=file.filename,
                key=result["key"],
                url=result["url"],
                size=result["size"],
                file_type=get_file_type(file.filename),
                mime_type=file.content_type,
                extension=ext,
                hash=result.get("hash"),
                storage_type=storage_type,
                folder=folder,
                uploader_id=current_user.get("id"),
                uploader_name=current_user.get("username")
            )
            
            results.append({
                "id": file_record.id,
                "name": file_record.name,
                "url": file_record.url,
                "size": file_record.size
            })
        except Exception as e:
            errors.append({"name": file.filename, "error": str(e)})
    
    return ResponseUtil.success(msg=f"Upload complete: {len(results)} success, {len(errors)} errors", data={
        "success": results,
        "errors": errors
    })


@authFileAPI.delete("/delete/{id}", response_class=JSONResponse, response_model=BaseResponse, summary="")
@authFileAPI.post("/delete/{id}", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.DELETE)
@Auth(permission_list=["file:btn:delete", "DELETE,POST:/file/delete/*"])
async def delete_file(request: Request, id: str = PathParam(description="ID")):
    """Delete file"""
    file_record = await SystemFile.get_or_none(id=id, is_del=False)
    if not file_record:
        return ResponseUtil.error(msg="File not found")
    
    try:
        dynamic_config = request.app.state.dynamic_config
        storage = await StorageFactory.create(dynamic_config)
        
        #  # (description)
        await storage.delete(file_record.key)
        
        #  # (description)
        file_record.is_del = True
        await file_record.save()
        
        return ResponseUtil.success(msg="")
    except Exception as e:
        logger.error(f": {e}")
        return ResponseUtil.error(msg=f": {str(e)}")


@authFileAPI.delete("/deleteList", response_class=JSONResponse, response_model=BaseResponse, summary="")
@authFileAPI.post("/deleteList", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.DELETE)
@Auth(permission_list=["file:btn:delete", "DELETE,POST:/file/deleteList"])
async def delete_file_list(request: Request, params: DeleteListParams):
    """Batch delete files"""
    dynamic_config = request.app.state.dynamic_config
    storage = await StorageFactory.create(dynamic_config)
    
    files = await SystemFile.filter(id__in=list(set(params.ids)), is_del=False)
    
    for file_record in files:
        try:
            await storage.delete(file_record.key)
        except Exception as e:
            logger.warning(f": {e}")
    
    await SystemFile.filter(id__in=list(set(params.ids)), is_del=False).update(is_del=True)
    
    return ResponseUtil.success(msg="")


@authFileAPI.get("/info/{id}", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.SELECT)
@Auth(permission_list=["file:btn:info", "GET:/file/info/*"])
async def get_file_info(request: Request, id: str = PathParam(description="ID")):
    """Get file details"""
    file_record = await SystemFile.get_or_none(id=id, is_del=False)
    if not file_record:
        return ResponseUtil.error(msg="File not found")
    
    return ResponseUtil.success(data={
        "id": file_record.id,
        "name": file_record.name,
        "key": file_record.key,
        "url": file_record.url,
        "size": file_record.size,
        "file_type": file_record.file_type,
        "mime_type": file_record.mime_type,
        "extension": file_record.extension,
        "hash": file_record.hash,
        "storage_type": file_record.storage_type,
        "folder": file_record.folder,
        "uploader_id": file_record.uploader_id,
        "uploader_name": file_record.uploader_name,
        "remark": file_record.remark,
        "created_at": file_record.created_at,
        "updated_at": file_record.updated_at
    })


@authFileAPI.get("/statistics", response_class=JSONResponse, response_model=BaseResponse, summary="")
@Log(title="", operation_type=OperationType.SELECT)
@Auth(permission_list=["file:btn:list", "GET:/file/statistics"])
async def get_file_statistics(request: Request):
    """Get file statistics"""
    from models.sa_orm import Count, Sum
    
    #  # (description)
    total_count = await SystemFile.filter(is_del=False).count()
    total_size_result = await SystemFile.filter(is_del=False).annotate(
        total=Sum("size")
    ).values("total")
    total_size = total_size_result[0]["total"] or 0 if total_size_result else 0
    
    #  # (description)
    type_stats = await SystemFile.filter(is_del=False).annotate(
        count=Count("id")
    ).group_by("file_type").values("file_type", "count")
    
    #  # (description)
    storage_stats = await SystemFile.filter(is_del=False).annotate(
        count=Count("id")
    ).group_by("storage_type").values("storage_type", "count")
    
    return ResponseUtil.success(data={
        "total_count": total_count,
        "total_size": total_size,
        "type_stats": type_stats,
        "storage_stats": storage_stats
    })


@authFileAPI.get("/storage-config", response_class=JSONResponse, response_model=BaseResponse, summary="Get storage configuration")
@Log(title="Get storage configuration", operation_type=OperationType.SELECT)
@Auth(permission_list=["file:btn:list", "GET:/file/storage-config"])
async def get_storage_config(request: Request):
    """Get current storage configuration"""
    dynamic_config = request.app.state.dynamic_config
    
    storage_type = await dynamic_config.get("upload_storage_type", "local")
    max_size = await dynamic_config.get_int("upload_max_size", 100)
    allowed_extensions = await dynamic_config.get_list("upload_allowed_extensions")
    
    return ResponseUtil.success(data={
        "storage_type": storage_type,
        "max_size": max_size,
        "allowed_extensions": allowed_extensions
    })

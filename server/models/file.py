

from .sa_orm import fields
from .common import BaseModel


class FileType:
    """"""
    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    OTHER = "other"


#  # (description)
FILE_TYPE_MAP = {
    #  # (description)
    "jpg": FileType.IMAGE, "jpeg": FileType.IMAGE, "png": FileType.IMAGE,
    "gif": FileType.IMAGE, "bmp": FileType.IMAGE, "webp": FileType.IMAGE,
    "svg": FileType.IMAGE, "ico": FileType.IMAGE,
    #  # (description)
    "doc": FileType.DOCUMENT, "docx": FileType.DOCUMENT,
    "xls": FileType.DOCUMENT, "xlsx": FileType.DOCUMENT,
    "ppt": FileType.DOCUMENT, "pptx": FileType.DOCUMENT,
    "pdf": FileType.DOCUMENT, "txt": FileType.DOCUMENT,
    "md": FileType.DOCUMENT, "csv": FileType.DOCUMENT,
    #  # (description)
    "mp4": FileType.VIDEO, "avi": FileType.VIDEO, "mov": FileType.VIDEO,
    "wmv": FileType.VIDEO, "flv": FileType.VIDEO, "mkv": FileType.VIDEO,
    #  # (description)
    "mp3": FileType.AUDIO, "wav": FileType.AUDIO, "flac": FileType.AUDIO,
    "aac": FileType.AUDIO, "ogg": FileType.AUDIO,
    #  # (description)
    "zip": FileType.ARCHIVE, "rar": FileType.ARCHIVE, "7z": FileType.ARCHIVE,
    "tar": FileType.ARCHIVE, "gz": FileType.ARCHIVE,
}


def get_file_type(filename: str) -> str:
    """Get file type from filename"""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return FILE_TYPE_MAP.get(ext, FileType.OTHER)


class SystemFile(BaseModel):
    """
    System File Model
    """
    name = fields.CharField(
        max_length=255,
        description="Original Filename",
        source_field="name"
    )
    key = fields.CharField(
        max_length=500,
        description="Storage key",
        source_field="storage_key"
    )
    url = fields.CharField(
        max_length=1000,
        description="Access URL",
        source_field="url"
    )
    size = fields.BigIntField(
        default=0,
        description="  ()",
        source_field="size"
    )
    file_type = fields.CharField(
        max_length=20,
        default=FileType.OTHER,
        description="",
        source_field="file_type"
    )
    mime_type = fields.CharField(
        max_length=100,
        null=True,
        description="MIME",
        source_field="mime_type"
    )
    extension = fields.CharField(
        max_length=20,
        null=True,
        description="File Extension",
        source_field="extension"
    )
    hash = fields.CharField(
        max_length=64,
        null=True,
        description="MD5",
        source_field="hash"
    )
    storage_type = fields.CharField(
        max_length=20,
        default="local",
        description="",
        source_field="storage_type"
    )
    folder = fields.CharField(
        max_length=255,
        default="",
        description="   ",
        source_field="folder"
    )
    uploader_id = fields.CharField(
        max_length=36,
        null=True,
        description="D",
        source_field="uploader_id"
    )
    uploader_name = fields.CharField(
        max_length=50,
        null=True,
        description="Uploader Name",
        source_field="uploader_name"
    )
    remark = fields.TextField(
        null=True,
        description="",
        source_field="remark"
    )

    class Meta:
        table = "system_file"
        table_description = "System File Table"

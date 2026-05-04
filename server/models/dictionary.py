
from .sa_orm import fields
from .common import BaseModel


class SystemDictionary(BaseModel):
    """
    ?
    """

    dict_name = fields.CharField(
        max_length=100,
        null=False,
        description="  ",
        source_field="dict_name"
    )
    """
      
    """
    dict_code = fields.CharField(
        max_length=100,
        null=False,
        unique=True,
        description="",
        source_field="dict_code"
    )
    """
    
    """
    dict_type = fields.CharField(
        max_length=50,
        null=False,
        description="",
        source_field="dict_type"
    )
    """
    
    """
    status = fields.IntField(
        null=False,
        default=1,
        description="Status (1 enabled, 0 disabled)",
        source_field="status"
    )
    """
    1??
    """
    sort = fields.IntField(
        null=False,
        default=0,
        description="Sort order (smaller number = higher priority)",
        source_field="sort"
    )
    """
    ?
    """
    remark = fields.TextField(
        null=True,
        description="",
        source_field="remark"
    )
    """
    
    """

    class Meta:
        table = "system_dictionary"
        table_description = "System Dictionary Table"
        ordering = ["sort", "-created_at"]



from .sa_orm import fields

from .common import BaseModel


class SystemDepartment(BaseModel):
    """
       
    """

    name = fields.CharField(
        max_length=50,
        description="     ",
        source_field="name"
    )
    """
         ?
    -   50
    - name
    """
    parent_id = fields.CharField(
        max_length=50,
        description="   ID",
        source_field="parent_id",
        null=True
    )
    """
       ID?
    - parent_id
    - 
    """
    sort = fields.IntField(
        default=0,
        description="?",
        source_field="sort"
    )
    """
    ?
    -       ?
    - ?0?
    -  sort?
    """

    phone = fields.CharField(
        max_length=30,
        null=True,
        description="   ",
        source_field="phone"
    )
    """
       ?
    -    30 ?
    - ?
    -  phone?
    """

    principal = fields.CharField(
        max_length=64,
        description="Department Principal",
        source_field="principal"
    )
    """
       ?
    -    64 ?
    -  principal?
    """

    email = fields.CharField(
        max_length=128,
        null=True,
        description="   ",
        source_field="email"
    )
    """
       ?
    -    128 ?
    - ?
    -  email?
    """

    status = fields.SmallIntField(
        default=1,
        description="Status (0 normal, 1 disabled)",
        source_field="status"
    )
    """
    ?
    - 1       e?       ?
    - ?1?
    -  status?
    """

    remark = fields.CharField(
        max_length=255,
        null=True,
        description="",
        source_field="remark"
    )
    """
    ?
    -    255 ?
    - ?
    -  remark?
    """

    class Meta:
        table = "system_department"
        table_description = "System Department Table"
        ordering = ["sort", "-created_at"]

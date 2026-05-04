
from .sa_orm import fields

from .common import BaseModel


class PermissionType:
    """"""
    MENU = 0      # 
    BUTTON = 1    # 
    API = 2       #    


class SystemPermission(BaseModel):
    """
    Permission Model
    Supports three types: Menu (0), Button (1), API (2)
    """
    menu_type = fields.SmallIntField(
        default=0,
        description="Permission Type (0=Menu, 1=Button, 2=API)",
        source_field="menu_type"
    )
    """
    ?
    - 0?- 
    - 1?- 
    - 2?- APICasbin?
    """
    
    parent_id = fields.UUIDField(
        default=None,
        null=True,
        description="D",
        source_field="parent_id"
    )
    
    name = fields.CharField(
        max_length=255,
        null=True,
        description="  /  ",
        source_field="name"
    )
    
    path = fields.CharField(
        max_length=255,
        description="/   ",
        null=True,
        source_field="path"
    )
    
    component = fields.CharField(
        max_length=255,
        description="",
        null=True,
        source_field="component"
    )
    
    title = fields.CharField(
        max_length=255,
        description="/  ",
        null=True,
        source_field="title"
    )

    icon = fields.CharField(
        max_length=255,
        description="",
        null=True,
        source_field="icon"
    )

    # ====================  # (description)
    
    api_path = fields.CharField(
        max_length=255,
        description="API Path (supports wildcard, e.g. /api/user/*)",
        null=True,
        source_field="api_path"
    )
    """
    API   ?
    -  menu_type=2 ?
    - /api/user/*  /api/user/1, /api/user/list ?
    -  api_path
    """
    
    api_method = fields.JSONField(
        description="HTTP request method list (e.g. ['GET', 'POST', 'PUT', 'DELETE'])",
        null=True,
        default=None,
        source_field="api_method"
    )
    """
    HTTP?
    -  menu_type=2 ?
    - SON"GET", "POST", "PUT", "DELETE"]
    - ?
    """
    
    data_scope = fields.SmallIntField(
        default=4,
        description="?   ?   ?   ?",
        null=True,
        source_field="data_scope"
    )
    """
    ?
    - 1   ?
    - 2   ?
    - 3?
    - 4   
    -  menu_type=2 ?
    """

    # ====================  # (description)

    showBadge = fields.BooleanField(
        description="   ",
        null=True,
        source_field="showBadge"
    )
    
    showTextBadge = fields.CharField(
        max_length=255,
        description="Badge Text",
        null=True,
        source_field="showTextBadge"
    )
    
    isHide = fields.BooleanField(
        description="",
        null=True,
        source_field="isHide"
    )
    
    isHideTab = fields.BooleanField(
        description="",
        null=True,
        source_field="isHideTab"
    )

    link = fields.CharField(
        max_length=255,
        description="",
        null=True,
        source_field="link"
    )
    
    isIframe = fields.BooleanField(
        description="iframe",
        null=True,
        source_field="isIframe"
    )

    keepAlive = fields.BooleanField(
        description="",
        null=True,
        source_field="keepAlive"
    )
    
    isFirstLevel = fields.BooleanField(
        description="Is First Level Menu",
        null=True,
        source_field="isFirstLevel"
    )
    
    fixedTab = fields.BooleanField(
        description="",
        null=True,
        source_field="fixedTab"
    )
    
    activePath = fields.CharField(
        max_length=255,
        description="Active Path",
        null=True,
        source_field="activePath"
    )
    
    isFullPage = fields.BooleanField(
        description="   ",
        null=True,
        source_field="isFullPage"
    )
    
    order = fields.IntField(
        default=999,
        description="",
        null=True,
        source_field="order"
    )

    # ====================  # (description)
    
    authTitle = fields.CharField(
        max_length=255,
        description="",
        null=True,
        source_field="authTitle"
    )
    
    authMark = fields.CharField(
        max_length=255,
        description="Permission Identifier (e.g. user:btn:add)",
        null=True,
        source_field="authMark"
    )

    # ====================  # (description)

    min_user_type = fields.SmallIntField(
        default=3,
        description="0$1$2   $3",
        source_field="min_user_type"
    )
    """
    ?
    - 0  
    - 1?
    - 2   ?
    - 3?
    """
    
    remark = fields.CharField(
        max_length=500,
        description="",
        null=True,
        source_field="remark"
    )

    class Meta:
        table = "system_permission"
        table_description = "System Permission Table"

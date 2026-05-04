

from enum import IntEnum
from .sa_orm import fields
from .common import BaseModel


class NotificationType(IntEnum):
    """"""
    LOGIN = 0       # 
    ANNOUNCEMENT = 1  #    
    MESSAGE = 2     # 


class NotificationScope(IntEnum):
    """"""
    ALL = 0         #       
    DEPARTMENT = 1  #    
    USER = 2        #    


class NotificationStatus(IntEnum):
    """Notification status"""
    DRAFT = 0       # 
    PUBLISHED = 1   # ?
    REVOKED = 2     # ?


class SystemNotification(BaseModel):
    """System Notification Table"""
    
    title = fields.CharField(max_length=200, description="Notification Title")
    content = fields.TextField(description="Notification Content")
    type = fields.SmallIntField(default=2, description="Type (0=Login, 1=Announcement, 2=System Message)")
    scope = fields.SmallIntField(default=0, description="Scope (0=All, 1=Department, 2=User)")
    scope_ids = fields.JSONField(null=True, description="Scope ID List (department IDs or user IDs)")
    status = fields.SmallIntField(default=0, description="Status (0=Draft, 1=Published, 2=Revoked)")
    priority = fields.SmallIntField(default=0, description="Priority (0=Normal, 1=Important, 2=Urgent)")
    publish_time = fields.DatetimeField(null=True, description="Publish Time")
    expire_time = fields.DatetimeField(null=True, description="Expire Time")
    creator = fields.ForeignKeyField(
        "system.SystemUser",
        related_name="created_notifications",
        on_delete=fields.SET_NULL,
        null=True,
        description="Creator"
    )
    
    class Meta:
        table = "system_notification"
        table_description = "System Notification Table"
        ordering = ["-created_at"]


class UserNotification(BaseModel):
    """User Notification Relation Table"""
    
    notification = fields.ForeignKeyField(
        "system.SystemNotification",
        related_name="user_notifications",
        on_delete=fields.CASCADE,
        description="Notification"
    )
    user = fields.ForeignKeyField(
        "system.SystemUser",
        related_name="notifications",
        on_delete=fields.CASCADE,
        description="User"
    )
    is_read = fields.BooleanField(default=False, description="Is Read")
    read_time = fields.DatetimeField(null=True, description="Read Time")
    
    class Meta:
        table = "user_notification"
        table_description = "User Notification Table"
        unique_together = [("notification", "user")]
        ordering = ["-created_at"]

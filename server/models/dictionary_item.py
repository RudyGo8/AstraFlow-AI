

from .sa_orm import fields
from .common import BaseModel


class SystemDictionaryItem(BaseModel):
    """
    鏁版嵁瀛楀吀椤硅
    """

    dictionary_id = fields.ForeignKeyField(
        "system.SystemDictionary",
        related_name="items",
        null=False,
        description="鎵灞炲瓧鍏窱D",
        source_field="dictionary_id",
        on_delete=fields.CASCADE
    )
    """
    鎵灞炲瓧鍏窱D
    """
    label = fields.CharField(
        max_length=100,
        null=False,
        description="Dictionary Item Label",
        source_field="label"
    )
    """
    瀛楀吀椤规爣绛?
    """
    value = fields.CharField(
        max_length=100,
        null=False,
        description="Dictionary Item Value",
        source_field="value"
    )
    """
    瀛楀吀椤瑰?
    """
    status = fields.IntField(
        null=False,
        default=1,
        description="Status (1 enabled, 0 disabled)",
        source_field="status"
    )
    """
    鐘舵侊紙1鍚敤锛?绂佺敤锛?
    """
    sort = fields.IntField(
        null=False,
        default=0,
        description="Sort Order (smaller is higher)",
        source_field="sort"
    )
    """
    鎺掑簭锛堟暟瀛楄秺灏忚秺闈犲墠锛?
    """
    tag_color = fields.CharField(
        max_length=50,
        null=True,
        description="鏍囩棰滆壊",
        source_field="tag_color"
    )
    """
    鏍囩棰滆壊
    """
    remark = fields.TextField(
        null=True,
        description="澶囨敞",
        source_field="remark"
    )
    """
    澶囨敞
    """

    class Meta:
        table = "system_dictionary_item"
        table_description = "鏁版嵁瀛楀吀椤硅"
        ordering = ["sort", "-created_at"]

from .sa_orm import fields
from .common import BaseModel


class SystemDictionaryItem(BaseModel):
    """数据字典项模型。"""

    dictionary_id = fields.ForeignKeyField(
        "system.SystemDictionary",
        related_name="items",
        null=False,
        description="所属字典 ID",
        source_field="dictionary_id",
        on_delete=fields.CASCADE,
    )
    """
    所属字典 ID。
    """

    label = fields.CharField(
        max_length=100,
        null=False,
        description="字典项标签",
        source_field="label",
    )
    """
    字典项标签。
    """

    value = fields.CharField(
        max_length=100,
        null=False,
        description="字典项值",
        source_field="value",
    )
    """
    字典项值。
    """

    status = fields.IntField(
        null=False,
        default=1,
        description="状态（1 启用，0 禁用）",
        source_field="status",
    )
    """
    状态。
    """

    sort = fields.IntField(
        null=False,
        default=0,
        description="排序值，数值越小越靠前",
        source_field="sort",
    )
    """
    排序值。
    """

    tag_color = fields.CharField(
        max_length=50,
        null=True,
        description="标签颜色",
        source_field="tag_color",
    )
    """
    标签颜色。
    """

    remark = fields.TextField(
        null=True,
        description="备注",
        source_field="remark",
    )
    """
    备注。
    """

    class Meta:
        table = "system_dictionary_item"
        table_description = "数据字典项表"
        ordering = ["sort", "-created_at"]

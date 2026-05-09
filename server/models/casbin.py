from .sa_orm import fields

from .common import BaseModel


class CasbinRule(BaseModel):
    """
    Casbin 策略规则表。

    用于存储 RBAC 权限策略，支持：
    - p：策略规则（policy）
    - g：分组规则（grouping）

    示例：
    - p, role_admin, /api/users, GET
    - g, user_123, role_admin
    """

    ptype = fields.CharField(
        max_length=255,
        description="规则类型（p=policy，g=grouping）",
        source_field="ptype",
    )

    v0 = fields.CharField(
        max_length=255,
        null=True,
        description="第一个参数，通常表示 sub 或角色",
        source_field="v0",
    )

    v1 = fields.CharField(
        max_length=255,
        null=True,
        description="第二个参数，通常表示 obj 或资源",
        source_field="v1",
    )

    v2 = fields.CharField(
        max_length=255,
        null=True,
        description="第三个参数，通常表示 act 或 HTTP 方法",
        source_field="v2",
    )

    v3 = fields.CharField(
        max_length=255,
        null=True,
        description="第四个参数，预留扩展字段",
        source_field="v3",
    )

    v4 = fields.CharField(
        max_length=255,
        null=True,
        description="第五个参数，预留扩展字段",
        source_field="v4",
    )

    v5 = fields.CharField(
        max_length=255,
        null=True,
        description="第六个参数，预留扩展字段",
        source_field="v5",
    )

    class Meta:
        table = "casbin_rule"
        table_description = "Casbin Rule Table"
        ordering = ["-created_at"]

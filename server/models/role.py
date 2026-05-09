from .sa_orm import fields

from .common import BaseModel


class SystemRole(BaseModel):
    """
    角色模型。

    权限管理基于 Casbin：
    - 菜单/按钮权限：`p, role_code, permission_id, menu|button`
    - API 权限：`p, role_code, /api/path/*, GET|POST|...`
    - 用户与角色关联：`g, user_id, role_code`
    """

    name = fields.CharField(
        max_length=255,
        description="角色名称",
        source_field="role_name",
    )
    """
    角色名称。
    - 允许重名，不同部门可以存在同名角色
    - 最大长度为 255 个字符
    - 映射到数据库字段 role_name
    """

    code = fields.CharField(
        max_length=255,
        unique=True,
        description="角色编码",
        source_field="role_code",
    )
    """
    角色编码。
    - 用于系统内部唯一标识角色
    - 必须唯一
    - 最大长度为 255 个字符
    - 映射到数据库字段 role_code
    """

    description = fields.CharField(
        max_length=255,
        null=True,
        description="角色描述",
        source_field="role_description",
    )
    """
    角色描述。
    - 最大长度为 255 个字符
    - 允许为空
    - 映射到数据库字段 role_description
    """

    status = fields.SmallIntField(
        default=1,
        description="角色状态",
        source_field="status",
    )
    """
    角色状态。
    - 1：启用
    - 0：禁用
    - 映射到数据库字段 status
    """

    department = fields.ForeignKeyField(
        "system.SystemDepartment",
        related_name="roles",
        null=True,
        description="所属部门",
        source_field="department_id",
    )
    """
    所属部门。
    - 表示角色所属的部门
    - 为 null 时表示全局角色
    - 映射到数据库字段 department_id
    """

    class Meta:
        table = "system_role"
        table_description = "System Role Table"
        ordering = ["-created_at"]

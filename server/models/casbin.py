
from .sa_orm import fields

from .common import BaseModel


class CasbinRule(BaseModel):
    """
    Casbin 绛栫暐瑙勫垯琛?
    瀛樺偍 RBAC 鏉冮檺绛栫暐锛屾敮鎸?p (policy) 鍜?g (grouping) 瑙勫垯
    
    p 瑙勫垯绀轰緥: p, role_admin, /api/users, GET  (瑙掕壊瀵硅祫婧愮殑璁块棶鏉冮檺)
    g 瑙勫垯绀轰緥: g, user_123, role_admin  (鐢ㄦ埛涓庤鑹茬殑鍏宠仈)
    """
    
    ptype = fields.CharField(
        max_length=255,
        description="绛栫暐绫诲瀷 (p=policy, g=grouping)",
        source_field="ptype"
    )
    
    v0 = fields.CharField(
        max_length=255,
        null=True,
        description="绗竴涓弬鏁?(閫氬父鏄?sub/瑙掕壊)",
        source_field="v0"
    )
    
    v1 = fields.CharField(
        max_length=255,
        null=True,
        description="绗簩涓弬鏁?(閫氬父鏄?obj/璧勬簮璺緞)",
        source_field="v1"
    )
    
    v2 = fields.CharField(
        max_length=255,
        null=True,
        description="绗笁涓弬鏁?(閫氬父鏄?act/HTTP鏂规硶)",
        source_field="v2"
    )
    
    v3 = fields.CharField(
        max_length=255,
        null=True,
        description="绗洓涓弬鏁?(鎵╁睍瀛楁)",
        source_field="v3"
    )
    
    v4 = fields.CharField(
        max_length=255,
        null=True,
        description="绗簲涓弬鏁?(鎵╁睍瀛楁)",
        source_field="v4"
    )
    
    v5 = fields.CharField(
        max_length=255,
        null=True,
        description="绗叚涓弬鏁?(鎵╁睍瀛楁)",
        source_field="v5"
    )

    class Meta:
        table = "casbin_rule"
        table_description = "Casbin Rule Table"
        ordering = ["-created_at"]

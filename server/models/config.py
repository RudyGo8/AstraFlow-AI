
from .sa_orm import fields

from .common import BaseModel


class ConfigGroup:
    """閰嶇疆鍒嗙粍甯搁噺"""
    SYSTEM = "system"       # 绯荤粺鍩虹閰嶇疆
    EMAIL = "email"         # 閭欢閰嶇疆
    MAP = "map"             # 鍦板浘閰嶇疆
    UPLOAD = "upload"       # 涓婁紶閰嶇疆
    SECURITY = "security"   # 瀹夊叏閰嶇疆
    ACCOUNT = "account"     # 璐埛閰嶇疆


class SystemConfig(BaseModel):
    """
    绯荤粺閰嶇疆妯瀷
    """
    name = fields.CharField(
        max_length=100,
        description="閰嶇疆鍚嶇О",
        source_field="name"
    )
    """
    閰嶇疆鍚嶇О銆?
    - 鏈澶ч暱搴︿负 100 涓瓧绗?
    - 鏄犲皠鍒版暟鎹簱瀛楁 name
    """
    key = fields.CharField(
        max_length=100,
        description="閰嶇疆閿悕",
        source_field="key"
    )
    """
    閰嶇疆閿悕銆?
    - 鏈澶ч暱搴︿负 100 涓瓧绗?
    - 鏄犲皠鍒版暟鎹簱瀛楁 key
    """
    value = fields.TextField(
        description="Config Value",
        source_field="value"
    )
    """
    閰嶇疆鍊笺?
    - 浣跨敤 TextField 鏀寔闀挎枃鏈?
    - 鏄犲皠鍒版暟鎹簱瀛楁 value
    """
    group = fields.CharField(
        max_length=50,
        default="system",
        null=True,
        description="閰嶇疆鍒嗙粍",
        source_field="group_name"
    )
    """
    閰嶇疆鍒嗙粍銆?
    - 鐢ㄤ簬鍖哄垎涓嶅悓绫诲瀷鐨勯厤缃?
    - 榛樿涓?system
    - 鍙负绌猴紙鍏煎鏃ф暟鎹級
    """
    type = fields.BooleanField(
        default=False,
        description="绯荤粺鍐呯疆",
        source_field="type"
    )
    """
    鏄惁涓虹郴缁熷唴缃?
    - 榛樿涓轰笉鏄?
    """
    remark = fields.TextField(
        null=True,
        description="澶囨敞",
        source_field="remark"
    )
    """
    澶囨敞淇伅銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗?
    - 鍙负绌?
    """

    class Meta:
        table = "system_config"
        table_description = "System Config Table"


from .sa_orm import fields

from .common import BaseModel


class SystemUser(BaseModel):
    """
    System User Model
    """

    username = fields.CharField(
        max_length=255,
        description="Username",
        source_field="username"
    )
    """
    鐢ㄦ埛鍚嶃?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 username銆?
    """

    password = fields.CharField(
        max_length=255,
        description="瀵嗙爜",
        source_field="password"
    )
    """
    瀵嗙爜銆?
    - 瀛樺偍鍔犲瘑鍚庣殑瀵嗙爜銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 password銆?
    """

    email = fields.CharField(
        max_length=255,
        null=True,
        description="閭",
        source_field="email"
    )
    """
    閭銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 email銆?
    """

    phone = fields.CharField(
        max_length=30,
        null=True,
        description="Phone Number",
        source_field="phone"
    )
    """
    鎵嬫満鍙枫?
    - 鏈澶ч暱搴︿负 30 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 phone銆?
    """

    nickname = fields.CharField(
        max_length=255,
        null=True,
        description="鏄电О",
        source_field="nickname"
    )
    """
    鏄电О銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 nickname銆?
    """

    avatar = fields.CharField(
        max_length=512,
        null=True,
        description="澶村儚",
        source_field="avatar"
    )
    """
    澶村儚銆?
    - 鏈澶ч暱搴︿负 512 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 avatar銆?
    """

    gender = fields.SmallIntField(
        default=0,
        description="鎬у埆锛?鏈煡锛?鐢凤紝2濂筹級",
        source_field="gender"
    )
    """
    鎬у埆銆?
    - 0锛氭湭鐭?
    - 1锛氱敺
    - 2锛氬コ
    - 榛樿涓?0銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 gender銆?
    """

    status = fields.SmallIntField(
        default=1,
        description="User Status (1 enabled, 0 disabled)",
        source_field="status"
    )
    """
    鐢ㄦ埛鐘舵併?
    - 1锛氬惎鐢?
    - 0锛氱鐢?
    - 榛樿涓?1銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 status銆?
    """

    user_type = fields.SmallIntField(
        default=3,
        description="鐢ㄦ埛韬唤鏍囪瘑锛?瓒呯骇绠$悊鍛橈紝1绠$悊鍛橈紝2閮ㄩ棬绠$悊鍛橈紝3鏅氱敤鎴凤級",
        source_field="user_type"
    )
    """
    鐢ㄦ埛韬唤鏍囪瘑銆?
    - 0锛氳秴绾х鐞嗗憳锛堟渶楂樻潈闄愶紝鍙鐞嗘墍鏈夎祫婧愶級
    - 1锛氱鐞嗗憳锛堝彲绠$悊澶氫釜閮ㄩ棬鍜岀郴缁熼厤缃級
    - 2锛氶儴闂ㄧ鐞嗗憳锛堝彲绠$悊鎵灞為儴闂ㄥ強涓嬪睘閮ㄩ棬锛?
    - 3锛氭櫘閫氱敤鎴凤紙鍙兘鏌ョ湅鍜屾搷浣滆嚜宸辩殑鏁版嵁锛?
    - 榛樿涓?3锛堟櫘閫氱敤鎴凤級銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 user_type銆?
    """

    department = fields.ForeignKeyField(
        "system.SystemDepartment",
        related_name="users",
        null=True,
        description="Belongs To Department",
        source_field="department_id"
    )
    """
    鎵灞為儴闂ㄣ?
    - 澶栭敭鍏宠仈鍒?SystemDepartment 琛ㄣ?
    - 濡傛灉涓?null锛屽垯琛ㄧず鐢ㄦ埛鏈垎閰嶉儴闂ㄣ?
    - 鏄犲皠鍒版暟鎹簱瀛楁 department_id銆?
    """

    class Meta:
        table = "system_user"
        table_description = "System User Table"
        ordering = ["-created_at"]


class SystemUserRole(BaseModel):
    """
    鐢ㄦ埛瑙掕壊涓棿琛ㄣ?
    """

    user = fields.ForeignKeyField(
        "system.SystemUser",
        related_name="user_roles",
        source_field="user_id",
        description="鐢ㄦ埛ID",
        on_delete=fields.CASCADE,
        null=True,
        default=None
    )
    role = fields.ForeignKeyField(
        "system.SystemRole",
        related_name="user_roles",
        source_field="role_id",
        on_delete=fields.CASCADE,
        null=True,
        default=None
    )

    class Meta:
        table = "system_user_role"
        table_description = "System User Role Table"

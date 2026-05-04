
from .sa_orm import fields

from .common import BaseModel


class SystemRole(BaseModel):
    """
    瑙掕壊琛ㄦā鍨嬨?
    
    鏉冮檺绠$悊璇存槑锛圕asbin 鏂规C锛夛細
    - 瑙掕壊鏉冮檺瀹屽叏鐢?Casbin 绠$悊锛屼笉鍐嶄娇鐢ㄤ腑闂磋
    - 鑿滃崟/鎸夐挳鏉冮檺: p, role_code, permission_id, menu|button
    - API鏉冮檺: p, role_code, /api/path/*, GET|POST|...
    - 鐢ㄦ埛-瑙掕壊鍏宠仈: g, user_id, role_code
    """

    name = fields.CharField(
        max_length=255,
        description="瑙掕壊鍚嶇О",
        source_field="role_name"
    )
    """
    瑙掕壊鍚嶇О銆?
    - 鍏佽閲嶅锛屽洜涓轰笉鍚岄儴闂ㄥ彲鑳芥湁鐩稿悓鐨勮鑹插悕绉般?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 role_name銆?
    """

    code = fields.CharField(
        max_length=255,
        unique=True,
        description="瑙掕壊缂栫爜",
        source_field="role_code"
    )
    """
    瑙掕壊缂栫爜銆?
    - 鐢ㄤ簬绯荤粺鍐呴儴璇嗗埆瑙掕壊銆?
    - 蹇呴』鍞竴銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 role_code銆?
    """

    description = fields.CharField(
        max_length=255,
        null=True,
        description="瑙掕壊鎻忚堪",
        source_field="role_description"
    )
    """
    瑙掕壊鎻忚堪銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 role_description銆?
    """

    status = fields.SmallIntField(
        default=1,
        description="Role Status",
        source_field="status"
    )
    """
    瑙掕壊鐘舵併?
    - 1: 姝e父
    - 0: 绂佺敤
    - 鏄犲皠鍒版暟鎹簱瀛楁 status銆?
    """

    department = fields.ForeignKeyField(
        "system.SystemDepartment",
        related_name="roles",
        null=True,
        description="Belongs To Department",
        source_field="department_id"
    )
    """
    鎵灞為儴闂ㄣ?
    - 琛ㄧず瑙掕壊鎵灞炵殑閮ㄩ棬銆?
    - 濡傛灉涓?null锛屽垯琛ㄧず瑙掕壊鏄叏灞瑙掕壊銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 department_id銆?
    """

    class Meta:
        table = "system_role"
        table_description = "System Role Table"
        ordering = ["-created_at"]

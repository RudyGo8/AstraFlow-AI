
from .sa_orm import fields

from .common import BaseModel


class SystemLoginLog(BaseModel):
    """
    System Login Log Model
    """

    user_id = fields.ForeignKeyField(
        "system.SystemUser",
        related_name="login_logs",
        description="鐢ㄦ埛ID",
        source_field="user_id"
    )
    """
    鐢ㄦ埛ID銆?
    - 澶栭敭鍏宠仈鍒?User 琛ㄣ?
    - 鏄犲皠鍒版暟鎹簱瀛楁 user_id銆?
    """

    login_ip = fields.CharField(
        max_length=256,
        description="鐧诲綍IP鍦板潃",
        source_field="login_ip"
    )
    """
    鐧诲綍IP鍦板潃銆?
    - 鏈澶ч暱搴︿负 50 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 login_ip銆?
    """

    login_location = fields.CharField(
        max_length=255,
        null=True,
        description="Login Location",
        source_field="login_location"
    )
    """
    鐧诲綍鍦扮偣銆?
    - 鏍规嵁 IP 鍦板潃瑙f瀽鐨勫湴鐞嗕綅缃俊鎭?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 login_location銆?
    """

    browser = fields.CharField(
        max_length=255,
        null=True,
        description="Browser Type",
        source_field="browser"
    )
    """
    娴忚鍣ㄧ被鍨嬨?
    - 璁板綍鐢ㄦ埛鐧诲綍鏃朵娇鐢ㄧ殑娴忚鍣ㄧ被鍨嬨?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 browser銆?
    """

    os = fields.CharField(
        max_length=255,
        null=True,
        description="鎿嶄綔绯荤粺",
        source_field="os"
    )
    """
    鎿嶄綔绯荤粺銆?
    - 璁板綍鐢ㄦ埛鐧诲綍鏃朵娇鐢ㄧ殑鎿嶄綔绯荤粺銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 os銆?
    """

    status = fields.SmallIntField(
        default=1,
        description="Login Status (1 success, 0 failure)",
        source_field="status"
    )
    """
    鐧诲綍鐘舵併?
    - 1锛氭垚鍔?
    - 0锛氬け璐?
    - 榛樿涓?1銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 status銆?
    """

    session_id = fields.CharField(
        max_length=36,
        null=True,
        description="浼氳瘽ID",
        source_field="session_id"
    )
    """
    浼氳瘽ID銆?
    - 璁板綍鐢ㄦ埛鐧诲綍鏃剁殑浼氳瘽ID銆?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 session_id銆?
    """

    class Meta:
        table = "system_login_log"
        table_description = "System Login Log Table"
        ordering = ["-created_at"]


class SystemOperationLog(BaseModel):
    """
    鎿嶄綔鏃ュ織琛ㄦā鍨嬨?
    """

    operation_name = fields.CharField(
        max_length=255,
        description="鎿嶄綔鍚嶇О",
        source_field="operation_name"
    )
    """
    鎿嶄綔鍚嶇О銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 operation_name銆?
    """

    operation_type = fields.SmallIntField(
        description="鎿嶄綔绫诲瀷锛堝鍒犳敼鏌ワ級",
        source_field="operation_type"
    )
    """
    鎿嶄綔绫诲瀷銆?
    - 澧炪佸垹銆佹敼銆佹煡绛夋搷浣滅被鍨嬨?
    - 鏈澶ч暱搴︿负 50 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 operation_type銆?
    """

    request_path = fields.TextField(
        description="璇锋眰璺緞",
        source_field="request_path"
    )
    """
    璇锋眰璺緞銆?
    - 璁板綍鐢ㄦ埛璇锋眰鐨?API 璺緞銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 request_path銆?
    """

    request_method = fields.CharField(
        max_length=10,
        description="璇锋眰鏂规硶",
        source_field="request_method"
    )
    """
    璇锋眰鏂规硶銆?
    - 璁板綍鐢ㄦ埛璇锋眰鐨?HTTP 鏂规硶锛堝 GET銆丳OST銆丳UT銆丏ELETE锛夈?
    - 鏈澶ч暱搴︿负 10 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 request_method銆?
    """

    operator = fields.ForeignKeyField(
        "system.SystemUser",
        related_name="operation_logs",
        null=True,
        description="鎿嶄綔浜哄憳",
        source_field="operator_id"
    )
    """
    鎿嶄綔浜哄憳銆?
    - 澶栭敭鍏宠仈鍒?User 琛ㄣ?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 operator_id銆?
    """

    host = fields.CharField(
        max_length=50,
        description="涓绘満鍦板潃",
        source_field="host"
    )
    """
    涓绘満鍦板潃銆?
    - 璁板綍鐢ㄦ埛璇锋眰鐨?IP 鍦板潃銆?
    - 鏈澶ч暱搴︿负 50 涓瓧绗︺?
    - 鏄犲皠鍒版暟鎹簱瀛楁 host銆?
    """

    location = fields.CharField(
        max_length=255,
        null=True,
        description="鎿嶄綔鍦扮偣",
        source_field="location"
    )
    """
    鎿嶄綔鍦扮偣銆?
    - 鏍规嵁 IP 鍦板潃瑙f瀽鐨勫湴鐞嗕綅缃俊鎭?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 location銆?
    """

    user_agent = fields.TextField(
        null=True,
        description="User Agent",
        source_field="user_agent"
    )
    """
    鐢ㄦ埛璇锋眰澶淬?
    - 璁板綍鐢ㄦ埛璇锋眰鐨?User-Agent 淇伅銆?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 user_agent銆?
    """

    browser = fields.CharField(
        max_length=255,
        null=True,
        description="Browser Type",
        source_field="browser"
    )
    """
    娴忚鍣ㄧ被鍨嬨?
    - 璁板綍鐢ㄦ埛鐧诲綍鏃朵娇鐢ㄧ殑娴忚鍣ㄧ被鍨嬨?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 browser銆?
    """

    os = fields.CharField(
        max_length=255,
        null=True,
        description="鎿嶄綔绯荤粺",
        source_field="os"
    )
    """
    鎿嶄綔绯荤粺銆?
    - 璁板綍鐢ㄦ埛鐧诲綍鏃朵娇鐢ㄧ殑鎿嶄綔绯荤粺銆?
    - 鏈澶ч暱搴︿负 255 涓瓧绗︺?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 os銆?
    """

    request_params = fields.TextField(
        null=True,
        description="璇锋眰鍙傛暟",
        source_field="request_params"
    )
    """
    璇锋眰鍙傛暟銆?
    - 璁板綍鐢ㄦ埛璇锋眰鐨勫弬鏁帮紙浠绘剰鏍煎紡锛屽瀛楃涓层丣SON銆乆ML 绛夛級銆?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 request_params銆?
    """

    response_result = fields.TextField(
        null=True,
        description="杩斿洖缁撴灉",
        source_field="response_result"
    )
    """
    杩斿洖缁撴灉銆?
    - 璁板綍鎿嶄綔鐨勮繑鍥炵粨鏋滐紙浠绘剰鏍煎紡锛屽瀛楃涓层丣SON銆乆ML 绛夛級銆?
    - 鍏佽涓虹銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 response_result銆?
    """

    status = fields.SmallIntField(
        default=1,
        description="Operation Status (1 success, 0 failure)",
        source_field="status"
    )
    """
    鎿嶄綔鐘舵併?
    - 1锛氭垚鍔?
    - 0锛氬け璐?
    - 榛樿涓?1銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 status銆?
    """

    cost_time = fields.FloatField(
        default=0,
        description="Cost Time (ms)",
        source_field="cost_time"
    )
    """
    娑堣楁椂闂淬?
    - 璁板綍鎿嶄綔娑堣楃殑鏃堕棿锛堝崟浣嶏細姣锛夈?
    - 榛樿涓?0銆?
    - 鏄犲皠鍒版暟鎹簱瀛楁 cost_time銆?
    """

    class Meta:
        table = "system_operation_log"
        table_description = "System Operation Log Table"
        ordering = ["-created_at"]

# _*_ coding : UTF-8 _*_
# @Time : 2025/08/01 00:14
# @Author : sonder
# @File : config.py
# @Software : PyCharm
# @Comment :  # (description)
import datetime
import os
from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Dict, Any

import yaml
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    """
    ?
    AML   ?
    """

    @classmethod
    def from_yaml(cls, yaml_data: Dict[str, Any]) -> "BaseConfig":
        """
        AMLf

        :param yaml_data: YAML  ?
        :return: ?
        """
        return cls.model_validate(yaml_data)


class AppSettings(BaseConfig):
    """
    ?
    $c?
    """
    env: str = 'dev'
    """
    
    - 'dev'   ?
    - 'prod'    
      
    """

    name: str = 'FastAPI-Vue-Admin'
    """
    Application name
    Used in API docs title, logs, and service identification
    Recommended to set as business-related name (e.g. "User Management System")
    """

    api_prefix: str = '/dev-api'
    """
    API   
    - /dev-api
    - ?apiURL
    h   
    """

    api_status_enabled: bool = True
    """
         ?
    - True/health  o   $?
    - False   ?
    """

    host: str = '0.0.0.0'
    """
    Application bind host address
    - '0.0.0.0': Listen on all network interfaces (default, suitable for server deployment)
    - '127.0.0.1': Local access only (suitable for local development)
    Production should be configured based on network security policies
    """

    port: int = 9090
    """
    e
    - ?-65535
    - ?0/443   o?
    - g?0/443
    """

    version: str = '1.0.0'
    """
    Application version number
    Follows semantic versioning (major.minor.patch)
    Used in API docs, log output, and version control
    """

    reload: bool = True
    """
    g
    - Trueg   ?
    - False  
    ?
    """

    ip_location_enabled: bool = True
    """
    IP   
    - TrueAPI      ?
    - False
    PI    
    """

    multi_login_allowed: bool = True
    """
    Allow multiple logins from different devices
    - True: allowed (default, user-friendly)
    - False: new login kicks out old session (more secure)
    """

    init_database: bool = True
    """
    
    - True      
    - False   
    """


class JwtSettings(BaseConfig):
    """
    JWT   ?
    $      ?
    """
    secret_key: str = 'FastAPI-Vue-Admin'
    """
    JWT   ?
            
    -          
    -    ?2
    penssl rand -hex 32
    """

    algorithm: str = 'HS256'
    """
    JWT
    -   S256   S384S512   ?
    - RS256S384  
       ?
    """

    salt: str = 'FastAPI-Vue-Admin'
    """
    JWT?
    ecret_key           ?
    ecret_key
    """

    expire_minutes: int = 1440
    """
    JWT   ?
    - 1440=24
    - ?0=1   
    
    """

    redis_expire_minutes: int = 30
    """
          edis
             
    expire_minutesedis
    """


class DatabaseSettings(BaseConfig):
    """
       
    $SQLAlchemy
    """
    engine: str = "mysql"
    """
    Database instance engine type
    Specify the database type to connect to:
    - 'mysql': MySQL database (default)
    - 'postgresql': PostgreSQL database
    - 'sqlite': SQLite database (file-based, no server needed)
    - 'oracle': Oracle database
    Different engines correspond to different drivers and connection parameters
    """

    host: str = "127.0.0.1"
    """
    Database host address
    - Local: 'localhost' or '127.0.0.1' (default)
    - Remote: server IP address or domain (e.g. db.prod.com)
    - SQLite: no need to set (ignored)
    """

    port: int = 3306
    """
    Database port
    - MySQL: 3306 (default)
    - PostgreSQL: 5432
    - Oracle: 1521
    - SQLite: auto-ignored
    Must match database server configuration
    """

    username: str = 'root'
    """
    Database login username
    - Dev: usually root (high privileges for debugging)
    - Prod: must use minimal privilege user
    SQLite: file permissions controlled by OS
    """

    password: SecretStr = SecretStr('root')
    """
    Database login password (sensitive)
    - Dev: can use simple password (e.g. root)
    - Prod: must use strong password
    """

    database: str = 'FVA'
    """
    Database name
    - Relational DB (MySQL/PostgreSQL): database name (e.g. FVA_prod)
    - SQLite: database file path (e.g. ./data/app.db)
    Ensure database is created (SQLite auto-creates file)
    """

    pool_size: int = 10
    """
    Database connection pool size
    Controls concurrent connections:
    - Dev: 5-10 (sufficient for debugging)
    - Prod: adjust based on concurrency (20-50, not too large)
    Too large pools consume excessive database resources
    """

    pool_timeout: int = 30
    """
    Connection pool timeout (seconds)
    Throws exception if connection not obtained within timeout
    Recommended: 30 seconds
    """

    echo: bool = False
    """
    Print SQL execution log
    - True: print all SQL statements and params (dev debugging)
    - False: no print (prod must disable for performance and security)
    """

    charset: str = "utf8mb4"
    """
    Database charset
    - MySQL: recommend utf8mb4 (supports emoji, 4-byte chars)
    - PostgreSQL: usually UTF8
    """

    timezone: str = "Asia/Shanghai"
    """
    Database timezone setting
    Affects time field storage and queries
    Default: 'Asia/Shanghai' (China Standard Time)
    Should match application server timezone to avoid time shift
    """

    @field_validator('engine')
    def validate_engine(cls, v):
        """
        ?

        :param v:   
        :return:   
        :raises ValueError: 
        """
        supported = ['mysql', 'postgresql', 'sqlite']
        if v not in supported:
            raise ValueError("Unsupported database engine: {} - supported: {}".format(v, supported))
        return v


class RedisSettings(BaseConfig):
    """
    RedisRedis?
    $
    """
    mode: str = 'server'
    """
    Redis
    - 'server'   Redis?
    """
    
    host: str = 'redis'
    """
    Redis host address (only effective in server mode)
    - Local: '127.0.0.1' (default)
    - Remote: server IP address or domain
    """

    port: int = 6379
    """
    Redis port number (only effective in server mode)
    Default: 6379 (Redis standard port)
    """

    password: SecretStr = SecretStr('')
    """
    Rediserver?
    -    ?
    - 
    """

    database: int = 1
    """
    Redis0-15?server?
    -   0?
    -    select?
       ey
    """

    max_connections: int = 10
    """
    Redis     server?
    edis   maxclients
       Redis
    """

    socket_timeout: int = 5
    """
    Rediserver?
       ?
    ??
    """

    retry_on_timeout: bool = True
    """
    server?
    - True        
    - False
            
    """
    
    @field_validator('mode')
    def validate_mode(cls, v):
        """Redis mode validation"""
        supported = ['server']
        if v not in supported:
            raise ValueError(f"Redis: {v}: {supported}")
        return v


class UploadSettings(BaseConfig):
    """
    ?
    SSCOS
    """
    storage_type: str = 'local'
    """
       ?
    - 'local'
    - 'aliyun_oss'OSS
    - 'tencent_cos'COS
    - 'aws_s3'WS S3
    ?
    """

    allowed_extensions: List[str] = [
        'bmp', 'gif', 'jpg', 'jpeg', 'png', 'webp',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'pdf', 'txt', 'html', 'htm',
        'rar', 'zip', '7z', 'gz', 'bz2',
        'mp4', 'avi', 'mov', 'flv', 'mkv',
        'mp3', 'wav', 'flac'
    ]
    """
    Allowed file extension list for upload (excluding dot prefix)
    Used for file type validation, prevents malicious file uploads
    Adjust based on business needs (e.g. exclude .exe etc.)
    """

    max_file_size: int = 100
    """
    Maximum file size limit (MB)
    Default 100MB, adjust based on business needs
    - Images: 5-10MB
    - Videos: 100-500MB
    Large files should use chunked upload
    """

    upload_node: str = 'node-A'
    """
    
    
       node-Aode-B?
       
    """

    local_upload_path: str = 'data/local_uploads'
    """
    torage_type=local
    /var/app/uploads?
       ?
    """

    local_download_path: str = 'data/local_downloads'
    """
    torage_type=local
          ?
    """

    local_url_prefix: str = '/uploads'
    """
    RLtorage_type=local
    ?uploads?uploads/2023/10/file.jpg
    eb?
    """

    cloud_access_key: Optional[str] = None
    """
    AKccess Key?
       API        AccessKey?
    ?
    """

    cloud_secret_key: Optional[SecretStr] = None
    """
    SKecret Key
    KPI
       ?
    """

    cloud_endpoint: Optional[str] = None
    """
    Endpoint
    ?ndpoint
    - SSss-cn-beijing.aliyuncs.com
    - OSos.ap-shanghai.myqcloud.com
    ndpoint
    """

    cloud_timeout: int = 30
    """
    API
      60
    """

    cloud_bucket: Optional[str] = None
    """
    Bucket?
            
    Bucket     ?
    """

    cloud_path_prefix: str = 'uploads/'
    """
    
         ucketser_avatars/ogs/?
       ploads/
    """

    cloud_domain: Optional[str] = None
    """
    
    CDNhttps://cdn.yourdomain.com
       ttps://bucket.endpoint?
    """

    def __init__(self, **data):
        super().__init__(**data)
        if self.storage_type == 'local':
            self._ensure_local_dirs()

    def _ensure_local_dirs(self):
        """Ensure local storage directories exist"""
        os.makedirs(self.local_upload_path, exist_ok=True)
        os.makedirs(self.local_download_path, exist_ok=True)

    def get_file_url(self, file_key: str) -> str:
        """
        URL

        :param file_key: 2023/10/avatar.jpg?
        :return:    URL?
        """
        if self.storage_type == 'local':
            return f"{self.local_url_prefix}/{file_key}"
        elif self.storage_type in ['aliyun_oss', 'tencent_cos', 'aws_s3']:
            if self.cloud_domain:
                return f"{self.cloud_domain}/{self.cloud_path_prefix}{file_key}"
            return f"https://{self.cloud_bucket}.{self.cloud_endpoint}/{self.cloud_path_prefix}{file_key}"
        raise ValueError(f": {self.storage_type}")

    def get_storage_path(self, file_key: str) -> str:
        """
        

        :param file_key: 
        :return: ey
        """
        return os.path.join(self.local_upload_path, file_key) if self.storage_type == 'local' \
            else f"{self.cloud_path_prefix}{file_key}"


class EmailSettings(BaseConfig):
    """
    ?
    $   ?
    """
    username: str = ''
    """
    SMTP   
    notify@yourdomain.com?
    """

    password: SecretStr = SecretStr('')
    """
    ?
    - QQ?63   MTP
    -    MTP
    """

    host: str = 'smtp.qq.com'
    """
    SMTP server address
    Different email providers have different addresses:
    - QQ: smtp.qq.com
    - 163: smtp.163.com
    - Enterprise: smtp.exmail.qq.com
    """

    port: int = 465
    """
    SMTP server port
    - 465: SSL encrypted port (recommended, default)
    - 587: TLS encrypted port
    Must match the email provider SMTP port
    """

    from_addr: str = ''
    """
    Sender address (displayed email address)
    Usually matches username, must comply with email provider standards
    Example: "System Notification" <notify@yourdomain.com>
    """


class MapSettings(BaseConfig):
    """
    ?
    $APIP
    """
    ak: str = ''
    """
    AKccess Key?
            ?
    - -$--AK
    - -$--Key
    """

    sk: SecretStr = SecretStr('')
    """
    SKecret Key
          IPK
    K  ?
    """

    provider: str = 'baidu'
    """
    ?
    - 'baidu'?
    - 'amap'?
    API   
    """


class ConfigLoader:
    """
    
    config.yaml?
    """

    def __init__(self):
        self.config = self._load_yaml_file()  # YAML

    def _load_yaml_file(self) -> Dict[str, Any]:
        """
        config.yaml

        :return: 
        :raises FileNotFoundError: ?
        """
        #  # (description)
        #  # (description)
        current_file = Path(__file__)
        project_root = current_file.parent.parent
        config_path = project_root / "config.yaml"

        #  # (description)
        if not config_path.exists() or not config_path.is_file():
            raise FileNotFoundError(f"   : {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        return config

    @lru_cache(maxsize=None)
    def app(self) -> AppSettings:
        """ """
        return AppSettings.from_yaml(self.config.get('app', {}))

    @lru_cache(maxsize=None)
    def jwt(self) -> JwtSettings:
        """JWT   """
        return JwtSettings.from_yaml(self.config.get('jwt', {}))

    @lru_cache(maxsize=None)
    def database(self) -> DatabaseSettings:
        """Database configuration"""
        db_data = self.config.get('database', {})
        return DatabaseSettings.from_yaml(db_data)

    @lru_cache(maxsize=None)
    def redis(self) -> RedisSettings:
        """Redis"""
        redis_data = self.config.get('redis', {})
        return RedisSettings.from_yaml(redis_data)

    @lru_cache(maxsize=None)
    def upload(self) -> UploadSettings:
        """ """
        return UploadSettings.from_yaml(self.config.get('upload', {}))

    @lru_cache(maxsize=None)
    def email(self) -> EmailSettings:
        """ """
        return EmailSettings.from_yaml(self.config.get('email', {}))

    @lru_cache(maxsize=None)
    def map(self) -> MapSettings:
        """ """
        return MapSettings.from_yaml(self.config.get('map', {}))


    def to_dict(self) -> Dict[str, Any]:
        """Export config as dict"""
        return _clean_config_data(self.config)

    def export_to_yaml(self, file_path: str):
        """AML"""
        export_config_to_yaml(self.to_dict(), file_path)

    def _update_nested_dict(self, target: Dict, key_path: List[str], value: Any) -> None:
        """
        ?

        :param target: 
        :param key_path: ?["database", "nodes", "0", "host"]?
        :param value: ?
        """
        if len(key_path) == 1:
            #  # (description)
            key = key_path[0]
            if isinstance(target, list) and key.isdigit():
                key = int(key)
            target[key] = value
            return

        #  # (description)
        current_key = key_path[0]
        #  # (description)
        if isinstance(target, list) and current_key.isdigit():
            current_key = int(current_key)

        #  # (description)
        if current_key not in target:
            #  # (description)
            next_key = key_path[1]
            target[current_key] = [] if next_key.isdigit() else {}

        self._update_nested_dict(target[current_key], key_path[1:], value)

    def set_config_value(self, key: str, value: Any) -> None:
        """
           ?

        :param key:  "database.nodes.0.host"?
        :param value: ?
        """
        # 1.  # (description)
        key_path = key.split(".")
        if not key_path:
            raise ValueError("Key cannot be empty")

        # 2.  # (description)
        self._update_nested_dict(self.config, key_path, value)

        # 3.  # (description)
        for method in [self.app, self.jwt, self.database, self.redis, self.upload, self.email, self.map]:
            method.cache_clear()


def _clean_config_data(data: Any) -> Any:
    """
    Pydantic        ?

    :param data: ydantic   ?
    :return: ?
    """
    #  # (description)
    if hasattr(data, "model_dump"):
        data = data.model_dump()

    #  # (description)
    if isinstance(data, list):
        return [_clean_config_data(item) for item in data]

    #  # (description)
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            #  # (description)
            if key.startswith("__"):
                continue
            #  # (description)
            # if isinstance(value, SecretStr):
            #     cleaned[key] = "***PROTECTED***"  #  # (description)
            # else:
            cleaned[key] = _clean_config_data(value)
        return cleaned

    #  # (description)
    return data


def export_config_to_yaml(
        config: Dict[str, Any],
        file_path: str,
        include_comments: bool = True
) -> None:
    """
    YAML

    :param config: config.merged_config?
    :param file_path: 
    :param include_comments:    
    """
    #  # (description)
    cleaned_data = _clean_config_data(config)

    #  # (description)
    content: List[str] = []

    #  # (description)
    if include_comments:
        content.extend([
            "# Auto-generated config file",
            f"# Generated at: {datetime.datetime.now().isoformat()}",
            "# Note: sensitive info replaced with placeholder",
            "",
        ])

    #  # (description)
    modules = [
        ("app", ""),
        ("jwt", "JWT   "),
        ("database", "Database configuration"),
        ("redis", "Redis"),
        ("upload", ""),
        ("email", ""),
        ("map", ""),
        ("elasticsearch", "Elasticsearch")
    ]

    for module, desc in modules:
        if module not in cleaned_data:
            continue

        #  # (description)
        content.extend([
            f"# {desc}",
            f"{module}:"
        ])

        #  # (description)
        if module == "database" and "nodes" in cleaned_data[module]:
            content.append("  # ")
            for key, value in cleaned_data[module].items():
                if key == "nodes":
                    continue  # 
                content.append(f"  {key}: {value}")

            #  # (description)
            content.extend([
                "  # Database global configuration",
                "  nodes:"
            ])
            for node in cleaned_data[module]["nodes"]:
                content.extend([
                    f"    - # Node: {node['alias']} ({node['engine']})",
                    f"      alias: {node['alias']!r}",
                    f"      engine: {node['engine']!r}",
                    f"      host: {node['host']!r}",
                    f"      port: {node['port']}",
                    f"      username: {node['username']!r}",
                    f"      password: {node['password']!r}",
                    f"      database: {node['database']!r}",
                    f"      pool_size: {node['pool_size']}",
                    f"      pool_timeout: {node['pool_timeout']}",
                    f"      echo: {node['echo']}",
                    "      extra_options:"
                ])
                #  # (description)
                for opt_key, opt_val in node["extra_options"].items():
                    content.append(f"        {opt_key}: {opt_val!r}")
                content.append("")  # ?

        #  # (description)
        elif module == "redis" and "cluster_nodes" in cleaned_data[module]:
            content.append("  # Redis   ")
            for key, value in cleaned_data[module].items():
                if key == "cluster_nodes":
                    continue  # 
                content.append(f"  {key}: {value}")

            #  # (description)
            content.extend([
                "  # Rediscluster_mode=true",
                "  cluster_nodes:"
            ])
            for node in cleaned_data[module]["cluster_nodes"]:
                content.extend([
                    f"    - host: {node['host']!r}",
                    f"      port: {node['port']}"
                ])
            content.append("")

        #  # (description)
        else:
            module_data = cleaned_data[module]
            for key, value in module_data.items():
                #  # (description)
                if isinstance(value, list):
                    content.append(f"  {key}:")
                    for item in value:
                        content.append(f"    - {item!r}")
                else:
                    content.append(f"  {key}: {value!r}" if isinstance(value, str) else f"  {key}: {value}")
            content.append("")  # ?

    #  # (description)
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f": {file_path}")


#  # (description)
config = ConfigLoader()

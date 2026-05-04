import json
from typing import Optional

from sqlalchemy import text

from models.sa_orm import _DB, init_orm


def register(mcp):
    @mcp.tool()
    async def execute_sql(sql: str, params: Optional[str] = None) -> str:
        sql_upper = sql.strip().upper()
        if not sql_upper.startswith("SELECT"):
            return json.dumps({"error": "Only SELECT statements are allowed"}, ensure_ascii=False)

        dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER", "CREATE"]
        if any(k in sql_upper for k in dangerous):
            return json.dumps({"error": "Dangerous SQL keyword detected"}, ensure_ascii=False)

        await init_orm()
        bind_params = json.loads(params) if params else {}
        if isinstance(bind_params, list):
            bind_params = {}

        async with _DB.session_factory() as session:
            result = await session.execute(text(sql), bind_params)
            rows = [dict(r) for r in result.mappings().all()]

        return json.dumps({"count": len(rows), "data": rows}, default=str, ensure_ascii=False)

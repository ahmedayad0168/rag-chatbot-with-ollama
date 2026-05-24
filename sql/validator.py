import re

BLOCKED = {"DROP", "ALTER", "TRUNCATE", "EXEC", "EXECUTE", "CREATE"}

WRITE_QUERIES = {"INSERT", "UPDATE", "DELETE"}

_REQUIRE_WHERE = WRITE_QUERIES - {"INSERT"}


def clean_sql(sql):
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "")
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip()


def validate_sql(sql):
    sql = clean_sql(sql)
    keyword = sql.split()[0].upper()

    if keyword in BLOCKED:
        return False, f"{keyword} is blocked"

    if keyword in _REQUIRE_WHERE and "WHERE" not in sql.upper():
        return False, "WHERE clause required for UPDATE/DELETE"

    return True, "OK"
"""Install missing input procedures without resetting tables or existing routines."""
from pathlib import Path
import re
from mysql.connector import connect
from config import MYSQL


def install_missing_procedures(password):
    source = (Path(__file__).parent / "sql" / "nhap-lieu-khach-san.sql").read_text(encoding="utf-8-sig")
    definitions = re.findall(
        r"^(CREATE PROCEDURE\s+(\w+)\b.*?^END\s*//)", source, re.MULTILINE | re.DOTALL
    )
    if len(definitions) != 1 or definitions[0][1] != "ThemKhachHang":
        raise ValueError("Không đọc được thủ tục ThemKhachHang từ sql/nhap-lieu-khach-san.sql.")
    installed = []
    with connect(**MYSQL, password=password) as connection:
        with connection.cursor() as cursor:
            for definition, name in definitions:
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.ROUTINES "
                    "WHERE ROUTINE_SCHEMA = DATABASE() AND ROUTINE_NAME = %s "
                    "AND ROUTINE_TYPE = 'PROCEDURE'", (name,)
                )
                if cursor.fetchone()[0]:
                    continue
                # DELIMITER is a Workbench directive, not part of CREATE SQL.
                cursor.execute(definition.rsplit("//", 1)[0].rstrip())
                while cursor.nextset():
                    pass
                installed.append(name)
    return installed

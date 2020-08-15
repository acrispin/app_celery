from time import time
import psutil
import pyodbc

from src.db import get_connection

"""
https://github.com/mkleehammer/pyodbc/issues/802
"""

# cuando 'varchar_limit' es '100', la memoria es constante, cuando es 'MAX', la memoria incrementa con cada iteracion
varchar_limit = "MAX"
print(f"using varchar({varchar_limit})")

print(f"pyodbc {pyodbc.version}")
cnxn = get_connection()
process = psutil.Process()


def print_status(msg, _t0=None):
    s = f"{msg}: "
    mb = process.memory_info().vms / 1048576
    s += f"vms {mb:0.1f} MiB"
    if _t0:
        _diff = time() - _t0
        s += f", {_diff*1000:,.2f} ms - {_diff:0.1f} seg."
    print(s)


print_status("startup")
num_rows = 10_000
data = [(i + 1, f"col{i + 1:06}", 3.14159265 * (i + 1)) for i in range(num_rows)]
print_status("data loaded")
print(data[0])

table_name = "pd_test"
col_names = ["id", "txt_col", "float_col"]
ins_sql = f"INSERT INTO {table_name} ({','.join(col_names)}) VALUES ({','.join('?' * len(col_names))})"

for iteration in range(5):
    t0 = time()
    crsr = cnxn.cursor()
    crsr.execute(f"DROP TABLE IF EXISTS {table_name}")
    crsr.execute(f"CREATE TABLE {table_name} (id int, txt_col varchar({varchar_limit}), float_col float(53))")
    crsr.fast_executemany = True
    crsr.executemany(ins_sql, data)
    crsr.close()
    # cnxn.commit()
    print_status(f"iteration {iteration + 1}", t0)

"""
python -m tests.insert_masive_tests
"""
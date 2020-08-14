import pyodbc as pyodbc
from decouple import config

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

DB_SERVER = config('DB_SERVER', default='localhost')
DB_PORT = config('DB_PORT', default='')
DB_NAME = config('DB_NAME', default='dbname')
DB_USER = config('DB_USER', default='username')
DB_PASSWORD = config('DB_PASSWORD', default='password')

# https://github.com/mkleehammer/pyodbc/wiki/The-pyodbc-Module#timeout
DB_CONNECTION_TIMEOUT = 6
# https://github.com/mkleehammer/pyodbc/wiki/Connection#timeout
DB_QUERY_TIMEOUT = 3600

# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver15
if DB_PORT:
    CONN_STR = f'DRIVER={{ODBC Driver 17 for SQL Server}};' \
               f'SERVER={DB_SERVER},{DB_PORT};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};'
else:
    CONN_STR = f'DRIVER={{ODBC Driver 17 for SQL Server}};' \
               f'SERVER={DB_SERVER};DATABASE={DB_NAME};UID={DB_USER};PWD={DB_PASSWORD};'
"""
Download ODBC Driver for SQL Server
https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
Download for Windows
https://go.microsoft.com/fwlink/?linkid=2137027
Download for Linux
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
Download for macOS
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15

# install ODBC Driver 17 for SQL Server: https://www.microsoft.com/en-us/download/details.aspx?id=56567
CONN_STR = 'DRIVER={ODBC Driver 17 for SQL Server};Server=%s,%s;port=%s;Database=%s;uid=%s;pwd=%s;' \
           % (DB_SERVER, DB_PORT, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)

CONN_STR = 'DRIVER={SQL Server Native Client 10.0};' \
           'Server=%s,%s;port=%s;Network Library=DBMSSOCN;Database=%s;uid=%s;pwd=%s;' \
         % (DB_SERVER, DB_PORT, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD)
"""


def get_info(_cnxn, _sql):
    try:
        with _cnxn.cursor() as _cur:
            _cur.execute(_sql)
            _val = _cur.fetchval()
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f'rowcount: {_cur.rowcount}, sql: {_sql}')
        return str(_val)
    except pyodbc.DatabaseError as err:
        logger.exception(err)
    except Exception as _ex:
        logger.exception(_ex)
    return None


def check_conection(_cnxn):
    logger.debug("Verificando conexion a bd")
    if not _cnxn:
        _cnxn = get_connection()
    try:
        with _cnxn.cursor() as _cur:
            _cur.execute("SELECT 1;")
        return True
    except pyodbc.DatabaseError as err:
        logger.exception(err)
    except Exception as _ex:
        logger.exception(_ex)
    return False


def get_connection(_autocommit=False):
    try:
        _cnxn = pyodbc.connect(CONN_STR, autocommit=_autocommit, timeout=DB_CONNECTION_TIMEOUT)
        _cnxn.timeout = DB_QUERY_TIMEOUT
        return _cnxn
    except pyodbc.DatabaseError as err:
        logger.exception(err)
        raise err
    except Exception as _ex:
        logger.exception(_ex)
        raise _ex
    return None


def info_connection(_autocommit=False):
    logger.info("Obteniendo informacion de conexion a bd.")
    cnxn = get_connection(_autocommit)
    servername = get_info(cnxn, "SELECT @@SERVERNAME;")
    username = get_info(cnxn, "SELECT SUSER_SNAME();")
    spid = get_info(cnxn, "SELECT @@SPID;")
    version = get_info(cnxn, "SELECT @@VERSION")
    return f"servername:'{servername}', username:'{username}', spid:'{spid}', version:'{version}'"


if __name__ == '__main__':
    logger.info("Iniciando conexion a base de datos.")
    try:
        logger.info("Conexion a base de datos correcta, info db: " + info_connection())
    except Exception as ex:
        logger.error("Error en conexion a base de datos")
        logger.error(ex)

"""
En la raiz del proyecto ejecutar, db.py debe estar en la carpeta src/
$ python -m src.db
"""

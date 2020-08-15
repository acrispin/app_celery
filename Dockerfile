FROM python:3.7 AS base

ENV PYTHONUNBUFFERED 1

# CONFIGURACION PARA EL DRIVER MSSQL, DEBIAN 10
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15#debian17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update -y \
    && ACCEPT_EULA=Y apt-get install msodbcsql17 -y \
    && ACCEPT_EULA=Y apt-get install mssql-tools -y \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && /bin/bash -c "source ~/.bashrc" \
    && apt-get install unixodbc-dev -y \
    && apt-get install libgssapi-krb5-2 -y
# https://github.com/microsoft/msphpsql/issues/1023
RUN apt-get update -yqq \
    && apt-get install -y --no-install-recommends openssl \
    && sed -i 's,^\(MinProtocol[ ]*=\).*,\1'TLSv1',g' /etc/ssl/openssl.cnf \
    && sed -i 's,^\(CipherString[ ]*=\).*,\1'DEFAULT@SECLEVEL=1',g' /etc/ssl/openssl.cnf\
    && rm -rf /var/lib/apt/lists/*
# CONFIGURACION PARA EL DRIVER MSSQL, DEBIAN 10


FROM base AS release

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./src/*.py /app/src/
# COPY ./.env.example /app/.env
COPY ./flowerconfig.py /app/flowerconfig.py
COPY ./main.py /app/main.py
COPY ./run_task.py /app/run_task.py
COPY ./info.sql /app/info.sql

WORKDIR /app/

# Se indicara en el docker-compose
#EXPOSE 5000
#ENTRYPOINT ["python"]
#CMD ["-m","src.api"]

FROM python:3.7

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./src/*.py /app/src/
# COPY ./.env.example /app/.env
COPY ./flowerconfig.py /app/flowerconfig.py
COPY ./main.py /app/main.py
COPY ./run_task.py /app/run_task.py

WORKDIR /app/

# Se indicara en el docker-compose
#EXPOSE 5000
#ENTRYPOINT ["python"]
#CMD ["-m","src.api"]

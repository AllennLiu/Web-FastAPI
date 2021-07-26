FROM python:3.7

ENV workdir=/usr/src

COPY . /usr/src

WORKDIR $workdir

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

EXPOSE 7788

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7788"]

FROM python:3.10

COPY ./requirements.txt ./wb_limit/requirements.txt

RUN pip install -r ./wb_limit/requirements.txt

EXPOSE 8000

COPY ./ ./wb_limit/

CMD ["uvicorn", "wb_limit.app:server", "--host", "0.0.0.0", "--port", "8000"]
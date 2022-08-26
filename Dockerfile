FROM python:3.10

WORKDIR /backend

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8804

COPY . ./

CMD ["uvicorn", "app:server", "--host", "0.0.0.0", "--port", "8804"]
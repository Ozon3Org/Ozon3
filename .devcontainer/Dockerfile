FROM python:3.9

COPY requirements.txt  /temp/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./temp/requirements.txt && \
    rm -rf ./temp

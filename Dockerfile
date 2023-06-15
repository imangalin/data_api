FROM osgeo/gdal:ubuntu-small-latest
ARG PIPENV_PARAMS=""
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install python3-pip --fix-missing
WORKDIR /data_api
COPY . ./
RUN pip install -r requirements.txt

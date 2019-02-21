FROM python:3.6-alpine

RUN pip --no-cache-dir install pipenv

COPY Pipfile Pipfile.lock /app/

WORKDIR /app

# --no-cache option allows to not cache the index locally, which is useful for keeping containers small.
#            Literally it equals apk update in the beginning and rm -rf /var/cache/apk/* in the end.
# --virtual  defines the name of
RUN apk add --no-cache --virtual build-dependencies alpine-sdk libffi-dev openssl-dev \
    && pipenv install --system --deploy \
    && apk del build-dependencies

COPY groundhog.py /app

RUN pip uninstall pipenv virtualenv virtualenv-clone -y

CMD ["python", "groundhog.py"]

FROM python:3.6-alpine

# Set timezone
ENV TZ="Europe/Berlin"
RUN apk add --no-cache tzdata
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip --no-cache-dir install pipenv

COPY Pipfile Pipfile.lock /app/

WORKDIR /app

# --no-cache: allows to not cache the index locally, which is useful for keeping containers small.
#             Literally it equals apk update in the beginning and rm -rf /var/cache/apk/* in the end.
# --virtual   defines the name of the succeeding dependency list -> used in `apk del` to
#             delete all the dependencies
RUN apk add --no-cache --virtual build-deps alpine-sdk libffi-dev openssl-dev \
    && pipenv install --system --deploy \
    && apk del build-deps

COPY *.py /app/

RUN pip uninstall -y pipenv virtualenv virtualenv-clone

CMD ["python", "groundhog.py"]

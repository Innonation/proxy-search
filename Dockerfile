FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y build-essential

COPY . /Data

RUN pip install -r /Data/requirements.txt

CMD ["/Data/Start.sh"]

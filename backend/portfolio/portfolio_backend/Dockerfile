

FROM python:3.13-slim-bullseye
LABEL author='Manvendra'

WORKDIR /usr/src/portfolio_backend

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/portfolio_backend/entrypoint.sh
#RUN chmod +x ./entrypoint.sh

COPY . .

#ENTRYPOINT ["/usr/src/portfolio_backend/entrypoint.sh"]

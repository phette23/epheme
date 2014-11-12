FROM ubuntu:latest
MAINTAINER phette23 <phette23@gmail.com>
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git mongodb cron python
# Twitter API credentials
# these environment variables are used by twarc
ENV CONSUMER_KEY "83y6Hnh6L8xWb1BBct7q9Q"
ENV CONSUMER_SECRET "FWrr7SnATssAUqglYwOcdLrwYrupq3B2qAIR4ZiQZqc"
ENV ACCESS_TOKEN "83880390-Xx5s8B67ZfjDBOe5YcwJuHG1GtdvmfKlAcFX2VWIO"
ENV ACCESS_TOKEN_SECRET "agqNQcBq5hUQXOjj3FrdX7MysYR6QVJE9EnX65dK7HDJt"
RUN git clone https://github.com/phette23/epheme /epheme
# NB: can remove this line once entrypoint.sh is in GitHub repo
ADD ./entrypoint.sh /entrypoint.sh
# mongodb default port
EXPOSE 27017
# cues up epheme to run every hour via cron
ENTRYPOINT ./entrypoint.sh
# run mongo in the background
CMD ["mongod", "--config=/epheme/mongo.conf"]

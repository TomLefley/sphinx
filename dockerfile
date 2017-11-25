FROM ubuntu:latest
MAINTAINER Tom Lefley "thomas.lefley@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /sphinx
WORKDIR /sphinx
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["sphinx.py"]

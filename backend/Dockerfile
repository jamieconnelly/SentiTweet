FROM python:2.7-onbuild

RUN apt-get update
# RUN apt-get -y install python-pip python-numpy python-scipy \
#	python-matplotlib python-pandas python-sklearn python-nltk
RUN apt-get -y install python-pip
RUN pip install tweepy

EXPOSE 5000
CMD ["gunicorn", "--config=gunicorn.py", "app:app"]
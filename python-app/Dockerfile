FROM python:3.4-onbuild

#RUN apt-get update
#RUN apt-get -y install python-pip python-numpy python-scipy python-matplotlib python-pandas python-sklearn python-nltk
EXPOSE 80
CMD ["gunicorn", "--config=gunicorn.py", "app:app"]
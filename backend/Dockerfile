FROM python:2.7-onbuild

RUN python -m nltk.downloader stopwords

EXPOSE 5000
CMD ["gunicorn", "--config=gunicorn.py", "app:app"]
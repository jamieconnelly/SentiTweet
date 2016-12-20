FROM python:2.7-onbuild

RUN python -m nltk.downloader stopwords wordnet maxent_treebank_pos_tagger punkt averaged_perceptron_tagger
# RUN mkdir tokenizers

EXPOSE 5000
CMD ["gunicorn", "--config=gunicorn.py", "app:app"]
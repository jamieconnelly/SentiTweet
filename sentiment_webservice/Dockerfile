FROM python:2.7-onbuild

ENV APP_CONFIG='/usr/src/app/config/app/settings.py'
RUN python -m nltk.downloader stopwords wordnet maxent_treebank_pos_tagger punkt averaged_perceptron_tagger
RUN find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
# RUN py.test tests/ -v

ENTRYPOINT uwsgi --ini ./config/uwsgi/uwsgi.ini
import os
import multiprocessing

if os.environ.get('MODE') == 'dev':
    reload = True

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:5000'
timeout = 120

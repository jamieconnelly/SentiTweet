# SentiVis
Sentiment analysis and visualisation of twitter data

Requirements
------------
- Python 2.7
- pip (`sudo easy_install pip` or `brew install python`)
- virtualenv (`sudo pip install virtualenv` _installs globally_)
- docker
[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
[Mac](https://docs.docker.com/docker-for-mac/install/)
[Windows](https://docs.docker.com/docker-for-windows/install/#download-docker-for-windows)
- docker-compose (`pip install docker-compose`)

The `brew` command is available on OS X after you have installed [Homebrew]

[Homebrew]: http://brew.sh/

Install (required for running classifier CLI)
---------------------------------------------
1. Go into the project root directory : `cd SentiVis`
1. Create and activate virtualenv: `virtualenv --python python2.7 .venv && . .venv/bin/activate`
1. Install Python packages: `pip install -r requirements.txt`

### On Windows (cmd.exe terminal)

1. Go into the project root directory : `cd SentiVis`
1. Create virtualenv: `virtualenv .venv`
1. Activate virtualenv: `.venv\Scripts\activate`
1. Install Python packages: `pip install -r requirements.txt`


Running the web application
---------------------------

    # from project root
    docker-compose up

    # once running visit `localhost` in a browser


Stopping the web application
---------------------------

    # in terminal
    ctrl + c

    # then
    docker-compose down -v


Running the classifier CLI
---------------------------

    # from project root
    cd classifier

    # note either -o (--obj-sub) or -p (--pos-neg) must be included as an option
    python main.py -o

    # options
    -h, --help     show this help message and exit
    -o, --obj-sub  train objective vs subjective classifier
    -p, --pos-neg  train positive vs negative classifier
    -t, --tfidf    print tfidf matrix
    -s, --save     save vocabulary and model


Please note that the training/test data could not be included in this repository
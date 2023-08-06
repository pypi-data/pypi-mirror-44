Thai Segmentation Webapp
========================

## Setup

Install requirements:

Currently only needs **Python3** with `Flask` (and `gevent` as wsgi container). Additionally use pylint for code and style checks.

```bash
conda create -n thai python=3  # create conda environment
conda activate thai
pip install pylint Flask gevent
# for later use cases ...
# conda install pytest pytest-cov flake8 jupyter matplotlib numpy pandas tabulate  # optional, for later
# conda install -c conda-forge flask-caching jupyter_contrib_nbextensions cython  # optional, for later
```

Setup project:

```bash
git clone git@git.informatik.uni-leipzig.de:koerner/thai-sentword-segment.git
cd thai-sentword-segment/
cd thai-segmentation-webapp/
# cp -r ../thai_sentence_segmentation/prepro segmenter  # (only for me once)
```

## Run

```bash
python app.py
```

Or in background:

```bash
screen -dmS thai  # create screen
screen -r thai  # attach to screen, next command (below) will be run in screen
python app.py
# Press [Ctrl]+[D] to detach from screen, so that it is in the background
```

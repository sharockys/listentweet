# listentweet
![Tests](https://github.com/sharockys/listentweet/actions/workflows/pythonapp.yml/badge.svg)

ListenTweet is a tool that uses tweetpy to retreive tweets from twitter and analyzes them using NLP techniques of subjects of your choices.

## Quick Start

crete `.env` on the home directory of this project. Example:

```bash
API_KEY=[API KEY]
API_SECRET=[API SECRET]
ACCESS_TOKEN=[ACCESS TOKEN]
ACCESS_TOKEN_SECRET=[ACCESS TOKEN SECRET]
```

You should create your own Twitter developper account to obtain these tokens so that you can use the twitter related part of this project.

## Checklist:

- [x] Tweet Retriever
- [x] Tweet Streamer
- [ ] Kafka integration
- [ ] Database - MongoDB?
- [ ] SpaCy Basic Pipelines
- [ ] Stanza Basic Pipelines
- [ ] Scaled F-score
- [ ] NLTK Keywords extractions
- [ ] Transformers based vectorization
- [ ] Umap dimension reduction
- [ ] HDBSCAN with BERT embeddings + Word Mover Distance
- [ ] Sentiment Analysis
- [ ] Zero-shot classification
- [ ] Fine-tune BERT with tweets
- [ ] new vocabulary discovery
- [ ] Dashboard visualization on daily basis

## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

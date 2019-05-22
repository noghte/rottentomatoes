# Rotten Tomatoes Crawler

This program crawls audience reviews and critic reviews from given URLs of the https://rottentomatoes.com website

## Prerequisites

### Using pip

```
pip install requests
pip install lxml
```

### Using conda
```
conda install requests
conda install lxml
```

### Config
There are a few variables before the main() method (including URLs) that you can change:
* allow_extract_critics
* allow_extract_audience
* page_limit
* ctitic_review_prefix
* url_list


## Run

`python app.py`

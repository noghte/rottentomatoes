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
There are a few parameters that you can set:
* allow_extract_critics
* allow_extract_audience
* page_limit
* urls_file


## Run

- With default values: `python app.py`
- With the `page_limit` parameter: `python app.py --page_limit 10`

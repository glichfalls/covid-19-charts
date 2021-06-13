# Covid-19 Charts

data fetched from the "Our World in Data" Covid-19 repository. (https://github.com/owid/covid-19-data)

## installation

``pip install -r requirements.txt``

## configuration

create config file `config.py` with database credentials:

```
db_credentials = dict(
    host='',
    database='',
    user='',
    password=''
)
```

## usage

### data fetching

``python3 fetcher.py [-h --help -v --verbose]``

### visualize

``python3 visualize.py``
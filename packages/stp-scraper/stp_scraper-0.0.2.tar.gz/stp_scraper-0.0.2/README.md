[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/stp-scraper/badge.svg?branch=stp-script&t=V0q7kh)](https://coveralls.io/github/cuenca-mx/stp-scraper?branch=stp-script)

# stp-scraper
STP scraper library for obtaining all transactions given a range of dates.

## Requirements
Python 3.7+

## Installation
```bash
pip install stp_scraper
```

## Tests
```bash
make test
```

## Basic usage
Get transactions of prior week
```python
import stp_scraper
stp_scraper.extract(None, None)
```

Get transactions for specific dates
```python
import stp_scraper
stp_scraper.extract('01/02/2019', '15/02/2019')
```

# [VIVOHarvester](https://pypi.org/project/VIVOHarvester/)

# Installation
```
pip install VIVOHarvester
```
or
```
git clone git@github.com:VTUL/VIVOHarvester.git
python setup.py install
```

# Usage:
* Harvest data from Elements (Default)
```
vivotool -f local.yml -t harvest -d 0
```

* Harvest data from Elements a day ago (Current time -1 day)
```
vivotool -f local.yml -t harvest -d 1
```

* Import RDF data into a VIVO instance
```
vivotool -f local.yml -t ingest
```

* Fetch user_map.csv
```
vivotool -f local.yml -t getuser
```
or
```
vivotool -f local.yml -t getuser -o yourpath/yourfilename
```

# Database creation
* Create require database
```
vivotool -f local.yml -t db
```

# Upgrade to newer version
```
pip uninstall VIVOHarvester
pip install VIVOHarvester==0.1.2 (e.g.)
```

# Testing
```
py.test --cov=vivotool test/
coverage report -m
coverage report
```


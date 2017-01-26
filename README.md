# SEARCH ENGINE

## RELEASE
Version 1 - Page rank : [HERE](https://github.com/kalaww/search_engine/releases)

## INSTALLATION
Require Python 2

Install the dependencies

```sh
$ pip install -r requirements.txt
```

## RUN
Run the program with :
```sh
$ python run.sh [options]
```

#### PAGE RANK
The page rank command line :
```sh
$ python run.sh pagerank [options]
```
Options :
```sh
Options:
  -h, --help            show this help message and exit
  -g FILE, --graph=FILE
                        FILE that contains a graph
  -v, --verbose         verbose mode
  -e EPSILON, --epsilon=EPSILON
                        page rank epsilon [default: 0.0001]
  -z ZAP, --zap=ZAP     zap factor [default: 0.0]
  -o FILE, --output=FILE
                        FILE to store the page rank vector [default: stdout]
  -s, --step            print number of step
  -a STARTER, --starter=STARTER
                        starter vertex for the page rank vector [default: 0]
```


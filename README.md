# SEARCH ENGINE

## RELEASE
- Version 1 - Page rank : [LINK](https://github.com/kalaww/search_engine/releases/tag/1.0)
- Version 2 - Page rank + Collector : [LINK](https://github.com/kalaww/search_engine/releases/tag/2.0)

## INSTALLATION
Require Python 3

Install the dependencies

```
$ pip3 install -r requirements.txt
```

## RUN
Run the program with :
```
$ python3 run.py [options]
```

#### PAGE RANK
The page rank command line :
```
$ python3 run.py pagerank [options]
```
###### OPTIONS
```
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
                        starter vertex for the page rank vector: index of the
                        vertex or 'all' for all vertices [default: all]
```

#### COLLECTOR
The french dictionary used for this collector is in 'data/dictionary.fr.csv' [LINK](https://github.com/Kalaww/search_engine/blob/master/data/dictionary.fr.csv)

You can check how I generate this dictionary with this Jupyter Notebook 'generate_dictionary.ipynb' (watchable on GitHub) [LINK](https://github.com/Kalaww/search_engine/blob/master/generate_dictionary.ipynb)

The collector creates three files : 
- 'id_to_page.csv' : relation page id -> page title
- 'page_links.txt' : relation page id -> links page id
- 'words_appearance.csv' : relation word id -> list(page id, word frequency)

In words_appearance.csv, each word in the title of the page (and in the dictionary used) add 1.0 to the word frequency.
It might help for a stronger classification of the pages (if a keyword is in the page title, it might be a highly relevant page)

The collector command line :
```
$ python3 run.py collector [options]
```
###### OPTIONS
```
Options:
  -h, --help            show this help message and exit
  -w FILE, --wiki=FILE  FILE that contains a wiki dump
  -o FILE, --output-dir=FILE
                        FILE output directory where to store collected data
  -d FILE, --dictionary=FILE
                        FILE words dictionary in csv
  -i VALUE, --print-interval=VALUE
                        print progress each VALUE lines [default: 100000]
  -l LINES, --line-count=LINES
                        specify the number of lines in the wiki file, it avoid
                        the programm to look for it
```

###### EXAMPLES
You can test the collector with some partial part of the 'frwiki-20151226-pages-articles.xml'
- 100 000 first lines (11 MB): [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CNU9Zd2doVm16amc)
- 1 000 000 first lines (105 MB) : [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CX29XTnpmby11THc)
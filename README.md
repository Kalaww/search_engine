# SEARCH ENGINE

## RELEASE
- Version 1 - Page rank : [LINK](https://github.com/kalaww/search_engine/releases/tag/1.0)
- Version 2 - Page rank + Collector : [LINK](https://github.com/kalaww/search_engine/releases/tag/2.0)

## INSTALLATION
Require Python 3

To install the dependencies, type :

```
$ pip3 install -r requirements.txt
```

## RUN
Run the program with :
```
$ python3 run.py [options]
```

#### PAGE RANK

###### COMMAND LINE
```
$ python3 run.py pagerank [options]
```
###### OPTIONS
```
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
The french dictionary used for this collector is in `data/dictionary.fr.csv` 
[LINK](https://github.com/Kalaww/search_engine/blob/master/data/dictionary.fr.csv)

You can check how I generate this dictionary with this Jupyter Notebook `generate_dictionary.ipynb` (watchable on GitHub) 
[LINK](https://github.com/Kalaww/search_engine/blob/master/generate_dictionary.ipynb)

The collector creates three files : 
- `id_to_page.csv` : relation page id -> page title
- `page_links.txt` : relation page id -> links page id
- `words_appearance.csv` : relation word id -> list(page id)

For space efficiency, `words_appearance.csv` store the N page's id for each word with the highest frequency (N is 10 by 
default, but it can be change with option `-p N`).

Each words in the page's title add 1.0 to the word's frequency in this page. Therefore, this page will be more relevant for
the corresponding word.


###### COMMAND LINE
```
$ python3 run.py collector [options]
```
###### OPTIONS
```
  -h, --help            show this help message and exit
  -w FILE, --wiki=FILE  FILE that contains a wiki dump
  -o FILE, --output-dir=FILE
                        FILE output directory where to store collected data
  -d FILE, --dictionary=FILE
                        FILE words dictionary in csv
  -i VALUE, --print-interval=VALUE
                        print progress each VALUE lines [default: 100000]
  -l LINES, --line-count=LINES
                        specify the number of lines in the wiki file, it avoids
                        the programm to look for it
  -p NUMBER, --pages-per-word=NUMBER
                        NUMBER of pages per word to save [default: 10]
```

###### EXAMPLES
You can test the collector with some partial part of the 'frwiki-20151226-pages-articles.xml'
- 100 000 first lines (11 MB): [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CNU9Zd2doVm16amc)
- 1 000 000 first lines (105 MB) : [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CX29XTnpmby11THc)

#### SEARCH

###### COMMAND LINE
```
$ python3 run.py search [options]
```

###### OPTIONS
```
  -h, --help            show this help message and exit
  -d FILE, --dictionary=FILE
                        FILE words dictionary in csv
  -w FILE, --words-appearance=FILE
                        FILE words appearance in page filename
  -p FILE, --pagescore=FILE
                        FILE pagescore filename
  -i FILE, --id-to-page=FILE
                        FILE id-to-page filename
  -v, --verbose         verbose mode
```
# SEARCH ENGINE

## RELEASE
- Version 1 - Page rank : [LIEN](https://github.com/kalaww/search_engine/releases/tag/1.0)
- Version 2 - Page rank + Collector : [LIEN](https://github.com/kalaww/search_engine/releases/tag/2.0)
- Version 3 - Page rank + Collector + Seach : [LIEN](https://github.com/kalaww/search_engine/releases/tag/3.0)

## INSTALLATION
Requière Python 3

Pour installer les dépendances :

```
pip3 install -r requirements.txt
```

## EXECUTION
Lancer le programme avec :
```
python3 run.py [options]
```

#### PAGE RANK

###### COMMAND LINE
```
python3 run.py pagerank [options]
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
###### EXEMPLE
```
python3 run.py pagerank -s -g graph.txt -e 0.01 -z 0.15 -o page_score.txt
```

#### COLLECTOR
Le fichier contenant le dictionnaire français se situe : `data/dictionary.fr.csv` 
[LIEN](https://github.com/Kalaww/search_engine/blob/master/data/dictionary.fr.csv)

Vous pouvez regarder comment a été généré le dictionnaire avec ce Jupyter Notebook `generate_dictionary.ipynb` 
(visible sur GitHub) 
[LIEN](https://github.com/Kalaww/search_engine/blob/master/generate_dictionary.ipynb)

Le collector crée trois fichiers :
- `pageID_to_title.txt` : relation pageID -> page title
- `page_links.txt` : relation pageID -> links page id
- `words_appearance.txt` : relation word id -> list(pageID)

Pour controler la taille du `words_appearance.csv` généré, il ne garde que les N pageID pour chaque mot du dictionnaire 
qui ont la plus grande fréquence d'apparition dans la page (N vaut 10 par défaut, mais il peut être changé via l'option 
`-p N`).

Chaque mot contenu dans le titre des pages ajoute 1.0 à la fréquence d'apparition de ce mot dans la page. Ainsi, lors 
d'une recherche, les pages avec les mots recherchés auront plus de chance de ressortir dans les résultats.

Le programme affiche la progression du collector avec une estimation (peu précise) du temps restant. Pour celà, le 
programme commence par compter le nombre de ligne du fichier XML contenant l'archive wikipedia. Cette étape pouvant 
être évitée avec l'option `-l N` en précisant le nombre de ligne du fichier.

###### COMMAND LINE
```
python3 run.py collector [options]
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

###### EXEMPLE
```
python3 run.py collector -w wikifr.xml -o result_dir -d dictionary.csv -p 25
```
Quelques fichiers de test généré à partir de 'frwiki-20151226-pages-articles.xml'
- 100 000 premières lignes (11 MB): [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CNU9Zd2doVm16amc)
- 1 000 000 première lignes (105 MB) : [DOWNLOAD](https://drive.google.com/open?id=0BxjKLsDqc12CX29XTnpmby11THc)

#### SEARCH

Une fois le programme lancé, ont peut réaliser autant de recherche souhaitée. Chaque résultat est affiché et stocké dans 
un fichier nommé selon la requête.

Les résultats sont classé par pertinence. Le premier étant le plus pertinent et le dernier le moins pertinent (selon le 
pagerank).

Le programme search charge les fichiers : dictionnaire, apparence des mots et page score en mémoire. Le fichier de 
relation [pageID -> titre] est simplement lut une fois par recherche afin de traduire les pageID en titre.

Le nombre de résultat étant conditionné par le nombre de pageID par mot dans le fichier d'apparence des mots généré lors 
du collector. Ainsi, en modifiant la valeur par défaut (10) avec l'option `-p N` du collector, on obtiendra un nombre N 
de résultat au maximum.

###### COMMAND LINE
```commandline
python3 run.py search [options]
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

###### EXEMPLE
```commandline
python3 run.py search -d dictionary.csv -w words_appearance.txt -p pagescore.txt -i pageID_to_title.txt
```

###### EXEMPLE
```
  python3 run.py both \
    -w data/test0/frwiki-tst-1.xml \
    -o data/test0 \
    -z 0.15 \
    -e 0.01 \
    -s 
```
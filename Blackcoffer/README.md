## Objective

Objective of this assignment is to extract some sections (which are mentioned below) from SEC / EDGAR financial reports and perform text analysis to compute variables those are explained below. Link to SEC / EDGAR financial reports are given in excel spreadsheet “cik_list.xlsx”. 

## Packages Required :

- pandas
- urllib
- re
- BeautifulSoup

## How to run:

Put the following files in a same folder:
1. cik_list.xlsx
2. constraining_dictionary.xlsx
3. LoughranMcDonald_MasterDictionary_2016.csv
4. StopWords_Generic.txt
5. uncertainty_dictionary.xlsx
6. BlackcofferAssignment.py

Now run the BlackcofferAssignment.py file with the required packages with an active internet connection.
Wait some time as the program is going to fetch the large number of files and perform operations on them.
The output file will be generated.

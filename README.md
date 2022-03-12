# iamc-reports-parser

Scripts for parsing IAMC reports from https://www.iamc.com.ar/informediario/

## Requirements
- Python 3.x
- pdftotext https://www.xpdfreader.com/download.html

## Usage

1) Download pdf file from `https://www.iamc.com.ar/informediario/`
2) Convert it to txt file using `pdftotext`:

```
pdftotext -layout 741338.pdf
```
3) Convert to csv running:
```
python iamc_to_csv.py 741338.txt > output.csv
```
4) Check file content:
```
less output.csv

Especie,Serie,Tipo,Cubiertas,Opuestas,Cruzadas,Descubiertas,Total,Variación c/día anterior
AAPL,APLC31977A,CALL,0,0,0,20,20,0
AAPL,APLC3400AB,CALL,300,0,0,10,310,0
ALUA,ALUC100.MA,CALL,"1,300",0,0,0,"1,300",0
ALUA,ALUC100.AB,CALL,"12,500","3,000",0,"42,900","58,400","2,300"
ALUA,ALUC105.AB,CALL,"12,000","7,300",706,"17,794","37,800",0
ALUA,ALUC110.AB,CALL,"12,200","7,100",0,"4,200","23,500","2,500"
ALUA,ALUC115.AB,CALL,"1,500",700,0,"10,100","12,300",0
ALUA,ALUC59929A,CALL,"48,300","2,500",0,"45,800","96,600",0
ALUA,ALUC62929A,CALL,"49,600","7,200",190,"219,910","276,900","116,400"
ALUA,ALUC64929A,CALL,"326,500","14,400","4,638","303,662","649,200",-300
ALUA,ALUC76929A,CALL,"7,600",0,0,0,"7,600",0
ALUA,ALUC77929A,CALL,"9,500",0,0,500,"10,000",0
...
```
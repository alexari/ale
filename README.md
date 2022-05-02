# Retailsys - zkušební příklad
## Instalace
Postup instalace je následující:
```bash
pip install pipenv
pipenv install
docker-compose build
docker-compose up
```
Automaticky se spustí web na url localhost:5000 kde lze vyzkoušet požadované funkce,
tedy počet produktů, seznam produktů a seznam náhradních dílů.

## Skript products

Tento skript slouží k vyvolání požadovaných funkcí z příkazové řádky, výpis se provede na terminál.
Volby jsou následujcí:
- -h|--help nápověda
- -c|--count počet produktů
- -p|--products seznam produktů
- -t|--parts seznam náhradních dílů
- -s|--server spustí server localhost:5000

Spouští se následovně například takto:
```bash
docker exec <container> bash -c "python /app/products -c"
```

## Poznámky k implementaci

Vzhledem k velikosti zkušebního souboru jsem zvolil optimalizovanou verzi parseru etree z knihovny lxml a zpracování XML souboru pomocí XPATH výrazů.

Pokud by soubor byl běžně větší než několik GB, bylo by třeba použít buď metodu iterparse, která XML soubor zpracovává postupně a nebo SAX parser, který by potřebná data vyfiltroval a uložil buď do externího souboru a nebo do paměti, například do slovníku.

Výpis seznamů neřeší stránkování.

## Použité knihovny
K implementaci byla použita knihovna lxml a mikroframework Flask, obdoba frameworku Slim z PHP.
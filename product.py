
import zipfile
import os

from urllib.request import urlretrieve
from os import unlink
from operator import itemgetter
from itertools import groupby
from lxml import etree as ET
from optparse import OptionParser

class HttpZipReader:
    """Stažení vzdáleného zip souboru, vrací požadovaný soubor vytažený z archivu"""

    def __init__(self, url, filename):
        """Konstruktor"""
        self._url = url
        self._filename = filename

    def read(self):
        """Načte zip archiv z url a vybere z něj datový soubor"""
        zip_file, header = urlretrieve(self._url)
        if header.defects:
            raise zipfile.BadZipFile()
        with zipfile.ZipFile(zip_file) as zf:
            content = zf.open(self._filename).read()
        unlink(zip_file)
        return content
    

class ETProductParser:
    """Implementace požadovaných pohledů z exportu produktů"""

    def __init__(self, url: str, filename: str) -> None:
        self.url = url
        self.filename = filename
        self.doc = False

    def load(self):
        """Načte xml soubor pokud ještě není načtený"""
        if not self.doc:
            try:
                self.doc = ET.fromstring(HttpZipReader(self.url, self.filename).read())
            except zipfile.BadZipFile:
                print("Nepodařilo se načíst soubor s údaji!")

    def count(self):
        """Počet produktů v exportu"""
        return int(self.doc.xpath("count(/export_full/items/item)"))

    def products(self):
        """Výpis produktů s exportu"""
        return self.doc.xpath("/export_full/items/item/@name")

    def parts(self):
        """Výpis náhradních dílů z exportu produktů"""
        parts = self.doc.xpath("/export_full/items/item/parts/part/item")
        parts = [(n.xpath("../../../@name")[0], n.xpath('@name')[0]) for n in parts]
        parts.sort(key=itemgetter(0))
        return [(g[0], list([p[1] for p in g[1]])) for g in groupby(parts, key=itemgetter(0))]


class TerminalViewer:

    def __init__(self, product: ETProductParser) -> None:
        self.product = product

    def count(self):
        print(f"Počet produktů: {self.product.count()}")

    def products(self):
        [print(f"{p}") for p in self.product.products()]

    def parts(self):
        [print(f"{product}:\n\t" + "\n\t".join(parts)) for product, parts in self.product.parts()] 

    
class HTMLViewer:

    def __init__(self, product: ETProductParser) -> None:
        self.product = product

    def count(self):
        return f"<div>Počet produktů: {self.product.count()}</div>"

    def products(self):
        return "<ul>" + "".join([f"<li>{p}</li>" for p in self.product.products()]) + "</ul>"

    def parts(self):
        return "".join([f"<h3>{product}:</h3><ul>" + "".join([f"<li>{p}</li>" for p in parts]) + "</ul>" 
                        for product, parts in self.product.parts()]) 

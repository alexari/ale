from flask import Flask
from product import ETProductParser, HTMLViewer

model = ETProductParser("http://www.astramodel.cz/b2b/export_xml_PSs6t5prnOYaHfTOUI-6XNF6m.zip", 
                        "export_full.xml")

model.load()

app = Flask(__name__)

screen = """
    <html>
    <head>
        <title>Zkušební příklad</title>
    </head>
    <body>
        <h1>{title}</h1>
        <ul>
            <li><a href="/count">Počet produktů</a></li>
            <li><a href="/products">Produkty</a></li>
            <li><a href="/parts">Náhradní díly k produktům</a></li>
            <li><a href="/">Domů</a></li>
        </ul>
        <div style="overflow:scroll; width:100%; height:500px;border:1px solid gray">{body}</div>
    </body>
    </html>
"""


@app.route("/")
def home():
    return screen.format(title="Produkty", body="") 


@app.route("/count")
def count():
    return screen.format(title="Počet produktů", body=HTMLViewer(model).count())


@app.route("/products")
def products():
    return screen.format(title="Výpis produktů", body=HTMLViewer(model).products())


@app.route("/parts")
def parts():
    return screen.format(title="Výpis náhradních dílů", body=HTMLViewer(model).parts())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
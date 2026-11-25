import xml.etree.ElementTree as ET

# Espais de noms

NS = {
    "gesmes": "http://www.gesmes.org/xml/2002-08-01",
    "bce": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref",
}


# Parseig del XML

def parsejar_xml(contingut):
    arrel = ET.fromstring(contingut)

    cub_data = arrel.find("bce:Cube/bce:Cube", NS)
    if cub_data is None:
        raise ValueError("El XML no te l'estructura esperada.")

    data = cub_data.get("time")

    divises = {"EUR": 1.0}
    for cub in cub_data.findall("bce:Cube", NS):
        moneda = cub.get("currency")
        tasa = float(cub.get("rate"))
        divises[moneda] = tasa

    return data, divises


# Prova

if __name__ == "__main__":
    from api import descarregar_xml

    data, divises = parsejar_xml(descarregar_xml())
    print(f"Data de les dades: {data}")
    for moneda, tasa in divises.items():
        print(f"{moneda}: {tasa}")

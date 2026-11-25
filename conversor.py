import math

# Validacio

def validar_quantitat(text):
    try:
        quantitat = float(str(text).replace(",", "."))
    except ValueError:
        raise ValueError("La quantitat ha de ser un número.")
    if not math.isfinite(quantitat):
        raise ValueError("La quantitat ha de ser un número.")
    if quantitat < 0:
        raise ValueError("La quantitat no pot ser negativa.")
    return quantitat


# Conversio creuada amb l'euro com a pont

def convertir(quantitat, origen, desti, divises):
    if origen not in divises or desti not in divises:
        raise ValueError("Moneda no disponible.")
    euros = quantitat / divises[origen]
    return euros * divises[desti]


def tipus_canvi(origen, desti, divises):
    return convertir(1, origen, desti, divises)


# Prova

if __name__ == "__main__":
    from api import descarregar_xml
    from xml_divises import parsejar_xml

    data, divises = parsejar_xml(descarregar_xml())
    quantitat = validar_quantitat("100")
    resultat = convertir(quantitat, "USD", "JPY", divises)
    print(f"Dades del {data}")
    print(f"{quantitat:.2f} USD = {resultat:.2f} JPY")
    print(f"1 USD = {tipus_canvi('USD', 'JPY', divises):.4f} JPY")

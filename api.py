import requests

# Configuracio

URL_BCE = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"


# Peticio a l'API

def descarregar_xml(url=URL_BCE):
    try:
        resposta = requests.get(url, timeout=10)
        if resposta.status_code == 200:
            return resposta.content.decode("utf-8")
        else:
            raise ConnectionError(f"Error en connectar amb el servidor (codi {resposta.status_code}).")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Ha ocorregut un error: {e}")


# Prova

if __name__ == "__main__":
    try:
        contingut = descarregar_xml()
        print("Connexio correcta.")
        print(contingut[:500])
    except ConnectionError as e:
        print(e)

# Conversor de Divises (BCE)

Aplicación en Python que descarga el XML diario del Banco Central Europeo, lo procesa con `xml.etree.ElementTree` y permite convertir importes entre divisas desde una interfaz web hecha con Streamlit.

## Requisitos

- Python 3.10 o superior
- Conexión a Internet (la aplicación descarga el XML al arrancar)

Para comprobar que Python está instalado:

```powershell
python --version
```

## 1. Abrir la carpeta del proyecto

```powershell
cd "D:\2 DAM\Acces\ConversorDivises"
```

## 2. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

Esto instala `requests` (petición HTTP) y `streamlit` (interfaz).

## 3. Ejecutar la aplicación

```powershell
python -m streamlit run app.py
```

Se abrirá el navegador en http://localhost:8501. Si no se abre solo, copia esa dirección en el navegador.

Para pararla, pulsa `Ctrl + C` en la terminal.

## 4. Usar la aplicación

1. Al arrancar se descarga el XML y arriba a la derecha aparece la fecha oficial de los datos.
2. Escribe la cantidad en el campo **Quantitat**.
3. Elige la moneda de origen en **De** y la de destino en **A**. El botón ⇄ las intercambia.
4. Pulsa **Calcular conversió**.
5. Debajo aparece el resultado, el tipo de cambio y el **Pont EUR**, que muestra el paso intermedio por el euro.
6. En **Veure el XML rebut del BCE** se puede ver el XML original descargado.
7. Al final está la tabla con todas las divisas y sus tasas respecto al euro.

## 5. Probar la validación

| Qué escribir | Resultado esperado |
|---|---|
| `100` | Conversión correcta |
| `25,50` | Conversión correcta (acepta coma decimal) |
| `abc` | Error: «La quantitat ha de ser un número.» |
| `-5` | Error: «La quantitat no pot ser negativa.» |
| (vacío) | Error: «La quantitat ha de ser un número.» |

## 6. Probar cada módulo por separado

Cada archivo del backend se puede ejecutar solo para ver qué hace:

```powershell
python api.py
```

Descarga el XML y muestra los primeros 500 caracteres.

```powershell
python xml_divises.py
```

Muestra la fecha y la lista de monedas con su tasa.

```powershell
python conversor.py
```

Hace una conversión de ejemplo de 100 USD a JPY usando el euro como puente.

## Estructura del proyecto

| Archivo | Función |
|---|---|
| `api.py` | Petición GET a la URL del BCE con `requests` |
| `xml_divises.py` | Parseo del XML: fecha (`time`) y monedas (`currency`, `rate`), añade EUR = 1.0 |
| `conversor.py` | Validación de la cantidad y conversión cruzada |
| `app.py` | Interfaz en Streamlit |
| `.streamlit/config.toml` | Tema oscuro de la interfaz |
| `requirements.txt` | Dependencias |

## Fórmula de la conversión

```
CantidadFinal = (Importe / TasaOrigen) × TasaDestino
```

Todas las tasas del XML están referidas al euro (1 EUR = X moneda), así que primero se pasa el importe a euros y después a la moneda de destino.

## Problemas habituales

- **`No module named 'requests'` o `'streamlit'`**: vuelve a ejecutar el paso 2.
- **`streamlit` no se reconoce como comando**: usa siempre `python -m streamlit run app.py` en lugar de `streamlit run app.py`.
- **Error al cargar los datos del BCE**: comprueba la conexión a Internet y recarga la página.
- **El puerto 8501 está ocupado**: `python -m streamlit run app.py --server.port 8502`.

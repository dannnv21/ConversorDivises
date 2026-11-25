import streamlit as st

from api import descarregar_xml
from xml_divises import parsejar_xml
from conversor import validar_quantitat, convertir, tipus_canvi

# Configuracio de la pagina

st.set_page_config(page_title="Conversor de Divises BCE", page_icon="💶", layout="wide")

# Simbols i noms de les monedes

INFO_MONEDES = {
    "EUR": ("€", "Euro"), "USD": ("$", "Dòlar dels EUA"), "JPY": ("¥", "Ien japonès"),
    "CZK": ("Kč", "Corona txeca"), "DKK": ("kr", "Corona danesa"), "GBP": ("£", "Lliura esterlina"),
    "HUF": ("Ft", "Fòrint hongarès"), "PLN": ("zł", "Zloty polonès"), "RON": ("lei", "Leu romanès"),
    "SEK": ("kr", "Corona sueca"), "CHF": ("Fr", "Franc suís"), "ISK": ("kr", "Corona islandesa"),
    "NOK": ("kr", "Corona noruega"), "TRY": ("₺", "Lira turca"), "AUD": ("A$", "Dòlar australià"),
    "BRL": ("R$", "Real brasiler"), "CAD": ("C$", "Dòlar canadenc"), "CNY": ("¥", "Iuan xinès"),
    "HKD": ("HK$", "Dòlar de Hong Kong"), "IDR": ("Rp", "Rupia indonèsia"), "ILS": ("₪", "Xéquel israelià"),
    "INR": ("₹", "Rupia índia"), "KRW": ("₩", "Won sud-coreà"), "MXN": ("$", "Peso mexicà"),
    "MYR": ("RM", "Ringgit malaisi"), "NZD": ("NZ$", "Dòlar neozelandès"), "PHP": ("₱", "Peso filipí"),
    "SGD": ("S$", "Dòlar de Singapur"), "THB": ("฿", "Baht tailandès"), "ZAR": ("R", "Rand sud-africà"),
}


def simbol(moneda):
    return INFO_MONEDES.get(moneda, ("¤", moneda))[0]


def nom(moneda):
    return INFO_MONEDES.get(moneda, ("¤", moneda))[1]


def format_numero(numero, decimals=2):
    text = f"{numero:,.{decimals}f}"
    return text.replace(",", " ").replace(".", ",").replace(" ", ".")


def format_taxa(taxa):
    text = f"{taxa:.4f}".rstrip("0")
    if text.endswith("."):
        text += "0"
    entera, decimal = text.split(".")
    return f"{format_numero(int(entera), 0)},{decimal}"


# Estils

ESTILS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {
    background-color: #060A13;
    background-image: linear-gradient(rgba(77,155,255,0.05) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(77,155,255,0.05) 1px, transparent 1px);
    background-size: 48px 48px;
    color: #E6EDF7;
    font-family: 'Inter', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 4rem; }

.capcalera { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 40px; }
.marca { display: flex; align-items: center; gap: 14px; }
.logo { width: 44px; height: 44px; border-radius: 50%; border: 1.5px solid #4D9BFF; box-shadow: 0 0 18px rgba(77,155,255,0.35);
        display: flex; align-items: center; justify-content: center; font-family: 'JetBrains Mono', monospace; font-size: 22px; color: #4D9BFF; }
.marca-nom { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 17px; letter-spacing: 0.02em; color: #E6EDF7; }
.marca-sub { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #8A9BB8; }
.estat { display: flex; align-items: center; gap: 10px; padding: 8px 14px; border: 1px solid #1C2A44; border-radius: 999px;
         background: #0A1120; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #8A9BB8; }
.estat b { color: #E6EDF7; }
.punt { width: 8px; height: 8px; border-radius: 50%; background: #4DE0B0; box-shadow: 0 0 10px #4DE0B0; }

.heroi { position: relative; margin-bottom: 32px; }
.heroi-simbols { position: absolute; right: 0; top: -12px; font-family: 'JetBrains Mono', monospace; font-size: 64px;
                 letter-spacing: 0.18em; color: #0D1A30; white-space: nowrap; overflow: hidden; max-width: 100%; user-select: none; }
.heroi-etiqueta { position: relative; font-family: 'JetBrains Mono', monospace; font-size: 13px; letter-spacing: 0.16em; color: #7DB8FF; }
.heroi h1 { position: relative; margin: 10px 0; padding: 0; font-family: 'Space Grotesk', sans-serif; font-weight: 700;
            font-size: clamp(40px, 6vw, 64px); line-height: 1.02; letter-spacing: -0.02em; color: #E6EDF7; }
.heroi p { position: relative; margin: 0; max-width: 560px; color: #A3B3CC; font-size: 17px; }

div[data-testid="stTextInput"] label p, div[data-testid="stSelectbox"] label p { color: #A3B3CC; font-size: 13px; font-weight: 500; }
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #080E1A; border: 1px solid #22334F; border-radius: 12px; min-height: 56px; color: #E6EDF7; font-size: 14px;
}
div[data-testid="stTextInput"] div[data-baseweb="input"] > div { background: transparent; }
div[data-testid="stTextInput"] input { background: transparent; font-family: 'JetBrains Mono', monospace; font-size: 20px; color: #E6EDF7; }
div[data-baseweb="popover"] ul { background: #0C1322; }

.stButton button { height: 56px; border-radius: 12px; border: 1px solid #22334F; background: #0A1424; color: #7DB8FF;
                   font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 16px; width: 100%; }
.stButton button:hover { border-color: #4D9BFF; color: #B5D6FF; }
.stButton button[kind="primary"] { background: #4D9BFF; color: #04101F; border: 0; box-shadow: 0 0 24px rgba(77,155,255,0.35); }
.stButton button[kind="primary"]:hover { background: #6FB1FF; color: #04101F; }

.resultat { margin-top: 24px; border: 1px solid #1C2A44; border-radius: 20px; background: #0A101D; padding: 28px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.45); }
.resultat-cap { display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 24px; }
.resultat-sub { font-size: 13px; color: #8A9BB8; }
.resultat-valor { font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: clamp(40px, 6vw, 60px); line-height: 1.1;
                  color: #F2F7FF; text-shadow: 0 0 28px rgba(77,155,255,0.45); }
.resultat-codi { font-family: 'JetBrains Mono', monospace; font-size: 22px; color: #4D9BFF; margin-left: 10px; }
.pastilla { padding: 8px 14px; border: 1px solid #22334F; border-radius: 999px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #A3B3CC; }

.pont-titol { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.14em; color: #7DB8FF; margin-bottom: 12px; }
.pont { display: flex; flex-wrap: wrap; align-items: stretch; gap: 12px; }
.node { flex: 1 1 200px; padding: 16px; border: 1px solid #22334F; border-radius: 14px; background: #080E1A; display: flex; flex-direction: column; gap: 4px; }
.node.euro { border-color: #4D9BFF; background: #0B1730; box-shadow: 0 0 24px rgba(77,155,255,0.18); }
.node-etiqueta { font-size: 12px; color: #8A9BB8; }
.node-valor { font-family: 'JetBrains Mono', monospace; font-size: 20px; color: #E6EDF7; }
.node-codi { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #8A9BB8; }
.fletxa { flex: 0 1 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;
          font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #7DB8FF; }
.formula { margin-top: 12px; font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #8A9BB8; }

.error { margin-top: 24px; display: flex; align-items: center; gap: 12px; padding: 16px 18px; border: 1px solid #5A2A33;
         border-radius: 12px; background: #1A0E14; color: #FFB3BD; }

div[data-testid="stExpander"] { margin-top: 40px; border: 1px solid #1C2A44; border-radius: 16px; background: rgba(12,19,34,0.92); }
div[data-testid="stExpander"] summary p { color: #E6EDF7; font-weight: 500; }

.taxes-cap { margin-top: 40px; margin-bottom: 20px; display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 12px; }
.taxes-cap h2 { margin: 0; padding: 0; font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 28px; color: #E6EDF7; }
.taxes-cap p { margin: 4px 0 0; color: #8A9BB8; }
.taxes-base { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #8A9BB8; }
.graella { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 12px; }
.targeta { min-height: 104px; box-sizing: border-box; padding: 16px; border: 1px solid #1C2A44; border-radius: 14px;
           background: rgba(12,19,34,0.85); display: flex; flex-direction: column; justify-content: space-between; gap: 10px; }
.targeta.activa { border-color: #4D9BFF; background: #0B1730; }
.targeta-cap { display: flex; justify-content: space-between; align-items: center; }
.targeta-codi { font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 15px; color: #E6EDF7; }
.targeta-simbol { font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #7DB8FF; }
.targeta-taxa { font-family: 'JetBrains Mono', monospace; font-size: 18px; color: #E6EDF7; }
.targeta-nom { font-size: 12px; color: #8A9BB8; }

.peu { margin-top: 48px; padding-top: 24px; border-top: 1px solid #1C2A44; display: flex; flex-wrap: wrap;
       justify-content: space-between; gap: 12px; font-size: 13px; color: #8A9BB8; }
.peu a { color: #7DB8FF; }
.peu span:last-child { font-family: 'JetBrains Mono', monospace; }
</style>
"""

st.markdown(ESTILS, unsafe_allow_html=True)


# Carrega de les dades

@st.cache_data(ttl=3600, show_spinner="Descarregant el XML del BCE...")
def carregar_dades():
    contingut = descarregar_xml()
    data, divises = parsejar_xml(contingut)
    return contingut, data, divises


try:
    xml_rebut, data, divises = carregar_dades()
except (ConnectionError, ValueError) as e:
    st.error(f"No s'han pogut carregar les dades del BCE. {e}")
    st.stop()

monedes = list(divises.keys())


# Estat de la sessio

if "origen" not in st.session_state:
    st.session_state.origen = "EUR"
    st.session_state.desti = "USD" if "USD" in divises else monedes[0]
    st.session_state.quantitat = "100"
    st.session_state.calcul = ("100", st.session_state.origen, st.session_state.desti)


def intercanviar():
    st.session_state.origen, st.session_state.desti = st.session_state.desti, st.session_state.origen


def calcular():
    st.session_state.calcul = (st.session_state.quantitat, st.session_state.origen, st.session_state.desti)


# Capcalera

st.markdown(
    f"""<div class="capcalera">
<div class="marca"><div class="logo">¤</div><div><div class="marca-nom">CONVERSOR·BCE</div><div class="marca-sub">eurofxref-daily.xml</div></div></div>
<div class="estat"><span class="punt"></span>Dades carregades · data oficial <b>{data}</b></div>
</div>
<div class="heroi">
<div class="heroi-simbols">€ $ ¥ £ ₩ ₹ ₺ ₱ ฿ ₪</div>
<div class="heroi-etiqueta">API · XML · CONVERSIÓ CREUADA</div>
<h1>Conversor de Divises</h1>
<p>Tipus de canvi de referència del Banc Central Europeu, descarregats i llegits directament del XML diari.</p>
</div>""",
    unsafe_allow_html=True,
)


# Formulari de conversio

col_quantitat, col_origen, col_canvi, col_desti, col_boto = st.columns([2.2, 2.2, 0.7, 2.2, 1.9], vertical_alignment="bottom")

with col_quantitat:
    st.text_input(f"Quantitat ({simbol(st.session_state.origen)})", key="quantitat")

with col_origen:
    st.selectbox("De", monedes, key="origen", format_func=lambda m: f"{simbol(m)}  {m} · {nom(m)}")

with col_canvi:
    st.button("⇄", on_click=intercanviar, help="Intercanviar monedes")

with col_desti:
    st.selectbox("A", monedes, key="desti", format_func=lambda m: f"{simbol(m)}  {m} · {nom(m)}")

with col_boto:
    st.button("Calcular conversió", type="primary", on_click=calcular)


# Resultat

text, origen, desti = st.session_state.calcul

try:
    quantitat = validar_quantitat(text)
    resultat = convertir(quantitat, origen, desti, divises)
    euros = convertir(quantitat, origen, "EUR", divises)
    canvi = tipus_canvi(origen, desti, divises)

    st.markdown(
        f"""<div class="resultat">
<div class="resultat-cap">
<div><div class="resultat-sub">{format_numero(quantitat)} {origen} equivalen a</div>
<div><span class="resultat-valor">{simbol(desti)} {format_numero(resultat)}</span><span class="resultat-codi">{desti}</span></div></div>
<div class="pastilla">Tipus de canvi: 1 {origen} = {format_numero(canvi, 4)} {desti}</div>
</div>
<div class="pont-titol">PONT EUR</div>
<div class="pont">
<div class="node"><span class="node-etiqueta">Import d'origen</span><span class="node-valor">{simbol(origen)} {format_numero(quantitat)}</span><span class="node-codi">{origen}</span></div>
<div class="fletxa"><span>÷ {format_taxa(divises[origen])}</span><span>⟶</span></div>
<div class="node euro"><span class="node-etiqueta">Valor en euros</span><span class="node-valor">€ {format_numero(euros)}</span><span class="node-codi">EUR · base 1,0</span></div>
<div class="fletxa"><span>× {format_taxa(divises[desti])}</span><span>⟶</span></div>
<div class="node"><span class="node-etiqueta">Import final</span><span class="node-valor">{simbol(desti)} {format_numero(resultat)}</span><span class="node-codi">{desti}</span></div>
</div>
<div class="formula">QuantitatFinal = (Import ÷ TaxaOrigen) × TaxaDestí</div>
</div>""",
        unsafe_allow_html=True,
    )
except ValueError as e:
    st.markdown(f'<div class="error">⚠ «{text}»: {e} Per exemple 100 o 25,50.</div>', unsafe_allow_html=True)


# XML rebut

with st.expander("</>  Veure el XML rebut del BCE"):
    st.code(xml_rebut, language="xml")


# Taula de tipus de canvi

targetes = ""
for moneda, taxa in divises.items():
    activa = " activa" if moneda == desti else ""
    targetes += (
        f'<div class="targeta{activa}">'
        f'<div class="targeta-cap"><span class="targeta-codi">{moneda}</span><span class="targeta-simbol">{simbol(moneda)}</span></div>'
        f'<div><div class="targeta-taxa">{format_taxa(taxa)}</div><div class="targeta-nom">{nom(moneda)}</div></div>'
        f"</div>"
    )

st.markdown(
    f"""<div class="taxes-cap">
<div><h2>Tipus de canvi</h2><p>Base EUR · {len(divises)} divises</p></div>
<div class="taxes-base">1 € = X moneda</div>
</div>
<div class="graella">{targetes}</div>""",
    unsafe_allow_html=True,
)


# Peu de pagina

st.markdown(
    """<div class="peu">
<span>Font: <a href="https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml" target="_blank">Banc Central Europeu · eurofxref-daily.xml</a></span>
<span>Accés a Dades · Mòdul 486</span>
</div>""",
    unsafe_allow_html=True,
)

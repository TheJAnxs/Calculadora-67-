import streamlit as st
import re
from itertools import product
import pandas as pd

st.set_page_config(page_title="Calculadora Tabla de la Verdad", layout="centered")

# Estilo visual espacial (púrpura y celestes)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
        color: #ffffff;
    }
    .sidebar .stSidebar {
        background-color: #1a153b !important;
    }
    h1, h2, h3 {
        color: #00d2ff !important;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }
    .stButton>button {
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Información del grupo y materia en la barra lateral
with st.sidebar:
    st.markdown("### 🎓 Universidad de Guayaquil")
    st.markdown("**Carrera:** Software")
    st.markdown("**Materia:** Estructuras Discretas")
    st.markdown("**Curso:** 1-15")
    st.markdown("---")
    st.markdown("### 👥 Integrantes:")
    st.markdown("- Ivis Judith Triviño Jiménez")
    st.markdown("- Bruno Rafael Lopez Carrera")
    st.markdown("- Terán Lindao Juan David")
    st.markdown("- Elias Daniel Zavala Alvaradez")

st.title("📊 Calculadora de Tabla de la Verdad")
st.write("Construye tu expresión haciendo clic. El resultado se muestra en 0 y 1.")

if 'expr' not in st.session_state:
    st.session_state.expr = ""

st.subheader("🛠️ Constructor de Expresión")

# Variables y operadores
variables = ['p', 'q', 'r', 's', 't', 'u']
operadores = ['∧', '∨', '¬', '⊕', '→', '↔', '(', ')']

# Botones de variables
st.write("**Variables:**")
cols_var = st.columns(len(variables))
for i, var in enumerate(variables):
    with cols_var[i]:
        if st.button(var, key=f"var_{var}", use_container_width=True):
            st.session_state.expr += var

# Botones de operadores
st.write("**Operadores:**")
cols_op = st.columns(len(operadores))
for i, op in enumerate(operadores):
    with cols_op[i]:
        if st.button(op, key=f"op_{op}", use_container_width=True):
            st.session_state.expr += op

# Acciones de control
col_clear, col_preview, col_silent = st.columns([1, 2, 1])
with col_clear:
    if st.button("🗑️ Limpiar Todo", type="secondary", use_container_width=True):
        st.session_state.expr = ""

st.code(st.session_state.expr or "Vacío", language="text")

# Funciones de evaluación de lógica
def normalizar_expresion(expr: str):
    expr = expr.replace('∧', ' and ')
    expr = expr.replace('∨', ' or ')
    expr = expr.replace('¬', ' not ')
    expr = expr.replace('⊕', ' != ')
    expr = expr.replace('→', ' <= ')
    expr = re.sub(r'(\w+)\s*↔\s*(\w+)', r'(\1 == \2)', expr)
    expr = expr.replace('↔', ' == ')
    return expr

def extraer_variables(expr: str):
    return sorted(list(set(re.findall(r'\b[p-u]\b', expr))))

def generar_tabla(expr_raw: str):
    if not expr_raw:
        return [], []
    expr_norm = normalizar_expresion(expr_raw)
    vars_list = extraer_variables(expr_raw)
    if not vars_list:
        return [], []
    
    tabla = []
    for valores in product([1, 0], repeat=len(vars_list)):
        entorno = {v: bool(val) for v, val in zip(vars_list, valores)}
        try:
            res = int(bool(eval(expr_norm, {}, entorno)))
            fila = list(valores) + [res]
            tabla.append(fila)
        except Exception:
            return [], []
    return vars_list, tabla

# Generar y mostrar tabla
if st.session_state.expr.strip():
    vars_list, tabla = generar_tabla(st.session_state.expr)
    if not vars_list or not tabla:
        st.error("Expresión inválida o sin variables detectadas.")
    else:
        cols = vars_list + ["Resultado"]
        st.success(f"Tabla generada para {len(vars_list)} variables.")
        df = pd.DataFrame(tabla, columns=cols)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Descargar CSV", csv, "tabla_verdad.csv", "text/csv")
else:
    st.info("Ingresa o construye una expresión primero.")
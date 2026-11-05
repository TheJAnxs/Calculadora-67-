import streamlit as st
import re
from itertools import product
import pandas as pd

st.set_page_config(page_title="Calculadora Tabla de la Verdad", layout="centered")

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
    expr = expr.replace('→', ' <= ') # Implicación p->q equivale a (not p or q) / p<=q en bool
    # Para la equivalencia bicondicional ↔ usar ==
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
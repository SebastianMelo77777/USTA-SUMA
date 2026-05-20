import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="USTA Suma – Resultados Encuesta",
    page_icon="🌿",
    layout="wide",
)

# ── Paleta ───────────────────────────────────────────────────────────────────
V_OSCURO  = "#1B5E3B"
V_MEDIO   = "#2E8B57"
V_CLARO   = "#52B788"
V_PASTEL  = "#95D5B2"
OCRE      = "#D4A017"
NARANJA   = "#E07B39"
TIERRA    = "#C0522A"
FONDO_PAG = "#FAFDF7"
FONDO_CARD= "#FFFFFF"
FONDO_GRF = "#F4FAF6"

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  /* Fondo general de la app */
  html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
      background-color: {FONDO_PAG} !important;
  }}
  [data-testid="stMain"] > div {{
      background-color: {FONDO_PAG} !important;
  }}
  .block-container {{ padding: 3.5rem 3rem 2.5rem 3rem; }}

  /* Encabezado */
  .titulo {{
      font-size: 2.8rem; font-weight: 900; color: {V_OSCURO};
      text-align: center; letter-spacing: -0.5px;
      margin-bottom: 0.3rem;
  }}
  .subtitulo {{
      font-size: 1.25rem; color: #4A7C60;
      text-align: center; margin-bottom: 2rem;
      font-weight: 400;
  }}

  /* KPI cards */
  .kpi-card {{
      background: {FONDO_CARD};
      border: 2px solid {V_PASTEL};
      border-top: 6px solid {V_MEDIO};
      border-radius: 14px;
      padding: 1.4rem 0.8rem 1.2rem 0.8rem;
      text-align: center;
      box-shadow: 0 3px 14px rgba(46,139,87,0.10);
  }}
  .kpi-num  {{ font-size: 3rem; font-weight: 900; color: {V_OSCURO}; line-height: 1; }}
  .kpi-lbl  {{ font-size: 1rem; color: #4A7C60; margin-top: 6px; font-weight: 600; }}

  /* Separador de sección */
  .seccion {{
      font-size: 1.35rem; font-weight: 800; color: {V_OSCURO};
      border-left: 7px solid {V_CLARO};
      padding: 4px 0 4px 14px;
      margin: 2rem 0 0.8rem 0;
      background: linear-gradient(90deg, #EAF7EF 0%, transparent 100%);
      border-radius: 0 8px 8px 0;
  }}

  /* Nota pie */
  .nota {{
      font-size: 0.92rem; color: #6B9E7E; text-align: center;
      margin-top: 2.5rem; border-top: 1px solid {V_PASTEL};
      padding-top: 1rem;
  }}
</style>
""", unsafe_allow_html=True)

# ── Datos ────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar():
    ruta = Path(__file__).parent / "Resultados_Encuesta_USTA_Suma.xlsx"
    df = pd.read_excel(ruta)
    df.rename(columns={
        "1. ¿Habías visto anteriormente la campaña USTA Suma?": "P1",
        "2. ¿Dónde viste la campaña?": "P2",
        "3. Después de la campaña, ¿consideras que eres más consciente del uso del papel?": "P3",
        "4. ¿La campaña logró llamar tu atención?": "P4",
        "5. ¿Crees que las intervenciones en baños fueron efectivas?": "P5",
        "6. ¿Crees que este tipo de campañas generan reflexión sobre sostenibilidad?": "P6",
        "7. ¿Cambiarías tus hábitos para ayudar al cuidado ambiental de la universidad?": "P7",
        "8. ¿Alguna vez has botado papel u otros residuos en lugares incorrectos dentro de la universidad?": "P8",
    }, inplace=True)
    df["P1_n"] = df["P1"].map({"Sí": 1, "No": 0})
    df["P3_n"] = df["P3"].map({"Sí": 2, "Parcialmente": 1, "No": 0})
    df["P4_n"] = df["P4"].map({"Mucho": 2, "Poco": 1, "Nada": 0})
    df["P5_n"] = df["P5"].map({"Sí": 1, "No": 0})
    df["P6_n"] = df["P6"].map({"Sí": 2, "Parcialmente": 1, "No": 0})
    df["P7_n"] = df["P7"].map({"Sí": 2, "Parcialmente": 1, "No": 0})
    return df

df = cargar()
N = len(df)

def pct(col):
    return (df[col].value_counts() / N * 100).round(1)

# Ajustes globales de gráficas
FONT_TITULO  = dict(size=17, color=V_OSCURO, family="Arial")
FONT_TICK    = dict(size=15, color="#2A2A2A")
FONT_TEXTO   = 16   # labels dentro/fuera de barras
ALTO_GRAF    = 380

def layout_base(titulo, alto=ALTO_GRAF):
    return dict(
        title=dict(text=titulo, font=FONT_TITULO, x=0, xanchor="left"),
        font=dict(family="Arial", size=14, color="#1A1A1A"),
        paper_bgcolor=FONDO_CARD,
        plot_bgcolor=FONDO_GRF,
        margin=dict(t=55, b=30, l=20, r=20),
        height=alto,
    )

# ── ENCABEZADO ───────────────────────────────────────────────────────────────
st.markdown('<div class="titulo">🌿 USTA SUMA, NO DESPERDICIA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Resultados de Encuesta de Percepción · Universidad Santo Tomás · Sede Doctor Angélico</div>', unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────────────────────
cols_k = st.columns(5)
kpis = [
    (f"{pct('P1')['Sí']:.0f}%",          "Reconocieron\nla campaña"),
    (f"{pct('P4')['Mucho']:.0f}%",        "Mucha atención\ngenerada"),
    (f"{pct('P5')['Sí']:.0f}%",           "Intervenciones\nen baños efectivas"),
    (f"{pct('P6')['Sí']:.0f}%",           "Reflexión sobre\nsostenibilidad"),
    (f"{pct('P7')['Sí']:.0f}%",           "Cambiaría\nsus hábitos"),
]
for c, (num, lbl) in zip(cols_k, kpis):
    c.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-num">{num}</div>'
        f'<div class="kpi-lbl">{lbl}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

st.markdown("&nbsp;", unsafe_allow_html=True)

# ── SECCIÓN 1: Reconocimiento y puntos de contacto ───────────────────────────
st.markdown('<div class="seccion">📍 Reconocimiento y puntos de contacto</div>', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1.7])

with c1:
    p1 = pct("P1")
    fig = go.Figure(go.Pie(
        labels=p1.index.tolist(), values=p1.values.tolist(),
        hole=0.52,
        marker_colors=[V_OSCURO, NARANJA],
        textinfo="label+percent",
        textfont=dict(size=16),
        insidetextorientation="radial",
    ))
    fig.update_layout(**layout_base("P1 · ¿Habías visto la campaña?"))
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    orden = ["Baño del 5 piso", "Pasillos", "Redes sociales", "Salones", "No la vi"]
    p2 = pct("P2").reindex(orden).dropna()
    fig = go.Figure(go.Bar(
        x=p2.values, y=p2.index, orientation="h",
        marker_color=[V_OSCURO, V_MEDIO, V_CLARO, OCRE, NARANJA],
        text=[f"  {v:.0f}%" for v in p2.values],
        textposition="outside",
        textfont=dict(size=FONT_TEXTO, color="#1A1A1A"),
    ))
    fig.update_layout(**layout_base("P2 · ¿Dónde viste la campaña?"))
    fig.update_xaxes(range=[0, 48], tickfont=FONT_TICK, title_text="% de respuestas", title_font=dict(size=14))
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=15, color="#1A1A1A"))
    st.plotly_chart(fig, use_container_width=True)

# ── SECCIÓN 2: Conciencia y atención ─────────────────────────────────────────
st.markdown('<div class="seccion">🧠 Impacto en conciencia y atención</div>', unsafe_allow_html=True)
c3, c4 = st.columns(2)

def barra_v(col, pregunta, titulo, orden, colores):
    vals = pct(pregunta).reindex(orden).dropna()
    fig = go.Figure(go.Bar(
        x=vals.index, y=vals.values,
        marker_color=colores,
        text=[f"{v:.0f}%" for v in vals.values],
        textposition="outside",
        textfont=dict(size=FONT_TEXTO, color="#1A1A1A"),
        width=0.5,
    ))
    fig.update_layout(**layout_base(titulo))
    fig.update_xaxes(tickfont=dict(size=16, color="#1A1A1A"))
    fig.update_yaxes(range=[0, max(vals.values) + 14], tickfont=FONT_TICK,
                     title_text="%", title_font=dict(size=14))
    col.plotly_chart(fig, use_container_width=True)

barra_v(c3, "P3", "P3 · ¿Eres más consciente del uso del papel?",
        ["Sí", "Parcialmente", "No"], [V_OSCURO, OCRE, TIERRA])
barra_v(c4, "P4", "P4 · ¿La campaña llamó tu atención?",
        ["Mucho", "Poco", "Nada"], [V_MEDIO, NARANJA, TIERRA])

# ── SECCIÓN 3: Efectividad y reflexión ───────────────────────────────────────
st.markdown('<div class="seccion">♻️ Efectividad y reflexión sostenible</div>', unsafe_allow_html=True)
c5, c6 = st.columns([1, 1.7])

with c5:
    p5 = pct("P5")
    fig = go.Figure(go.Pie(
        labels=p5.index.tolist(), values=p5.values.tolist(),
        hole=0.52,
        marker_colors=[V_MEDIO, NARANJA],
        textinfo="label+percent",
        textfont=dict(size=16),
        insidetextorientation="radial",
    ))
    fig.update_layout(**layout_base("P5 · ¿Intervenciones en baños efectivas?"))
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with c6:
    orden3 = ["Sí", "Parcialmente", "No"]
    p6 = pct("P6").reindex(orden3).fillna(0)
    p7 = pct("P7").reindex(orden3).fillna(0)
    fig = go.Figure()
    for nombre, vals, color in [("P6 · Genera reflexión", p6, V_OSCURO),
                                  ("P7 · Cambiaría hábitos",  p7, OCRE)]:
        fig.add_trace(go.Bar(
            name=nombre, x=orden3, y=vals.values,
            marker_color=color,
            text=[f"{v:.0f}%" for v in vals.values],
            textposition="outside",
            textfont=dict(size=FONT_TEXTO, color="#1A1A1A"),
            width=0.35,
        ))
    fig.update_layout(**layout_base("P6 y P7 · Reflexión sostenible y cambio de hábitos"))
    fig.update_layout(
        barmode="group",
        legend=dict(font=dict(size=14), orientation="h", y=-0.18, x=0),
    )
    fig.update_xaxes(tickfont=dict(size=16, color="#1A1A1A"))
    fig.update_yaxes(range=[0, 78], tickfont=FONT_TICK, title_text="%", title_font=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)

# ── SECCIÓN 4: Comportamiento previo + radar ──────────────────────────────────
st.markdown('<div class="seccion">🗑️ Comportamiento previo y resumen de impacto</div>', unsafe_allow_html=True)
c7, c8 = st.columns(2)

with c7:
    orden8 = ["No", "Algunas veces", "Sí"]
    p8 = pct("P8").reindex(orden8).dropna()
    fig = go.Figure(go.Bar(
        x=p8.index, y=p8.values,
        marker_color=[V_CLARO, OCRE, TIERRA],
        text=[f"{v:.0f}%" for v in p8.values],
        textposition="outside",
        textfont=dict(size=FONT_TEXTO, color="#1A1A1A"),
        width=0.5,
    ))
    fig.update_layout(**layout_base("P8 · ¿Has botado residuos en lugares incorrectos?"))
    fig.update_xaxes(tickfont=dict(size=16, color="#1A1A1A"))
    fig.update_yaxes(range=[0, 65], tickfont=FONT_TICK, title_text="%", title_font=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)

with c8:
    r_labels = ["Reconocimiento (P1)", "Conciencia (P3)", "Atención (P4)",
                "Efectividad (P5)", "Reflexión (P6)", "Cambio hábitos (P7)"]
    r_scores = [
        df["P1_n"].mean() / 1 * 100,
        df["P3_n"].mean() / 2 * 100,
        df["P4_n"].mean() / 2 * 100,
        df["P5_n"].mean() / 1 * 100,
        df["P6_n"].mean() / 2 * 100,
        df["P7_n"].mean() / 2 * 100,
    ]
    fig = go.Figure(go.Scatterpolar(
        r=r_scores + [r_scores[0]],
        theta=r_labels + [r_labels[0]],
        fill="toself",
        fillcolor="rgba(82,183,136,0.22)",
        line=dict(color=V_OSCURO, width=3),
        marker=dict(color=OCRE, size=10),
    ))
    fig.update_layout(**layout_base("Resumen · Impacto general de la campaña (0–100)"))
    fig.update_layout(
        polar=dict(
            bgcolor=FONDO_GRF,
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=13), gridcolor="#CCEAD8"),
            angularaxis=dict(tickfont=dict(size=13, color=V_OSCURO)),
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Tabla con descarga ────────────────────────────────────────────────────────
st.markdown('<div class="seccion">📋 Datos completos de la encuesta</div>', unsafe_allow_html=True)

tabla_cols = {
    "P1": "¿Habías visto la campaña?",
    "P2": "¿Dónde la viste?",
    "P3": "¿Más consciente del papel?",
    "P4": "¿Llamó tu atención?",
    "P5": "¿Intervenciones efectivas?",
    "P6": "¿Genera reflexión?",
    "P7": "¿Cambiarías hábitos?",
    "P8": "¿Has botado residuos mal?",
}
df_tabla = df[["ID"] + list(tabla_cols.keys())].rename(columns=tabla_cols)

st.dataframe(df_tabla, use_container_width=True, height=360)

# Botón de descarga CSV
csv_bytes = df_tabla.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
st.download_button(
    label="⬇️ Descargar tabla en CSV",
    data=csv_bytes,
    file_name="Resultados_USTA_Suma.csv",
    mime="text/csv",
)

# ── Pie ───────────────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="nota">Muestra: {N} respuestas · Universidad Santo Tomás, Sede Doctor Angélico · Campaña USTA Suma, No Desperdicia</div>',
    unsafe_allow_html=True
)
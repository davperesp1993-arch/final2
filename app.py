import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Simulador Cable Preensamblado ASC - AAAC",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Simulador de Producción: Cable Preensamblado")
st.markdown("Selecciona el modelo de cable, ingresa el metraje a fabricar y ajusta recetas, tiempos totales por proceso o costos indirectos en vivo.")
st.divider()

# 1. PANEL LATERAL: SELECCIÓN DE CALIBRE, VOLUMEN Y COSTOS BASE
st.sidebar.header("🔌 1. Selección de Producto")
modelo_cable = st.sidebar.selectbox(
    "Modelo de Cable Preensamblado:",
    options=[
        "CABLE PREENSAMBLADO ASC - AAAC 2 X 50 + 1 X 50 MM2",
        "CABLE PREENSAMBLADO ASC - AAAC 3 X 50 + 1 X 50 MM2"
    ]
)

es_3x50 = "3 X 50" in modelo_cable
num_fases = 3 if es_3x50 else 2
num_neutros = 1

st.subheader(f"{modelo_cable} | Actual vs. Compactado")

st.sidebar.divider()
st.sidebar.header("📏 2. Orden de Producción")
metros = st.sidebar.number_input(
    "Cantidad a fabricar (Metros):",
    min_value=1,
    max_value=5000000,
    value=1000,
    step=100
)
km = metros / 1000.0
st.sidebar.caption(f"Equivalente a: **{km:,.3f} km**")

st.sidebar.divider()
st.sidebar.header("💲 3. Costos de Materia Prima ($/kg)")
costo_al_1350 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 1350 9.50 MM H14 ($/kg):",
    min_value=0.0,
    value=4.2700,
    step=0.01,
    format="%.4f"
)
costo_al_6201 = st.sidebar.number_input(
    "ALAMBRE DE ALUMINIO 6201 3.00 MM ($/kg):",
    min_value=0.0,
    value=5.2416,
    step=0.01,
    format="%.4f"
)
costo_xlpe = st.sidebar.number_input(
    "XLPE NEG ($/kg):",
    min_value=0.0,
    value=2.2865,
    step=0.01,
    format="%.4f"
)

# 2. CONFIGURACIÓN DE RECETAS DE MATERIA PRIMA (UNITARIO POR CONDUCTOR)
with st.expander(f"📦 Ver / Editar Recetas Unitarias por Conductor ({num_fases} Fases + {num_neutros} Neutro)", expanded=False):
    st.caption(f"Los valores ingresados corresponden a **1 conductor**. El sistema multiplica automáticamente las Fases x{num_fases} y el Neutro x{num_neutros}.")
    df_recetas = pd.DataFrame([
        {"Componente": "Fase ASC (x1 conductor) - Al 1350", "Actual (kg/km)": 135.97, "Compactado (kg/km)": 135.97},
        {"Componente": "Fase ASC (x1 conductor) - XLPE NEG", "Actual (kg/km)": 53.60, "Compactado (kg/km)": 41.00},
        {"Componente": "Neutro AAAC (x1 conductor) - Al 6201", "Actual (kg/km)": 134.17, "Compactado (kg/km)": 134.17},
        {"Componente": "Neutro AAAC (x1 conductor) - XLPE NEG", "Actual (kg/km)": 53.73, "Compactado (kg/km)": 53.73},
    ])
    recetas_edit = st.data_editor(df_recetas, hide_index=True, use_container_width=True, key=f"recetas_{num_fases}")

# 3. ESTRUCTURA DE PESTAÑAS
tab1, tab2, tab3, tab4 = st.tabs([
    "🏭 Tiempos y Costos Indirectos (Modificable)",
    "⏱️ Comparativa Tiempos y Costos Totales",
    "📋 Comparativa Materia Prima", 
    "📈 Gráficos Ejecutivos e Histórico (2024–2026)"
])

# PESTAÑA 1: CONFIGURACIÓN MODIFICABLE DE TIEMPOS TOTALES Y COSTOS POR PROCESO
with tab1:
    st.markdown(f"### ⏱️ 1. Tiempos Totales Modificables por Proceso para **{num_fases}x50 + 1x50** (hrs/km de cable)")
    st.markdown("Ingresa directamente los **tiempos totales (hrs/km)** que toma cada proceso completo para fabricar 1 km del cable terminado.")
    
    if es_3x50:
        df_tiempos_base = pd.DataFrame([
            {"Proceso": "Trefilado", "Actual (hrs/km)": 1.35, "Compactado (hrs/km)": 1.35, "Detalle / Alcance": "Tiempo total trefilado (3 fases)"},
            {"Proceso": "Cableado", "Actual (hrs/km)": 2.40, "Compactado (hrs/km)": 2.70, "Detalle / Alcance": "Tiempo total cableado (3 fases)"},
            {"Proceso": "Extrusado", "Actual (hrs/km)": 4.40, "Compactado (hrs/km)": 3.80, "Detalle / Alcance": "Tiempo total extrusión XLPE (3 fases + 1 neutro)"},
            {"Proceso": "Trenzado", "Actual (hrs/km)": 0.95, "Compactado (hrs/km)": 0.90, "Detalle / Alcance": "Tiempo total reunido / preensamblado final"},
        ])
    else:
        df_tiempos_base = pd.DataFrame([
            {"Proceso": "Trefilado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.90, "Detalle / Alcance": "Tiempo total trefilado (2 fases)"},
            {"Proceso": "Cableado", "Actual (hrs/km)": 1.60, "Compactado (hrs/km)": 1.80, "Detalle / Alcance": "Tiempo total cableado (2 fases)"},
            {"Proceso": "Extrusado", "Actual (hrs/km)": 3.30, "Compactado (hrs/km)": 2.85, "Detalle / Alcance": "Tiempo total extrusión XLPE (2 fases + 1 neutro)"},
            {"Proceso": "Trenzado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.85, "Detalle / Alcance": "Tiempo total reunido / preensamblado final"},
        ])
    
    tiempos_edit = st.data_editor(
        df_tiempos_base,
        use_container_width=True,
        hide_index=True,
        disabled=["Proceso"],
        key=f"tiempos_{num_fases}",
        column_config={
            "Proceso": st.column_config.TextColumn("Proceso"),
            "Actual (hrs/km)": st.column_config.NumberColumn("Tiempo Total Actual (hrs/km)", min_value=0.0, format="%.2f", required=True),
            "Compactado (hrs/km)": st.column_config.NumberColumn("Tiempo Total Compactado (hrs/km)", min_value=0.0, format="%.2f", required=True),
            "Detalle / Alcance": st.column_config.TextColumn("Observación")
        }
    )

    st.divider()
    st.markdown("### 🏭 2. Costos Indirectos y Mano de Obra por Proceso ($/Hora-Máquina)")
    st.markdown("Edita los valores por hora para cada proceso. La columna **Total ($/hr)** se suma automáticamente.")
    
    df_procesos_base = pd.DataFrame([
        {
            "Proceso": "Trefilado",
            "Costo Mano de Obra Directa": 12.00,
            "Costo Mano de Obra Indirecta": 5.00,
            "Costos Indirectos de Fabricación": 18.00
        },
        {
            "Proceso": "Cableado",
            "Costo Mano de Obra Directa": 14.00,
            "Costo Mano de Obra Indirecta": 6.00,
            "Costos Indirectos de Fabricación": 22.00
        },
        {
            "Proceso": "Extrusado",
            "Costo Mano de Obra Directa": 16.00,
            "Costo Mano de Obra Indirecta": 7.50,
            "Costos Indirectos de Fabricación": 28.00
        },
        {
            "Proceso": "Trenzado",
            "Costo Mano de Obra Directa": 15.00,
            "Costo Mano de Obra Indirecta": 6.50,
            "Costos Indirectos de Fabricación": 24.00
        }
    ])
    
    procesos_edit = st.data_editor(
        df_procesos_base,
        use_container_width=True,
        hide_index=True,
        disabled=["Proceso"],
        key="costos_procesos_global",
        column_config={
            "Proceso": st.column_config.TextColumn("Proceso / Línea"),
            "Costo Mano de Obra Directa": st.column_config.NumberColumn("Costo Mano de Obra Directa ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costo Mano de Obra Indirecta": st.column_config.NumberColumn("Costo Mano de Obra Indirecta ($/hr)", min_value=0.0, format="$%.2f", required=True),
            "Costos Indirectos de Fabricación": st.column_config.NumberColumn("Costos Indirectos de Fabricación ($/hr)", min_value=0.0, format="$%.2f", required=True),
        }
    )
    
    for col in ["Costo Mano de Obra Directa", "Costo Mano de Obra Indirecta", "Costos Indirectos de Fabricación"]:
        procesos_edit[col] = pd.to_numeric(procesos_edit[col], errors="coerce").fillna(0.0)
        
    procesos_edit["Total ($/hr)"] = (
        procesos_edit["Costo Mano de Obra Directa"] +
        procesos_edit["Costo Mano de Obra Indirecta"] +
        procesos_edit["Costos Indirectos de Fabricación"]
    )
    
    tarifas_dict = procesos_edit.set_index("Proceso").to_dict(orient="index")
    
    st.markdown("#### 📊 Tarifas Totales Activas por Proceso ($/hr)")
    cols_proc = st.columns(4)
    for idx, row in procesos_edit.iterrows():
        cols_proc[idx].metric(
            label=f"⚙️ {row['Proceso']}",
            value=f"${row['Total ($/hr)']:,.2f} / hr",
            delta=f"MOD: ${row['Costo Mano de Obra Directa']:.2f} | MOI: ${row['Costo Mano de Obra Indirecta']:.2f} | CIF: ${row['Costos Indirectos de Fabricación']:.2f}",
            delta_color="off"
        )

# Resumen en barra lateral
st.sidebar.divider()
st.sidebar.header("🏭 4. Tarifas por Proceso ($/hr)")
for proc_nombre, datos_p in tarifas_dict.items():
    st.sidebar.text(f"• {proc_nombre}: ${datos_p['Total ($/hr)']:,.2f}/hr")

# 4. MOTOR DE CÁLCULO (ACTUAL VS COMPACTADO SIN MULTIPLICADOR EN TIEMPOS)
def calcular_escenario(tipo, km_eval, fases_cant=num_fases, df_t_custom=None):
    col_val = f"{tipo} (kg/km)"
    df_t_usar = df_t_custom if df_t_custom is not None else tiempos_edit
    
    al_1350_fase = recetas_edit.loc[0, col_val]
    xlpe_fase = recetas_edit.loc[1, col_val]
    al_6201_neutro = recetas_edit.loc[2, col_val]
    xlpe_neutro = recetas_edit.loc[3, col_val]
    
    kg_km_1350 = al_1350_fase * fases_cant
    kg_km_6201 = al_6201_neutro * num_neutros
    kg_km_xlpe = (xlpe_fase * fases_cant) + (xlpe_neutro * num_neutros)
    
    tot_kg_1350 = kg_km_1350 * km_eval
    tot_kg_6201 = kg_km_6201 * km_eval
    tot_kg_xlpe = kg_km_xlpe * km_eval
    peso_total_kg = tot_kg_1350 + tot_kg_6201 + tot_kg_xlpe
    
    costo_tot_1350 = tot_kg_1350 * costo_al_1350
    costo_tot_6201 = tot_kg_6201 * costo_al_6201
    costo_tot_xlpe = tot_kg_xlpe * costo_xlpe
    costo_mp_total = costo_tot_1350 + costo_tot_6201 + costo_tot_xlpe
    
    col_t = f"{tipo} (hrs/km)"
    procesos_detalle = []
    horas_totales = 0.0
    
    tot_mod = 0.0
    tot_moi = 0.0
    tot_cif = 0.0
    costo_indirecto_total = 0.0
    
    for _, row in df_t_usar.iterrows():
        proc = row["Proceso"]
        tarifas_p = tarifas_dict.get(proc, {"Costo Mano de Obra Directa": 0, "Costo Mano de Obra Indirecta": 0, "Costos Indirectos de Fabricación": 0, "Total ($/hr)": 0})
        
        # Tiempo total ingresado directamente en hrs/km multiplicado por los km
        hrs_proc = row[col_t] * km_eval
        c_mod = hrs_proc * tarifas_p["Costo Mano de Obra Directa"]
        c_moi = hrs_proc * tarifas_p["Costo Mano de Obra Indirecta"]
        c_cif = hrs_proc * tarifas_p["Costos Indirectos de Fabricación"]
        c_tot_proc = hrs_proc * tarifas_p["Total ($/hr)"]
        
        horas_totales += hrs_proc
        tot_mod += c_mod
        tot_moi += c_moi
        tot_cif += c_cif
        costo_indirecto_total += c_tot_proc
        
        procesos_detalle.append({
            "Proceso": proc,
            "Horas": hrs_proc,
            "Tarifa_Hr": tarifas_p["Total ($/hr)"],
            "MOD": c_mod,
            "MOI": c_moi,
            "CIF": c_cif,
            "Costo_Total_Proc": c_tot_proc
        })
        
    costo_gran_total = costo_mp_total + costo_indirecto_total
    costo_por_metro = costo_gran_total / (km_eval * 1000.0) if km_eval > 0 else 0
    
    df_mp = pd.DataFrame([
        {"Materia Prima": f"ALAMBRE DE ALUMINIO 1350 9.50 MM H14 ({fases_cant} Fases)", "Kg/Km Cable": kg_km_1350, "Consumo Total (kg)": tot_kg_1350, "Costo Total ($)": costo_tot_1350},
        {"Materia Prima": "ALAMBRE DE ALUMINIO 6201 3.00 MM (1 Neutro)", "Kg/Km Cable": kg_km_6201, "Consumo Total (kg)": tot_kg_6201, "Costo Total ($)": costo_tot_6201},
        {"Materia Prima": f"XLPE NEG ({fases_cant} Fases + 1 Neutro)", "Kg/Km Cable": kg_km_xlpe, "Consumo Total (kg)": tot_kg_xlpe, "Costo Total ($)": costo_tot_xlpe},
    ])
    
    return {
        "df_mp": df_mp,
        "df_procesos": pd.DataFrame(procesos_detalle),
        "peso_total": peso_total_kg,
        "costo_mp": costo_mp_total,
        "horas_totales": horas_totales,
        "tot_mod": tot_mod,
        "tot_moi": tot_moi,
        "tot_cif": tot_cif,
        "costo_ind_total": costo_indirecto_total,
        "costo_total": costo_gran_total,
        "costo_metro": costo_por_metro,
        "kg_xlpe": tot_kg_xlpe,
        "costo_xlpe": costo_tot_xlpe
    }

act = calcular_escenario("Actual", km)
comp = calcular_escenario("Compactado", km)

diff_costo_tot = comp["costo_total"] - act["costo_total"]
diff_pct_tot = (diff_costo_tot / act["costo_total"]) * 100 if act["costo_total"] > 0 else 0
diff_xlpe_kg = comp["kg_xlpe"] - act["kg_xlpe"]
diff_xlpe_usd = comp["costo_xlpe"] - act["costo_xlpe"]
diff_horas = comp["horas_totales"] - act["horas_totales"]
diff_ind_tot = comp["costo_ind_total"] - act["costo_ind_total"]

# 5. TARJETAS DE IMPACTO EJECUTIVO (KPIs)
st.subheader(f"📊 Resultados de Simulación para {metros:,} metros ({km:,.2f} km) — {num_fases}x50 + 1x50 mm²")

k1, k2, k3 = st.columns(3)
k1.metric(
    "💰 Costo Total: ACTUAL",
    f"${act['costo_total']:,.2f}",
    f"${act['costo_metro']:,.4f} / metro",
    delta_color="off"
)
k2.metric(
    "🚀 Costo Total: COMPACTADO",
    f"${comp['costo_total']:,.2f}",
    f"{diff_costo_tot:+,.2f} USD ({diff_pct_tot:+.2f}%)",
    delta_color="inverse"
)
k3.metric(
    "🛢️ Ahorro en XLPE NEG",
    f"{abs(diff_xlpe_kg):,.2f} kg",
    f"{diff_xlpe_usd:+,.2f} USD en aislamiento",
    delta_color="inverse"
)

t1, t2, t3, t4 = st.columns(4)
t1.metric(
    "⏱️ Tiempo Total ACTUAL",
    f"{act['horas_totales']:,.2f} hrs",
    "Tiempo base sin compactar",
    delta_color="off"
)
t2.metric(
    "⏱️ Tiempo Total COMPACTADO",
    f"{comp['horas_totales']:,.2f} hrs",
    f"{diff_horas:+,.2f} hrs vs Actual",
    delta_color="inverse"
)
t3.metric(
    "🏭 Costo Indirecto ACTUAL",
    f"${act['costo_ind_total']:,.2f}",
    "MOD + MOI + CIF Actual",
    delta_color="off"
)
t4.metric(
    "🏭 Costo Indirecto COMPACTADO",
    f"${comp['costo_ind_total']:,.2f}",
    f"{diff_ind_tot:+,.2f} USD vs Actual",
    delta_color="inverse"
)

st.divider()

# 6. PESTAÑA 2: COMPARATIVA DETALLADA DE TIEMPOS Y COSTOS INDIRECTOS
with tab2:
    st.markdown(f"### ⏱️ Comparativa por Proceso ({num_fases}x50 + 1x50): Tiempos Totales vs. Costos Indirectos Totales")
    
    df_comp_proc = pd.DataFrame({
        "Proceso": act["df_procesos"]["Proceso"],
        "Tarifa ($/hr)": act["df_procesos"]["Tarifa_Hr"],
        "Horas Actual": act["df_procesos"]["Horas"],
        "Horas Compactado": comp["df_procesos"]["Horas"],
        "Dif. Horas": comp["df_procesos"]["Horas"] - act["df_procesos"]["Horas"],
        "Costo Total Actual ($)": act["df_procesos"]["Costo_Total_Proc"],
        "Costo Total Compactado ($)": comp["df_procesos"]["Costo_Total_Proc"],
        "Dif. Costo ($)": comp["df_procesos"]["Costo_Total_Proc"] - act["df_procesos"]["Costo_Total_Proc"]
    })
    
    fila_total = pd.DataFrame([{
        "Proceso": "TOTAL GENERAL",
        "Tarifa ($/hr)": None,
        "Horas Actual": df_comp_proc["Horas Actual"].sum(),
        "Horas Compactado": df_comp_proc["Horas Compactado"].sum(),
        "Dif. Horas": df_comp_proc["Dif. Horas"].sum(),
        "Costo Total Actual ($)": df_comp_proc["Costo Total Actual ($)"].sum(),
        "Costo Total Compactado ($)": df_comp_proc["Costo Total Compactado ($)"].sum(),
        "Dif. Costo ($)": df_comp_proc["Dif. Costo ($)"].sum()
    }])
    
    df_comp_proc_final = pd.concat([df_comp_proc, fila_total], ignore_index=True)
    
    st.dataframe(
        df_comp_proc_final.style.format({
            "Tarifa ($/hr)": lambda x: f"${x:,.2f}" if pd.notnull(x) else "—",
            "Horas Actual": "{:,.2f} hrs",
            "Horas Compactado": "{:,.2f} hrs",
            "Dif. Horas": "{:+,.2f} hrs",
            "Costo Total Actual ($)": "${:,.2f}",
            "Costo Total Compactado ($)": "${:,.2f}",
            "Dif. Costo ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("#### 🧾 Desglose Acumulado por Elemento de Costo (MOD, MOI y CIF)")
    df_res_conv = pd.DataFrame([
        {"Rubro": "Costo Mano de Obra Directa (MOD)", "Actual ($)": act["tot_mod"], "Compactado ($)": comp["tot_mod"], "Diferencia ($)": comp["tot_mod"] - act["tot_mod"]},
        {"Rubro": "Costo Mano de Obra Indirecta (MOI)", "Actual ($)": act["tot_moi"], "Compactado ($)": comp["tot_moi"], "Diferencia ($)": comp["tot_moi"] - act["tot_moi"]},
        {"Rubro": "Costos Indirectos de Fabricación (CIF)", "Actual ($)": act["tot_cif"], "Compactado ($)": comp["tot_cif"], "Diferencia ($)": comp["tot_cif"] - act["tot_cif"]},
        {"Rubro": "TOTAL COSTOS INDIRECTOS Y MANO DE OBRA", "Actual ($)": act["costo_ind_total"], "Compactado ($)": comp["costo_ind_total"], "Diferencia ($)": comp["costo_ind_total"] - act["costo_ind_total"]},
    ])
    st.dataframe(
        df_res_conv.style.format({
            "Actual ($)": "${:,.2f}",
            "Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

# 7. PESTAÑA 3: COMPARATIVA MATERIA PRIMA
with tab3:
    st.markdown(f"### Desglose de Materia Prima ({num_fases} Fases ASC + 1 Neutro AAAC)")
    
    df_comp_mp = pd.DataFrame({
        "Materia Prima": act["df_mp"]["Materia Prima"],
        "Actual (kg/km)": act["df_mp"]["Kg/Km Cable"],
        "Compactado (kg/km)": comp["df_mp"]["Kg/Km Cable"],
        "Consumo Actual (kg)": act["df_mp"]["Consumo Total (kg)"],
        "Consumo Compactado (kg)": comp["df_mp"]["Consumo Total (kg)"],
        "Costo Actual ($)": act["df_mp"]["Costo Total ($)"],
        "Costo Compactado ($)": comp["df_mp"]["Costo Total ($)"],
        "Diferencia ($)": comp["df_mp"]["Costo Total ($)"] - act["df_mp"]["Costo Total ($)"]
    })
    
    st.dataframe(
        df_comp_mp.style.format({
            "Actual (kg/km)": "{:,.2f}",
            "Compactado (kg/km)": "{:,.2f}",
            "Consumo Actual (kg)": "{:,.2f}",
            "Consumo Compactado (kg)": "{:,.2f}",
            "Costo Actual ($)": "${:,.2f}",
            "Costo Compactado ($)": "${:,.2f}",
            "Diferencia ($)": "${:+,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

# 8. PESTAÑA 4: GRÁFICOS EJECUTIVOS + CONSOLIDADO HISTÓRICO 2024 - 2026
with tab4:
    st.markdown(f"### 📊 Comparativa de la Orden Actual ({metros:,} m — {num_fases}x50 + 1x50 mm²)")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("**Costos Indirectos por Proceso ($): Actual vs. Compactado**")
        df_g_proc = pd.concat([
            act["df_procesos"][["Proceso", "Costo_Total_Proc"]].assign(Escenario="Actual"),
            comp["df_procesos"][["Proceso", "Costo_Total_Proc"]].assign(Escenario="Compactado")
        ])
        fig_proc = px.bar(
            df_g_proc, x="Proceso", y="Costo_Total_Proc", color="Escenario", barmode="group", text_auto=".2f",
            labels={"Costo_Total_Proc": "Costo Total ($)"},
            color_discrete_map={"Actual": "#EF553B", "Compactado": "#00CC96"}
        )
        fig_proc.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_proc, use_container_width=True)

    with col_g2:
        st.markdown("**Tiempos Totales por Proceso (hrs): Actual vs. Compactado**")
        df_g_hrs = pd.concat([
            act["df_procesos"][["Proceso", "Horas"]].assign(Escenario="Actual"),
            comp["df_procesos"][["Proceso", "Horas"]].assign(Escenario="Compactado")
        ])
        fig_hrs = px.bar(
            df_g_hrs, x="Proceso", y="Horas", color="Escenario", barmode="group", text_auto=".2f",
            labels={"Horas": "Tiempo Total (hrs)"},
            color_discrete_map={"Actual": "#EF553B", "Compactado": "#00CC96"}
        )
        fig_hrs.update_layout(xaxis_title="", legend_title="")
        st.plotly_chart(fig_hrs, use_container_width=True)

    st.divider()
    
    # SECCIÓN HISTÓRICA CONSOLIDADA (2x50+50 Y 3x50+50)
    st.markdown("### 📅 Simulación Histórica Consolidada (2024 – 2026): 2x50+50 y 3x50+50")
    st.markdown("Cálculo del ahorro real que se habría obtenido sumando ambos calibres si se hubiera compactado desde 2024.")
    
    df_hist_base = pd.DataFrame([
        {"Año": "2024", "Metros 2x50+50": 697098, "Metros 3x50+50": 83765},
        {"Año": "2025", "Metros 2x50+50": 571272, "Metros 3x50+50": 62869},
        {"Año": "2026 (YTD)", "Metros 2x50+50": 411499, "Metros 3x50+50": 59976},
    ])
    
    col_htabla, col_hresumen = st.columns([1.4, 1])
    
    with col_htabla:
        st.markdown("**Metrajes Históricos Producidos (Modificables)**")
        hist_edit = st.data_editor(
            df_hist_base,
            use_container_width=True,
            hide_index=True,
            key="tabla_historica_consolidada",
            column_config={
                "Año": st.column_config.TextColumn("Periodo", disabled=True),
                "Metros 2x50+50": st.column_config.NumberColumn("Metros 2x50 + 50", min_value=0, step=1000, format="%d m"),
                "Metros 3x50+50": st.column_config.NumberColumn("Metros 3x50 + 50", min_value=0, step=1000, format="%d m")
            }
        )
        
    # Tiempos base totales por calibre (sin multiplicador) para el cálculo consolidado histórico
    df_t_2x50_hist = pd.DataFrame([
        {"Proceso": "Trefilado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.90},
        {"Proceso": "Cableado", "Actual (hrs/km)": 1.60, "Compactado (hrs/km)": 1.80},
        {"Proceso": "Extrusado", "Actual (hrs/km)": 3.30, "Compactado (hrs/km)": 2.85},
        {"Proceso": "Trenzado", "Actual (hrs/km)": 0.90, "Compactado (hrs/km)": 0.85},
    ])
    df_t_3x50_hist = pd.DataFrame([
        {"Proceso": "Trefilado", "Actual (hrs/km)": 1.35, "Compactado (hrs/km)": 1.35},
        {"Proceso": "Cableado", "Actual (hrs/km)": 2.40, "Compactado (hrs/km)": 2.70},
        {"Proceso": "Extrusado", "Actual (hrs/km)": 4.40, "Compactado (hrs/km)": 3.80},
        {"Proceso": "Trenzado", "Actual (hrs/km)": 0.95, "Compactado (hrs/km)": 0.90},
    ])
    
    # Si el usuario editó los tiempos del calibre activo en la Pestaña 1, usar esos valores
    if es_3x50:
        df_t_3x50_hist = tiempos_edit[["Proceso", "Actual (hrs/km)", "Compactado (hrs/km)"]]
    else:
        df_t_2x50_hist = tiempos_edit[["Proceso", "Actual (hrs/km)", "Compactado (hrs/km)"]]
        
    # Ahorro unitario por km de cada calibre
    ahorro_km_2x50 = calcular_escenario("Actual", 1.0, 2, df_t_2x50_hist)["costo_total"] - calcular_escenario("Compactado", 1.0, 2, df_t_2x50_hist)["costo_total"]
    ahorro_km_3x50 = calcular_escenario("Actual", 1.0, 3, df_t_3x50_hist)["costo_total"] - calcular_escenario("Compactado", 1.0, 3, df_t_3x50_hist)["costo_total"]
    
    xlpe_km_2x50 = calcular_escenario("Actual", 1.0, 2, df_t_2x50_hist)["kg_xlpe"] - calcular_escenario("Compactado", 1.0, 2, df_t_2x50_hist)["kg_xlpe"]
    xlpe_km_3x50 = calcular_escenario("Actual", 1.0, 3, df_t_3x50_hist)["kg_xlpe"] - calcular_escenario("Compactado", 1.0, 3, df_t_3x50_hist)["kg_xlpe"]
    
    resultados_hist = []
    acumulado_usd = 0.0
    for _, row in hist_edit.iterrows():
        km_2 = row["Metros 2x50+50"] / 1000.0
        km_3 = row["Metros 3x50+50"] / 1000.0
        
        ahorro_2 = km_2 * ahorro_km_2x50
        ahorro_3 = km_3 * ahorro_km_3x50
        ahorro_total_anio = ahorro_2 + ahorro_3
        acumulado_usd += ahorro_total_anio
        xlpe_total_kg = (km_2 * xlpe_km_2x50) + (km_3 * xlpe_km_3x50)
        
        resultados_hist.append({
            "Año": row["Año"],
            "Metros Totales": row["Metros 2x50+50"] + row["Metros 3x50+50"],
            "Ahorro 2x50+50 ($)": ahorro_2,
            "Ahorro 3x50+50 ($)": ahorro_3,
            "Ahorro Total Anual ($)": ahorro_total_anio,
            "Ahorro Acumulado ($)": acumulado_usd,
            "XLPE Ahorrado (kg)": xlpe_total_kg
        })
        
    df_hist_calc = pd.DataFrame(resultados_hist)
    
    tot_m_2 = hist_edit["Metros 2x50+50"].sum()
    tot_m_3 = hist_edit["Metros 3x50+50"].sum()
    tot_ahorro_2 = df_hist_calc["Ahorro 2x50+50 ($)"].sum()
    tot_ahorro_3 = df_hist_calc["Ahorro 3x50+50 ($)"].sum()
    tot_ahorro_combinado = df_hist_calc["Ahorro Total Anual ($)"].sum()
    tot_xlpe_combinado = df_hist_calc["XLPE Ahorrado (kg)"].sum()
    
    with col_hresumen:
        st.success("💰 **Ahorro Total Combinado (2024 – 2026)**")
        st.metric(
            label=f"Ahorro Total Suma (2x50 + 3x50) | {tot_m_2 + tot_m_3:,.0f} m",
            value=f"${tot_ahorro_combinado:,.2f} USD",
            delta=f"{tot_xlpe_combinado:,.1f} kg de XLPE ahorrados",
            delta_color="normal"
        )
        c_sub1, c_sub2 = st.columns(2)
        c_sub1.metric("Aporte 2x50+50", f"${tot_ahorro_2:,.2f}", f"{tot_m_2:,.0f} m", delta_color="off")
        c_sub2.metric("Aporte 3x50+50", f"${tot_ahorro_3:,.2f}", f"{tot_m_3:,.0f} m", delta_color="off")

    st.dataframe(
        df_hist_calc.style.format({
            "Metros Totales": "{:,.0f} m",
            "Ahorro 2x50+50 ($)": "${:,.2f}",
            "Ahorro 3x50+50 ($)": "${:,.2f}",
            "Ahorro Total Anual ($)": "${:,.2f}",
            "Ahorro Acumulado ($)": "${:,.2f}",
            "XLPE Ahorrado (kg)": "{:,.2f} kg"
        }),
        use_container_width=True,
        hide_index=True
    )
    
    col_hg1, col_hg2 = st.columns(2)
    
    with col_hg1:
        st.markdown("**Ahorro Anual Combinado por Calibre (2x50+50 + 3x50+50)**")
        df_melted_ahorro = df_hist_calc.melt(
            id_vars=["Año", "Ahorro Total Anual ($)"],
            value_vars=["Ahorro 2x50+50 ($)", "Ahorro 3x50+50 ($)"],
            var_name="Calibre",
            value_name="Ahorro ($)"
        )
        df_melted_ahorro["Calibre"] = df_melted_ahorro["Calibre"].replace({
            "Ahorro 2x50+50 ($)": "2x50 + 50 mm²",
            "Ahorro 3x50+50 ($)": "3x50 + 50 mm²"
        })
        
        fig_hist_sum = px.bar(
            df_melted_ahorro,
            x="Año",
            y="Ahorro ($)",
            color="Calibre",
            barmode="stack",
            text_auto="$,.0f",
            color_discrete_map={"2x50 + 50 mm²": "#00CC96", "3x50 + 50 mm²": "#636EFA"}
        )
        fig_hist_sum.add_trace(
            go.Scatter(
                x=df_hist_calc["Año"],
                y=df_hist_calc["Ahorro Total Anual ($)"],
                text=[f"<b>Total: ${v:,.0f}</b>" for v in df_hist_calc["Ahorro Total Anual ($)"]],
                mode="text",
                textposition="top center",
                showlegend=False
            )
        )
        max_y = df_hist_calc["Ahorro Total Anual ($)"].max() * 1.18 if len(df_hist_calc) > 0 else 100
        fig_hist_sum.update_layout(xaxis_title="", yaxis_title="Ahorro Total (USD)", legend_title="", yaxis=dict(range=[0, max_y]))
        st.plotly_chart(fig_hist_sum, use_container_width=True)
        
    with col_hg2:
        st.markdown("**Curva de Ahorro Acumulado Combinado (2024 – 2026)**")
        fig_hist_acum = px.area(
            df_hist_calc,
            x="Año",
            y="Ahorro Acumulado ($)",
            markers=True,
            text=[f"${v:,.0f}" for v in df_hist_calc["Ahorro Acumulado ($)"]],
            color_discrete_sequence=["#00CC96"]
        )
        fig_hist_acum.update_traces(textposition="top center")
        max_acum = df_hist_calc["Ahorro Acumulado ($)"].max() * 1.18 if len(df_hist_calc) > 0 else 100
        fig_hist_acum.update_layout(xaxis_title="", yaxis_title="Ahorro Acumulado (USD)", yaxis=dict(range=[0, max_acum]))
        st.plotly_chart(fig_hist_acum, use_container_width=True)

# ============================================================
# KILOMETRAJE / VALOR EXACTO A BUSCAR
# ============================================================

ingrekk = st.number_input(
    "Kilometraje / valor exacto a buscar",
    min_value=0,
    value=None,
    placeholder="Ingrese el kilometraje",
    step=1
)


# ============================================================
# NUEVA BÚSQUEDA INDEPENDIENTE EN METROS
# ============================================================

busqueda_metros_input = st.number_input(
    "Valor independiente a buscar en metros",
    min_value=0,
    value=None,
    placeholder="Ingrese el valor en metros",
    step=1
)


# ============================================================
# NUEVO KILOMETRAJE FIJO
# ============================================================

nuevo_km_input = st.number_input(
    "Nuevo kilometraje fijo",
    min_value=0,
    value=None,
    placeholder="Ingrese el nuevo kilometraje",
    step=1
)

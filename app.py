import streamlit as st
import struct
import pandas as pd
import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Monky BIN Analyzer",
    page_icon="🐒",
    layout="wide"
)


# ============================================================
# ESTILO UNDERGROUND
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #080808;
    color: #00ff66;
}

html, body, [class*="css"] {
    font-family: "Courier New", monospace;
}

h1 {
    color: #00ff66 !important;
    font-family: "Courier New", monospace !important;
    font-weight: bold;
    letter-spacing: 3px;
    text-transform: uppercase;
}

h2, h3 {
    color: #00ff66 !important;
    font-family: "Courier New", monospace !important;
}

p {
    color: #b0ffcc;
}

input {
    background-color: #111111 !important;
    color: #00ff66 !important;
    border: 1px solid #00ff66 !important;
    font-family: "Courier New", monospace !important;
}

.stButton > button {
    background-color: #001a0a;
    color: #00ff66;
    border: 1px solid #00ff66;
    border-radius: 0px;
    font-family: "Courier New", monospace;
    font-weight: bold;
    letter-spacing: 2px;
}

.stButton > button:hover {
    background-color: #00ff66;
    color: #000000;
}

[data-testid="stMetric"] {
    background-color: #0d0d0d;
    border: 1px solid #00ff66;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #00ff66 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #00ff66;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.title("🐒 🌿💨 MONKY BIN ANALYZER")

st.write(
    "Busca un valor exacto, realiza un barrido de las tres "
    "últimas cifras y analiza equivalentes en kilómetros "
    "o metros dentro de todo el archivo BIN."
)

st.caption("Concept by Ariel Calacaterra | Developed by DAB")


# ============================================================
# CARGAR ARCHIVO
# ============================================================

archivo = st.file_uploader(
    "Seleccionar archivo BIN",
    type=["bin"]
)


# ============================================================
# VALOR A BUSCAR
# ============================================================

ingrekk = st.number_input(
    "Valor exacto a buscar",
    min_value=0,
    value=None,
    placeholder="Ingrese el valor",
    step=1
)


# ============================================================
# NUEVO KILOMETRAJE
# ============================================================

nuevo_km_input = st.number_input(
    "Nuevo kilometraje fijo",
    min_value=0,
    value=None,
    placeholder="Ingrese el nuevo kilometraje",
    step=1
)


# ============================================================
# MARGEN DE BÚSQUEDA
# ============================================================

MARGEN_BUSQUEDA_METROS = 1_100_000


st.number_input(
    "Margen de búsqueda en metros",
    min_value=0,
    value=MARGEN_BUSQUEDA_METROS,
    step=100_000,
    disabled=True
)


# ============================================================
# UMBRALES
# ============================================================

UMBRAL_KM = 100
UMBRAL_METROS = 100_000


st.info(
    f"Umbral KM: modificación si distancia absoluta < "
    f"**{UMBRAL_KM:,} km** | "
    f"Umbral metros: modificación si distancia absoluta < "
    f"**{UMBRAL_METROS:,} m**"
)


# ============================================================
# BOTONES DE BÚSQUEDA
# ============================================================

col_b1, col_b2 = st.columns(2)


with col_b1:

    buscar_km = st.button(
        "🔎 BÚSQUEDA EN KM",
        type="primary",
        use_container_width=True
    )


with col_b2:

    buscar_metros = st.button(
        "📏 BÚSQUEDA EN METROS",
        type="primary",
        use_container_width=True
    )


# ============================================================
# VALIDACIÓN GENERAL
# ============================================================

buscar = buscar_km or buscar_metros


if buscar:

    if archivo is None:

        st.warning(
            "Primero debes cargar un archivo BIN."
        )

        st.stop()


    if ingrekk is None:

        st.warning(
            "Ingrese el valor exacto a buscar."
        )

        st.stop()


    if nuevo_km_input is None:

        st.warning(
            "Ingrese el nuevo kilometraje fijo."
        )

        st.stop()


    # ========================================================
    # LEER BIN
    # ========================================================

    datos_originales = archivo.read()

    datos_modificados = bytearray(
        datos_originales
    )

    tamaño = len(
        datos_originales
    )

    objetivo = int(
        ingrekk
    )

    nuevo_km = int(
        nuevo_km_input
    )


    # ========================================================
    # LISTAS
    # ========================================================

    resultados_barrido = []

    resultados_metros = []

    direcciones_km = []

    direcciones_metros = []

    direcciones_metros_modificar = []


    # ========================================================
    # INFORMACIÓN ARCHIVO
    # ========================================================

    st.success(
        f"Archivo cargado correctamente: {archivo.name}"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Tamaño BIN",
        f"{tamaño:,} bytes"
    )


    col2.metric(
        "Valor buscado",
        f"{objetivo:,}"
    )


    col3.metric(
        "Nuevo kilometraje",
        f"{nuevo_km:,}"
    )


    # ========================================================
    # ========================================================
    #                 BÚSQUEDA EN KM
    # ========================================================
    # ========================================================

    if buscar_km:

        rango_inicio = (
            objetivo // 1000
        ) * 1000

        rango_fin = (
            rango_inicio + 999
        )


        st.subheader(
            "🔎 Búsqueda en KM"
        )


        st.write(
            f"Valor ingresado: **{objetivo:,} km**"
        )


        st.write(
            f"Rango de las tres últimas cifras: "
            f"**{rango_inicio:,} → {rango_fin:,}**"
        )


        # ====================================================
        # BARRIDO COMPLETO
        # ====================================================

        for direccion in range(
            0,
            tamaño - 3
        ):

            valor = struct.unpack_from(
                "<I",
                datos_originales,
                direccion
            )[0]


            bytes_valor = (
                datos_originales[
                    direccion:direccion + 4
                ]
            )


            if (
                rango_inicio
                <= valor
                <= rango_fin
            ):

                diferencia = (
                    valor
                    - objetivo
                )

                distancia_absoluta = abs(
                    diferencia
                )


                if valor == objetivo:

                    tipo_coincidencia = "🔴 EXACTO"

                elif distancia_absoluta < UMBRAL_KM:

                    tipo_coincidencia = (
                        f"🟡 CERCANO < {UMBRAL_KM} KM"
                    )

                else:

                    tipo_coincidencia = ""


                resultados_barrido.append({

                    "Dirección":
                        f"0x{direccion:04X}",

                    "Valor":
                        valor,

                    "Diferencia desde exacto":
                        diferencia,

                    "Distancia absoluta":
                        distancia_absoluta,

                    "Coincidencia":
                        tipo_coincidencia,

                    "HEX":
                        f"0x{valor:08X}",

                    "Bytes":
                        bytes_valor.hex(
                            " "
                        ).upper()

                })


                # ==========================================
                # DIRECCIONES PARA MODIFICAR
                # ==========================================

                if distancia_absoluta < UMBRAL_KM:

                    direcciones_km.append(
                        direccion
                    )


        # ====================================================
        # DATAFRAME KM
        # ====================================================

        resultado_barrido = pd.DataFrame(
            resultados_barrido
        )


        if resultado_barrido.empty:

            st.warning(
                f"No se encontraron valores entre "
                f"{rango_inicio:,} y "
                f"{rango_fin:,}."
            )

        else:

            resultado_barrido = (
                resultado_barrido
                .sort_values(
                    [
                        "Valor",
                        "Dirección"
                    ]
                )
                .reset_index(
                    drop=True
                )
            )


            st.success(
                f"Se encontraron "
                f"{len(resultado_barrido)} "
                f"coincidencias."
            )


            st.dataframe(
                resultado_barrido,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # EXACTOS
            # =================================================

            exactos = resultado_barrido[
                resultado_barrido[
                    "Valor"
                ] == objetivo
            ]


            st.subheader(
                f"Valor exacto: {objetivo:,}"
            )


            if exactos.empty:

                st.warning(
                    f"No se encontró el valor exacto "
                    f"{objetivo:,}."
                )

            else:

                st.success(
                    f"Se encontraron "
                    f"{len(exactos)} "
                    f"apariciones exactas."
                )


                st.dataframe(
                    exactos,
                    use_container_width=True,
                    hide_index=True
                )


            # =================================================
            # CERCANOS
            # =================================================

            cercanos = resultado_barrido[
                resultado_barrido[
                    "Distancia absoluta"
                ] < UMBRAL_KM
            ]


            st.subheader(
                f"Valores KM que cumplen < "
                f"{UMBRAL_KM:,} km"
            )


            if cercanos.empty:

                st.warning(
                    "No hay valores KM dentro "
                    "del umbral."
                )

            else:

                st.success(
                    f"Se modificarían "
                    f"{len(cercanos)} "
                    f"apariciones KM."
                )


                st.dataframe(
                    cercanos,
                    use_container_width=True,
                    hide_index=True
                )


    # ========================================================
    # ========================================================
    #              BÚSQUEDA DIRECTA EN METROS
    # ========================================================
    # ========================================================

    if buscar_metros:

        objetivo_metros = int(
            ingrekk
        )


        rango_inicio = (
            objetivo_metros // 1000
        ) * 1000

        rango_fin = (
            rango_inicio + 999
        )


        limite_inicio = (
            objetivo_metros
            - MARGEN_BUSQUEDA_METROS
        )

        limite_fin = (
            objetivo_metros
            + MARGEN_BUSQUEDA_METROS
        )


        st.subheader(
            "📏 Búsqueda en metros"
        )


        st.write(
            f"Valor ingresado: "
            f"**{objetivo_metros:,} metros**"
        )


        st.write(
            f"Rango de búsqueda por margen: "
            f"**{limite_inicio:,} → "
            f"{limite_fin:,} metros**"
        )


        st.write(
            f"Barrido de las tres últimas cifras: "
            f"**{rango_inicio:,} → {rango_fin:,}**"
        )


        # ====================================================
        # BARRIDO EN METROS
        # ====================================================

        for direccion in range(
            0,
            tamaño - 3
        ):

            valor = struct.unpack_from(
                "<I",
                datos_originales,
                direccion
            )[0]


            bytes_valor = (
                datos_originales[
                    direccion:direccion + 4
                ]
            )


            if (
                limite_inicio
                <= valor
                <= limite_fin
            ):

                diferencia = (
                    valor
                    - objetivo_metros
                )

                distancia_absoluta = abs(
                    diferencia
                )


                resultados_metros.append({

                    "Dirección":
                        f"0x{direccion:04X}",

                    "Valor":
                        valor,

                    "Kilómetros":
                        round(
                            valor / 1000,
                            3
                        ),

                    "Metros":
                        valor,

                    "Diferencia (m)":
                        diferencia,

                    "Distancia absoluta":
                        distancia_absoluta,

                    "Modifica":
                        (
                            "SÍ"
                            if distancia_absoluta
                            < UMBRAL_METROS
                            else "NO"
                        ),

                    "HEX":
                        f"0x{valor:08X}",

                    "Bytes":
                        bytes_valor.hex(
                            " "
                        ).upper()

                })


                direcciones_metros.append(
                    direccion
                )


                if distancia_absoluta < UMBRAL_METROS:

                    direcciones_metros_modificar.append(
                        direccion
                    )


        # ====================================================
        # DATAFRAME METROS
        # ====================================================

        resultado_metros = pd.DataFrame(
            resultados_metros
        )


        if resultado_metros.empty:

            st.warning(
                "No se encontraron valores dentro "
                "del margen de búsqueda."
            )

        else:

            resultado_metros = (
                resultado_metros
                .sort_values(
                    "Distancia absoluta"
                )
                .reset_index(
                    drop=True
                )
            )


            st.success(
                f"Se encontraron "
                f"{len(resultado_metros)} "
                f"coincidencias dentro del margen."
            )


            st.dataframe(
                resultado_metros,
                use_container_width=True,
                hide_index=True
            )


            # =================================================
            # METROS A MODIFICAR
            # =================================================

            metros_a_modificar = resultado_metros[
                resultado_metros[
                    "Distancia absoluta"
                ] < UMBRAL_METROS
            ]


            st.subheader(
                f"Valores en metros que cumplen < "
                f"{UMBRAL_METROS:,} m"
            )


            if metros_a_modificar.empty:

                st.warning(
                    "No hay valores en metros dentro "
                    "del umbral."
                )

            else:

                st.success(
                    f"Se modificarían "
                    f"{len(metros_a_modificar)} "
                    f"apariciones en metros."
                )


                st.dataframe(
                    metros_a_modificar,
                    use_container_width=True,
                    hide_index=True
                )


            # =================================================
            # MÁS CERCANO
            # =================================================

            cercano = (
                resultado_metros.iloc[0]
            )


            st.info(
                f"Más cercano al objetivo: "
                f"{cercano['Metros']:,} metros | "
                f"{cercano['Kilómetros']} km | "
                f"Diferencia: "
                f"{cercano['Diferencia (m)']:+,} m | "
                f"Distancia absoluta: "
                f"{cercano['Distancia absoluta']:,} m | "
                f"Dirección: "
                f"{cercano['Dirección']}"
            )


    # ========================================================
    # ========================================================
    #                  MODIFICACIÓN
    # ========================================================
    # ========================================================

    st.subheader(
        "🛠️ Modificación de valores"
    )


    if buscar_km:

        st.write(
            f"Valor KM buscado: "
            f"**{objetivo:,} km**"
        )


    if buscar_metros:

        st.write(
            f"Valor metros buscado: "
            f"**{objetivo:,} m**"
        )


    st.write(
        f"Nuevo kilometraje: "
        f"**{nuevo_km:,} km**"
    )


    st.write(
        f"Nuevo valor base en metros: "
        f"**{nuevo_km * 1000:,} m**"
    )


    st.write(
        f"Umbral KM: "
        f"**< {UMBRAL_KM:,} km**"
    )


    st.write(
        f"Umbral metros: "
        f"**< {UMBRAL_METROS:,} m**"
    )


    # ========================================================
    # CANTIDADES
    # ========================================================

    cantidad_km = len(
        direcciones_km
    )

    cantidad_metros = len(
        direcciones_metros_modificar
    )


    total_modificaciones = (
        cantidad_km
        + cantidad_metros
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "KM a modificar",
        cantidad_km
    )


    col2.metric(
        "Metros a modificar",
        cantidad_metros
    )


    col3.metric(
        "Total modificaciones",
        total_modificaciones
    )


    # ========================================================
    # REALIZAR MODIFICACIONES
    # ========================================================

    if total_modificaciones == 0:

        st.warning(
            "No se encontraron valores "
            "para modificar."
        )


    else:

        modificaciones = []


        # ====================================================
        # MODIFICAR KM
        # ====================================================

        for direccion in direcciones_km:

            valor_anterior = (
                struct.unpack_from(
                    "<I",
                    datos_originales,
                    direccion
                )[0]
            )


            diferencia = (
                valor_anterior
                - objetivo
            )


            distancia_absoluta = abs(
                diferencia
            )


            if valor_anterior == objetivo:

                tipo_modificacion = "KM exacto"

            elif valor_anterior < objetivo:

                tipo_modificacion = (
                    f"KM cercano por debajo "
                    f"(< {UMBRAL_KM} km)"
                )

            else:

                tipo_modificacion = (
                    f"KM cercano por encima "
                    f"(< {UMBRAL_KM} km)"
                )


            nuevo_valor = nuevo_km


            nuevos_bytes = struct.pack(
                "<I",
                nuevo_valor
            )


            datos_modificados[
                direccion:
                direccion + 4
            ] = nuevos_bytes


            modificaciones.append({

                "Tipo":
                    tipo_modificacion,

                "Dirección":
                    f"0x{direccion:04X}",

                "Valor anterior":
                    valor_anterior,

                "Diferencia":
                    diferencia,

                "Distancia absoluta":
                    distancia_absoluta,

                "Nuevo valor":
                    nuevo_valor,

                "Kilómetros":
                    nuevo_valor,

                "Últimas 3 cifras":
                    "",

                "HEX anterior":
                    f"0x{valor_anterior:08X}",

                "HEX nuevo":
                    f"0x{nuevo_valor:08X}",

                "Bytes anteriores":
                    datos_originales[
                        direccion:
                        direccion + 4
                    ].hex(
                        " "
                    ).upper(),

                "Bytes nuevos":
                    nuevos_bytes.hex(
                        " "
                    ).upper()

            })


        # ====================================================
        # GENERAR SUFIJOS
        # ====================================================

        cantidad = len(
            direcciones_metros_modificar
        )


        if cantidad <= 1000:

            sufijos = random.sample(
                range(1000),
                cantidad
            )

        else:

            sufijos = [

                random.randint(
                    0,
                    999
                )

                for _ in range(
                    cantidad
                )

            ]


        # ====================================================
        # MODIFICAR METROS
        # ====================================================

        for direccion, sufijo in zip(
            direcciones_metros_modificar,
            sufijos
        ):

            valor_anterior = (
                struct.unpack_from(
                    "<I",
                    datos_originales,
                    direccion
                )[0]
            )


            # IMPORTANTE:
            # Para metros se compara contra el
            # valor ingresado directamente.

            objetivo_para_metros = int(
                ingrekk
            )


            diferencia = (
                valor_anterior
                - objetivo_para_metros
            )


            distancia_absoluta = abs(
                diferencia
            )


            nuevo_valor = (
                nuevo_km * 1000
            ) + sufijo


            nuevos_bytes = struct.pack(
                "<I",
                nuevo_valor
            )


            datos_modificados[
                direccion:
                direccion + 4
            ] = nuevos_bytes


            modificaciones.append({

                "Tipo":
                    "Metros",

                "Dirección":
                    f"0x{direccion:04X}",

                "Valor anterior":
                    valor_anterior,

                "Diferencia":
                    diferencia,

                "Distancia absoluta":
                    distancia_absoluta,

                "Nuevo valor":
                    nuevo_valor,

                "Kilómetros":
                    round(
                        nuevo_valor / 1000,
                        3
                    ),

                "Últimas 3 cifras":
                    f"{sufijo:03d}",

                "HEX anterior":
                    f"0x{valor_anterior:08X}",

                "HEX nuevo":
                    f"0x{nuevo_valor:08X}",

                "Bytes anteriores":
                    datos_originales[
                        direccion:
                        direccion + 4
                    ].hex(
                        " "
                    ).upper(),

                "Bytes nuevos":
                    nuevos_bytes.hex(
                        " "
                    ).upper()

            })


        # ====================================================
        # DATAFRAME MODIFICACIONES
        # ====================================================

        resultado_modificaciones = pd.DataFrame(
            modificaciones
        )


        st.subheader(
            "📋 Registro de modificaciones"
        )


        st.success(
            f"Se realizaron "
            f"{len(modificaciones)} "
            f"modificaciones."
        )


        st.dataframe(
            resultado_modificaciones,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # VERIFICACIÓN
        # ====================================================

        st.subheader(
            "✓ Verificación"
        )


        errores = 0


        # ====================================================
        # VERIFICAR KM
        # ====================================================

        for direccion in direcciones_km:

            valor_verificado = (
                struct.unpack_from(
                    "<I",
                    datos_modificados,
                    direccion
                )[0]
            )


            if (
                valor_verificado
                != nuevo_km
            ):

                errores += 1


        # ====================================================
        # VERIFICAR METROS
        # ====================================================

        for direccion, sufijo in zip(
            direcciones_metros_modificar,
            sufijos
        ):

            valor_esperado = (
                nuevo_km * 1000
            ) + sufijo


            valor_verificado = (
                struct.unpack_from(
                    "<I",
                    datos_modificados,
                    direccion
                )[0]
            )


            if (
                valor_verificado
                != valor_esperado
            ):

                errores += 1


        # ====================================================
        # RESULTADO VERIFICACIÓN
        # ====================================================

        if errores == 0:

            st.success(
                "✓ Todos los reemplazos fueron "
                "verificados correctamente."
            )

        else:

            st.error(
                f"Se detectaron "
                f"{errores} errores "
                f"durante la verificación."
            )


        # ====================================================
        # NOMBRE ARCHIVO
        # ====================================================

        nombre_original = (
            archivo.name
        )


        if nombre_original.lower().endswith(
            ".bin"
        ):

            nombre_salida = (
                nombre_original[:-4]
                + "_MODIFICADO.bin"
            )

        else:

            nombre_salida = (
                nombre_original
                + "_MODIFICADO.bin"
            )


        # ====================================================
        # DESCARGAR BIN
        # ====================================================

        st.subheader(
            "⬇️ Descargar BIN modificado"
        )


        st.download_button(
            label="⬇️ Descargar BIN MODIFICADO",
            data=bytes(
                datos_modificados
            ),
            file_name=nombre_salida,
            mime="application/octet-stream",
            type="primary"
        )


        # ====================================================
        # DESCARGAR CSV
        # ====================================================

        csv_modificaciones = (
            resultado_modificaciones
            .to_csv(
                index=False
            )
            .encode("utf-8")
        )


        st.download_button(
            label="⬇️ Descargar registro de modificaciones",
            data=csv_modificaciones,
            file_name="registro_modificaciones.csv",
            mime="text/csv"
        )


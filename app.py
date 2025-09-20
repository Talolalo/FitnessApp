import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# -------------------------
# Archivos de datos
# -------------------------
RUTINAS_FILE = "rutinas.json"
PROGRESO_FILE = "progreso.csv"

# -------------------------
# Cargar rutinas
# -------------------------
if os.path.exists(RUTINAS_FILE):
    with open(RUTINAS_FILE, "r") as f:
        rutinas = json.load(f)
else:
    # Rutinas iniciales
    rutinas = {
        "A": [
            ["Chest Press", 32, "Maquina 20", "Asiento: 3; Respaldo: 3"],
            ["Pectoral Fly", 39, "Maquina 26", "Asiento: 3"],
            ["Tríceps Polea", 14.7, "Maquina 62", ""],
            ["Abdominal Maquina", 32, "Maquina 40", "Asiento: 3"],
            ["Dip Chin", 32, "", ""]
        ],
        "B": [
            ["Press Militar Maquina", 18, "Maquina 50", ""],
            ["Seated Leg Curl", 38, "Maquina 3", ""],
            ["Leg Extension", 36, "Maquina 2", ""],
            ["Abductor de Cadera", 50, "Maquina 4", ""],
            ["Adductor de Cadera", 45, "", "Maquina"]
        ],
        "C": [
            ["Leg Press", 63, "Maquina 1", ""],
            ["Remada Maquina Agarre Neutro", 36, "Maquina 30", ""],
            ["Vuelo Posterior Alternado Maquina", 32, "Maquina 26", ""],
            ["Curl Bíceps con Mancuerna", 14, "", ""],
            ["Lumbar Maquina", 63, "Maquina 43", ""]
        ]
    }

# -------------------------
# Estado de rutinas
# -------------------------
if "estado" not in st.session_state:
    st.session_state.estado = {nombre: {"pendientes": ejercicios.copy(), "completados": []} 
                               for nombre, ejercicios in rutinas.items()}

# -------------------------
# Funciones
# -------------------------
def guardar_rutinas():
    with open(RUTINAS_FILE, "w") as f:
        json.dump(rutinas, f, indent=4)

def guardar_progreso(ejercicio, kg, rutina):
    df = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), rutina, ejercicio, kg]],
                      columns=["Fecha", "Rutina", "Ejercicio", "Kg"])
    if os.path.exists(PROGRESO_FILE):
        df.to_csv(PROGRESO_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(PROGRESO_FILE, index=False)

# -------------------------
# Interfaz con pestañas
# -------------------------
st.title("🏋️ FitnessApp")

tab1, tab2, tab3 = st.tabs(["Entrenamiento", "Historial", "Personalización"])

# ----------- TAB 1: Entrenamiento -----------
with tab1:
    opcion = st.radio("Elige tu entrenamiento:", list(rutinas.keys()), key="radio_entrenamiento")
    estado = st.session_state.estado[opcion]

    st.subheader("Ejercicios pendientes")
    for i, e in enumerate(estado["pendientes"]):
        if st.button(f"✓ {e[0]} - {e[1]} kg", key=f"pendiente-{opcion}-{i}"):
            estado["pendientes"].remove(e)
            estado["completados"].append(e)
            guardar_progreso(e[0], e[1], opcion)
            st.experimental_rerun()

    if not estado["pendientes"]:
        st.success("🏆 Rutina completada!")

    st.subheader("Ejercicios completados")
    for i, e in enumerate(estado["completados"]):
        if st.button(f"✗ {e[0]} - {e[1]} kg", key=f"completado-{opcion}-{i}"):
            estado["completados"].remove(e)
            estado["pendientes"].append(e)
            st.experimental_rerun()

# ----------- TAB 2: Historial -----------
with tab2:
    st.subheader("Historial de entrenamientos")
    if os.path.exists(PROGRESO_FILE):
        df = pd.read_csv(PROGRESO_FILE)
        st.dataframe(df)
    else:
        st.info("Aún no has completado ningún ejercicio.")

# ----------- TAB 3: Personalización -----------
with tab3:
    st.subheader("Modificar o crear ejercicios y rutinas")
    accion = st.selectbox("Acción:", ["Agregar ejercicio", "Editar ejercicio", "Crear nueva rutina"], key="accion_personalizacion")

    if accion == "Agregar ejercicio":
        rutina_sel = st.selectbox("Selecciona rutina:", list(rutinas.keys()), key="add_rutina")
        nombre = st.text_input("Nombre del ejercicio", key="add_nombre")
        kg = st.number_input("Peso (kg)", min_value=0.0, key="add_kg")
        maquina = st.text_input("Máquina", key="add_maquina")
        ajustes = st.text_input("Ajustes", key="add_ajustes")
        if st.button("Agregar ejercicio", key="boton_add"):
            rutinas[rutina_sel].append([nombre, kg, maquina, ajustes])
            guardar_rutinas()
            st.success("Ejercicio agregado!")

    elif accion == "Editar ejercicio":
        st.subheader("Editar ejercicio")
        rutina_sel = st.selectbox("Selecciona rutina:", list(rutinas.keys()), key="edit_rutina")
        nombres_ejercicios = [e[0] for e in rutinas[rutina_sel]]
        ejercicio_seleccionado = st.selectbox("Selecciona ejercicio a modificar:", nombres_ejercicios, key="edit_ejercicio")
        ejercicio_idx = nombres_ejercicios.index(ejercicio_seleccionado)

        # Inputs para editar valores
        nuevo_nombre = st.text_input("Nombre del ejercicio:", rutinas[rutina_sel][ejercicio_idx][0], key="input_nombre")
        nuevo_peso = st.number_input("Peso (kg):", value=rutinas[rutina_sel][ejercicio_idx][1], key="input_peso")
        nuevo_maquina = st.text_input("Máquina:", rutinas[rutina_sel][ejercicio_idx][2], key="input_maquina")
        nueva_config = st.text_input("Configuración:", rutinas[rutina_sel][ejercicio_idx][3], key="input_config")

        if st.button("Guardar cambios", key="boton_guardar"):
            rutinas[rutina_sel][ejercicio_idx] = [nuevo_nombre, nuevo_peso, nuevo_maquina, nueva_config]
            guardar_rutinas()
            st.success("Ejercicio actualizado correctamente!")

    elif accion == "Crear nueva rutina":
        nueva_rutina = st.text_input("Nombre de la nueva rutina", key="nueva_rutina")
        if st.button("Crear rutina", key="boton_crear_rutina"):
            if nueva_rutina and nueva_rutina not in rutinas:
                rutinas[nueva_rutina] = []
                guardar_rutinas()
                st.success(f"Rutina '{nueva_rutina}' creada!")
            else:
                st.error("Nombre inválido o ya existe.")

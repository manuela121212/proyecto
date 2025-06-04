import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from PIL import Image
from geopy.geocoders import Nominatim
import os
import csv
import pandas as pd
import folium 
import folium.plugins
from streamlit_folium import st_folium 
from folium.plugins import MarkerCluster
from groq import Groq

geolocalizador = Nominatim(user_agent="streamlit_localizador") 

# TABLAS GOOGLE SHEET

#urls de las hojas con las tablas
url1 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=2113758662"
url2 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=1988635410"
url3 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=588298795"
url4 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=618124138"

#urls de edición
url5 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=1159460135"
url6 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=517307069"
url7 = "https://docs.google.com/spreadsheets/d/171PnTEEBC2PBSvmqfvkPS_GbvCMJTPijVd5FlAIaYEY/export?format=csv&gid=606498095"

# función para cargar y limpiar los datos
def cargar_datos():
    df1 = pd.read_csv(url1)
    df2 = pd.read_csv(url2)
    df3 = pd.read_csv(url3)
    df4 = pd.read_csv(url4)
    df5 = pd.read_csv(url5)
    df6 = pd.read_csv(url6)
    df7 = pd.read_csv(url7)

    #dropna elimina las filas que tienen un valor vacío o nulo
    # df2[df2.columns[0]].astype(str): convierte la primera columna a texto
    # pd.to_numeric(df2[df2.columns[1]]): convierte la segunda a números
    # errors='coerce': si no se puede convertir, se convierte en nulo o lo reemplaza por NaN
    df2 = df2.dropna()
    df2[df2.columns[0]] = df2[df2.columns[0]].astype(str)
    df2[df2.columns[1]] = pd.to_numeric(df2[df2.columns[1]], errors='coerce')
    df2 = df2.dropna()

    df3 = df3.dropna()
    df3[df3.columns[0]] = df3[df3.columns[0]].astype(str)
    df3[df3.columns[1]] = pd.to_numeric(df3[df3.columns[1]], errors='coerce')
    df3 = df3.dropna()

    df4 = df4.dropna()
    df4[df4.columns[0]] = df4[df4.columns[0]].astype(str)
    df4[df4.columns[1]] = pd.to_numeric(df4[df4.columns[1]], errors='coerce')
    df4 = df4.dropna()

    df5 = df5.dropna()
    df5[df5.columns[0]] = df5[df5.columns[0]].astype(str)
    df5[df5.columns[1]] = pd.to_numeric(df5[df5.columns[1]], errors='coerce')
    df5 = df5.dropna()

    df6 = df6.dropna()
    df6[df6.columns[0]] = df6[df6.columns[0]].astype(str)
    df6[df6.columns[1]] = pd.to_numeric(df6[df6.columns[1]], errors='coerce')
    df6 = df6.dropna()

    df7 = df7.dropna()
    df7[df7.columns[0]] = df7[df7.columns[0]].astype(str)
    df7[df7.columns[1]] = pd.to_numeric(df7[df7.columns[1]], errors='coerce')
    df7 = df7.dropna()

    return df1, df2, df3, df4, df5, df6, df7

# FORMULARIO

# crear la BBDD y la tabla
def inicializar_db():
    conexion = sqlite3.connect('quejas_ciudadanas.db')
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS QUEJAS
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                apellido TEXT,
                correo TEXT,
                ciudad TEXT,
                direccion TEXT,
                telefono TEXT,
                categoria TEXT,
                descripcion TEXT
            )
    ''')
    conexion.commit()
    conexion.close()

# función para insertar una nueva queja
def nueva_queja(nombre, apellido, correo, ciudad, direccion, telefono, categoria, descripcion):
    conexion = sqlite3.connect('quejas_ciudadanas.db')
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO QUEJAS (nombre, apellido, correo, ciudad, direccion, telefono, categoria, descripcion) VALUES (?,?,?,?,?,?,?,?)", (nombre, apellido, correo, ciudad, direccion, telefono, categoria, descripcion))
    conexion.commit()
    conexion.close()

#inicializar base de datos
inicializar_db()

# SIDE BAR
menu = ['Inicio', 'Análisis de tablas', 'Chat de ayuda', 'Formulario de quejas', 'Mapa de quejas', 'Dataframe direcciones']
seleccion = st.sidebar.selectbox('Selecciona una opción', menu)

if seleccion == 'Inicio':
    st.title('PROYECTO FINAL CICLO 2')
    st.header('Aquí encontrarás')
    st.write('''
        - Análisis de tablas y gráficos con Google Sheet
        - Asistente de IA integrado con tres modelos diferentes
        - Formulario inteligente de quejas para participación ciudadana
        - Mapas para visualizar las quejas de los ciudadanos
        - Dataframe con las ubicaciones de las quejas           
    ''')

elif seleccion == 'Análisis de tablas':
    # cargar los datos
    df1, df2, df3, df4, df5, df6, df7 = cargar_datos()

    st.title('Dataset Fórmula 1')

    tab1, tab2, tab3 = st.tabs(['Todos los datos', 'Tablas con Queries', 'Tablas de edición'])

    with tab1:
        st.subheader('Campeonato de conductores de F1 (1950-2020)')
        st.dataframe(df1)
        
    with tab2:
        seleccionar_tabla = st.radio('Tablas de datos', options=['Constructores', 'Pilotos', 'Países'], horizontal=True, key='radio1')

        if seleccionar_tabla == 'Constructores':
            st.subheader('Constructores con más puntos')
            st.dataframe(df2)

        elif seleccionar_tabla == 'Pilotos':
            st.subheader('Puntos totales de pilotos actuales')
            st.dataframe(df3)

        else:
            st.subheader('Puntos totales por país')
            st.dataframe(df4)

    with tab3:
        seleccionar_tabla_edicion = st.radio('Tablas de datos', options=['Constructores', 'Pilotos', 'Países'], horizontal=True, key='radio2')

        if seleccionar_tabla_edicion == 'Constructores':
            @st.experimental_fragment(run_every=2)
            def cargar_hoja5():
                _, _, _, _, df5, _, _, = cargar_datos()
                st.subheader('Edición tabla constructores')
                st.dataframe(df5)

            cargar_hoja5()

            @st.experimental_fragment(run_every=2)
            def grafico_hoja5():
                _, _, _, _, df5, _, _, = cargar_datos()
                st.subheader('Gráfico')
                fig = px.bar(
                    df5,
                    x = df5.columns[0],
                    y = df5.columns[1],
                    title="Constructores con más puntos",
                    color = df5.columns[0]
                )
                st.plotly_chart(fig, use_container_width=True)

            grafico_hoja5()
        
        elif seleccionar_tabla_edicion == 'Pilotos':
            @st.experimental_fragment(run_every=2)
            def cargar_hoja6():
                _, _, _, _, _, df6, _, = cargar_datos()
                st.subheader('Edición tabla pilotos')
                st.dataframe(df6)

            cargar_hoja6()

            @st.experimental_fragment(run_every=2)
            def grafico_hoja6():
                _, _, _, _, _, df6, _, = cargar_datos()
                st.subheader('Gráfico')
                fig = px.bar(
                    df6,
                    x = df6.columns[0],
                    y = df6.columns[1],
                    title="Puntos totales de pilotos actuales",
                    color = df6.columns[0]
                )
                st.plotly_chart(fig, use_container_width=True)

            grafico_hoja6()
        
        else:
            @st.experimental_fragment(run_every=2)
            def cargar_hoja7():
                _, _, _, _, _, _, df7, = cargar_datos()
                st.subheader('Edición tabla países')
                st.dataframe(df7)

            cargar_hoja7()

            @st.experimental_fragment(run_every=2)
            def grafico_hoja7():
                _, _, _, _, _, _, df7, = cargar_datos()
                st.subheader('Gráfico')
                fig = px.bar(
                    df7,
                    x = df7.columns[0],
                    y = df7.columns[1],
                    title="Puntos totales por país",
                    color = df7.columns[0]
                )
                st.plotly_chart(fig, use_container_width=True)

            grafico_hoja7()
    
elif seleccion == 'Formulario de quejas':
    st.title('Formulario de quejas ciudadanas')

    with st.form(key='form_quejas'):
        nombre = st.text_input('Nombre')
        apellido = st.text_input('Apellido')
        correo = st.text_input('Correo')
        ciudad = st.text_input('Ciudad')
        direccion = st.text_input('Dirección', placeholder='Ejemplo: Calle 10 43A-30, Medellín, Colombia')
        telefono = st.text_input('Teléfono')
        categoria = st.radio('Categoría', options=['Seguridad', 'Servicios', 'Infraestructura'], horizontal=True, key='radio_form')
        descripcion = st.text_area('Descripción')
        evidencia = st.file_uploader('Sube una imagen de evidencia si deseas', type=['jpg', 'jpeg', 'png'])

        #mostrar la imagen subida
        if evidencia is not None:
            imagen = Image.open(evidencia)
            st.image(imagen, use_container_width=True)

        enviar = st.form_submit_button(label='Enviar')

        #guardar
        archivo = 'registros.csv'
            
        if enviar:
            if nombre.strip() == '' or apellido.strip() == '' or correo.strip() == '' or ciudad.strip() == '' or direccion.strip() == '' or telefono.strip() == '' or descripcion.strip() == '':
                st.warning('Por favor completa todos los campos')

            else:
                ubicacion = geolocalizador.geocode(direccion)

                if ubicacion:
                    lat = ubicacion.latitude
                    lon = ubicacion.longitude
                    registros_csv = not os.path.exists(archivo) # verifica si el archivo .csv ya existe o no para agregar o no el encabezado.
                    
                    # se escribe en el archivo csv para agregar los datos
                    with open(archivo, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        if registros_csv:
                            writer.writerow(['Ciudad','Dirección', 'Latitud', 'Longitud', 'Categoría']) 
                        writer.writerow([ciudad, direccion, lat, lon, categoria])

                    st.success('Formulario enviado con éxito y dirección geolocalizada')
                    nueva_queja(nombre, apellido, correo, ciudad, direccion, telefono, categoria, descripcion)

                else:
                    st.error("Dirección no encontrada. Intenta escribirla de otra forma.")

elif seleccion == 'Dataframe direcciones':
    archivo = 'registros.csv'

    # Mostrar tabla si el archivo existe
    if os.path.exists(archivo):
        st.title("Registros guardados con coordenadas:")
        df = pd.read_csv(archivo)
        st.dataframe(df)

elif seleccion == 'Mapa de quejas':
    df = pd.read_csv('registros.csv')

    st.title('Mapa de quejas')
    
    tipoMapa = st.radio('Tipo de marcadores', options=['Grupo', 'Individual'], horizontal=True)
    mapa = folium.Map(location=[6.242827227796505, -75.6132478], zoom_start=10) 

    colores_categoria = {
        "Seguridad": "red",
        "Servicios": "green",
        "Infraestructura": "orange"
    }
    
    if tipoMapa == 'Grupo':
        mapa_grupo = MarkerCluster().add_to(mapa) 

    for index, row in df.iterrows():
        marker = folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=row['Categoría'],
            icon=folium.Icon(color=colores_categoria.get(row['Categoría']), icon="info-sign"),
        )
        if tipoMapa == 'Grupo':
            marker.add_to(mapa_grupo)
        else:
            marker.add_to(mapa)

    folium.plugins.Fullscreen(
        position="topright",
        title="Pantalla Completa",
        title_cancel="cancelar",
        force_separate_button=True,
    ).add_to(mapa)

    out = st_folium(mapa, height=600, use_container_width=True)

elif seleccion == 'Chat de ayuda':
    st.title('Groq Bot')

    #declaramos el cliente de groq
    client = Groq(api_key='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')

    modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'gemma2-9b-it']

    # i es un fragmento de la respuesta que me dará la ia
    # i.choices[0] accede al primer resultado generado
    # .delta es el diccionario en donde está el contenido (la mejor respuesta por parte de la ia)
    # .content es la clave de ese diccionario (la respuesta)
    # yield lo muestra uno a uno

    def generar_respuestas_chat(respuesta_ia):
        for i in respuesta_ia:
            if i.choices[0].delta.content:
                yield i.choices[0].delta.content

    # inicializamos el historial de streamlit
    # st.session_state.messages = [] es una lista que se utiliza para guardar el historial completo del chat
    if 'mensajes' not in st.session_state:
        st.session_state.mensajes = []

    # mostrar todo el historial del chat en la pantalla de streamlit
    # st.container(): crea un contenedor visual en streamlit
    # for mensaje in st.session_state.mensajes: recorre uno a uno los mensajes guardados en la lista en donde se guarda el historial
    # st.chat_message(mensaje['role']): crea una simulación de un chat intercambiando roles (usuario y máquina)
    # st.markdown(mensaje['content']): muestra el contenido del mensaje (el texto del usuario o de la ia)
    with st.container():
        for mensaje in st.session_state.mensajes:
            with st.chat_message(mensaje['role']):
                st.markdown(mensaje['content'])

    eleccion_modelos = st.sidebar.selectbox('Modelos', options=modelos, index=0)

    prompt = st.chat_input('¿Qué quieres saber?')

    if prompt:
        st.chat_message('user').markdown(prompt) # mostrar el mensaje (prompt) dentro de la interfaz de chat en streamlit
        st.session_state.mensajes.append({'role':'user', 'content': prompt})

        try:
            mensajes_conversacion = st.session_state.mensajes
            respuesta_ia = client.chat.completions.create(
                model = eleccion_modelos,
                messages = mensajes_conversacion,
                stream = True
            )
        
            with st.chat_message('assistant'):
                respuestas_bot = generar_respuestas_chat(respuesta_ia)
                # st.write_stream(respuestas_bot) recibe el generador de texto que se hizo con el yield 
                respuesta_completa = st.write_stream(respuestas_bot) 
            st.session_state.mensajes.append({'role':'assistant', 'content':respuesta_completa})

        except Exception as e:
            st.error(e)



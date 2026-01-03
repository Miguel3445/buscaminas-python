import tkinter as tk
import random
import winsound
import os
import sys
# Detecta si la aplicación está ejecutándose como archivo empaquetado (.exe)
# o directamente desde el script, para definir correctamente el directorio base
# y poder acceder a los recursos (imágenes, sonidos, etc.).
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(__file__)

# Directorio base para los recursos gráficos
IMAGES_DIR = os.path.join(BASE_DIR, "images")


# ---------- Constantes y límites de configuración ----------
# Estos límites se definieron para garantizar que incluso el tablero de mayor tamaño
# se visualice correctamente en pantallas de tamaño estándar (portátiles y monitores comunes),
# evitando desbordes o problemas de escala en la interfaz.

TAM_CELDA=35
FILAS_MIN = 4
FILAS_MAX = 17

COLUMNAS_MIN = 4
COLUMNAS_MAX = 35

MINAS_MIN = 1
MINAS_MAX = 500

# ---------- variables de estado global ----------
#de UI
frame_tablero = None
frame_controles = None


#principales para el juego
juego_activo = False
modo_actual = 0  # 0 = revelar, 2 = bandera
btn_bandera = None
btn_reiniciar = None
lbl_estado = None
lbl_contador = None

#para la apertura y cierre de la configuración(animacion principalmente)
config_abierta = False
frame_config = None
config_visible = False
config_x = 1.0   # posición relativa (1.0 = fuera del la ventana)

# ---------- ESTRUCTURAS ----------
tablero_logico = []
labels_tablero = []
tableroDeJuego = []
tableroDeJuegoMatriz = []
celdas_animacion = [] #para la animacion de la aparicion del tablero
COLORES_NUMEROS = { #diccionario
    1: "blue",
    2: "green",
    3: "red",
    4: "navy",
    5: "brown",
    6: "turquoise",
    7: "black",
    8: "gray"
}


def crearFrameInicio():
    global frame_inicio

    frame_inicio = tk.Frame(ventana, bg="#2f4f2f")
    frame_inicio.place(relx=0.5, rely=0.5, anchor="center")
    frame_inicio.configure(padx=80, pady=50)

    lbl_titulo = tk.Label(
        frame_inicio,
        text="BUSCAMINAS",
        font=("Arial", 30, "bold"),
        fg="#f5f5f5",
        bg="#2f4f2f"
    )
    lbl_titulo.pack(pady=(0, 10))

    lbl_subtitulo = tk.Label(
        frame_inicio,
        text="Classic Retro Game",
        font=("Arial", 14, "italic"),
        fg="#cfcfcf",
        bg="#2f4f2f"
    )
    lbl_subtitulo.pack(pady=(0, 25))

    frame_imagen = tk.Frame(
        frame_inicio,
        width=300,
        height=160,
        bg="#1a1a1a",
        bd=4,
        relief="ridge"
    )
    frame_imagen.pack(pady=15)
    frame_imagen.pack_propagate(False)

    lbl_img_placeholder = tk.Label(
        frame_imagen,
        image=RECURSOS["imagen_portada"],
        bg="#1f1f1f"
    )
    lbl_img_placeholder.place(relx=0.5, rely=0.5, anchor="center")

    btn_inicio = tk.Button(
        frame_inicio,
        text="▶ INICIAR JUEGO",
        font=("Arial", 18, "bold"),
        bg="#4caf50",
        fg="black",
        activebackground="#66bb6a",
        padx=40,
        pady=15,
        cursor="hand2",
        relief="raised",
        bd=4,
        command=iniciarDesdeMenu
    )
    btn_inicio.pack(pady=(25, 15))

    btn_config = tk.Button(
        frame_inicio,
        text="⚙ CONFIGURACIÓN",
        font=("Arial", 14, "bold"),
        bg="#c0c0c0",
        fg="black",
        activebackground="#d6d6d6",
        padx=25,
        pady=8,
        cursor="hand2",
        relief="raised",
        bd=3,
        command=toggleConfiguracion
    )
    btn_config.pack(pady=(0, 20))


#funciones de configuracion(panel de configuracion, validacion de los entrys)
def config():
    try:
        #obtiene los datos de los entrys en forma de entero
        filas = int(var_filas.get())
        columnas = int(var_columnas.get())
        minas = int(var_minas.get())

        inicioVerificado = verificarConfig(filas, columnas, minas)
        if inicioVerificado == 1:
            lbl_estado.config(text="", fg="white")
            return 1
        else:
            return 0
    except ValueError:
        juego_activo = False
        lbl_estado.config(
            text="Parámetro inválido, se detecto una letra",
            fg="orange"
        )
        return 0

def verificarConfig(filas, columnas, minas):

    global FILAS, COLUMNAS, MINAS #variables principales de configuración
    #el lbl_estado es el recuadro en el que se imprimen los mensajes de error, victoria y derrota
    if not (FILAS_MIN <= filas <= FILAS_MAX):
        lbl_estado.config(text="Parámetro inválido, Filas inválidas", fg="orange")
        return 0

    if not (COLUMNAS_MIN <= columnas <= COLUMNAS_MAX):
        lbl_estado.config(text="Parámetro inválido, Columnas inválidas", fg="orange")
        return 0

    if not (MINAS_MIN <= minas <= MINAS_MAX):
        lbl_estado.config(text="Parámetro inválido, Minas inválidas", fg="orange")
        return 0

    # VALIDACIÓN PARA QUE LAS MINAS NO SUPEREN EL RANGO DEL TABLERO
    if minas >= filas * columnas:
        lbl_estado.config(
            text="Parámetro inválido, demasiadas minas para el tablero",
            fg="orange"
        )
        return 0

    # si pasa todas las validaciónes se asigna el parametro a las variables globales
    FILAS = filas
    COLUMNAS = columnas
    MINAS = minas

    return 1

#esta funcion solo crea el aspecto visual del frame
def crearPanelConfiguracion():
    global frame_config #se crea de manera global para poderlo editar en otras funciones

    if frame_config:
        return

    #ventana del panel de configuración
    frame_config = tk.Frame(
        ventana,
        bg="#4a4a4a",     # Color un poco más claro
        bd=2,             # Borde fino
        relief="ridge",   # Estilo de borde
        width=320,
        height=280
    )

    frame_config.pack_propagate(False)#de esta manera el contenedor siempre tendra un tamaño fijo 

    tk.Label(
        frame_config,#se crea el label sobre el frame_config
        text="CONFIGURACIÓN",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#4a4a4a",
        anchor="w"        # Alineación a la izquierda
    ).pack(
        fill="x",
        pady=(15, 20),
        padx=15
    )

    # Se utiliza un bucle for para evitar repetir código.
    # Cada iteración crea una fila de configuración compuesta por:
    #   - Un Label (texto descriptivo)
    #   - Un Entry (campo de entrada)
    #
    # La estructura que se recorre es una tupla de pares (texto, variable),
    # donde:
    #   texto -> cadena que se mostrará en el Label
    #   var   -> variable Tkinter asociada al Entry (IntVar, StringVar, etc.)
    for texto, var in (
        ("Filas (4 - 17):", var_filas),
        ("Columnas (4 - 35):", var_columnas),
        ("Minas:", var_minas),
    ):

        # Se crea un Frame contenedor para cada fila de configuración.
        # Esto permite agrupar el Label y el Entry horizontalmente
        # y manejar el espaciado de forma más ordenada.
        fila = tk.Frame(
            frame_config,
            bg="#4a4a4a"   # Color de fondo uniforme para toda la fila
        )
        fila.pack(
            fill="x",
            pady=6,
            padx=15
        )

        # Se crea el Label que describe el valor a ingresar.
        # El texto cambia en cada iteración, pero el estilo se mantiene.
        tk.Label(
            fila,
            text=texto,            # Texto descriptivo (Filas, Columnas, Minas)
            font=("Arial", 13),    # Fuente ligeramente más compacta
            fg="white",            # Color del texto
            bg="#4a4a4a",
            anchor="w",            # Alineación izquierda real
            width=18               # Ancho fijo para alineación uniforme
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # Se crea el campo de entrada asociado al Label.
        # Cada Entry queda enlazado a una variable distinta mediante textvariable,
        # permitiendo leer y modificar su valor desde el código.
        tk.Entry(
            fila,
            width=6,               # Un poco más ancho
            textvariable=var,
            justify="center",      # Texto centrado dentro del Entry
            relief="solid",
            bd=1
        ).pack(
            side="left"
        )


#primera función que se llama al presionar el botón de configuración
def toggleConfiguracion():
    if config_visible: #con esta validación hacemos que al presionar el btn_config se abra el panel de configuración, y si volvemos a presionar se cierra
        cerrarConfiguracion()
    else:
        abrirConfiguracion()

def abrirConfiguracion():
    global config_visible, config_x

    if config_visible:
        return

    crearPanelConfiguracion()
    config_visible = True
    animarConfigEntrada()
    

        
def cerrarConfiguracion():
    global config_visible, config_x

    if not config_visible:
        return

    animarConfigSalida()
    


                            
#funcion de sonido, la libreria usada winsound es para windows unicamente.
def reproducirSonido(ruta):
    if os.path.exists(ruta):
        winsound.PlaySound(
            ruta,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )


#CONTROL DE FLUJO(menú, inicio, validación)
          
def iniciarDesdeMenu():
    cerrarConfiguracion() #esta función esta para que el panel de configuración no quede abierto
    if config() == 1:
        frame_inicio.place_forget() #oculta el widget que fue posicionado con place pero sin destruirlo
        iniciarJuego()
        
        
        
# ---------- INICIAR JUEGO ---------- esta es la que crea todo el tablero de control, los botones
def iniciarJuego():
    #concepto clave, este global, no es global para todo el archivo, por eso en la otra funcion de irAinicio() tambien debemos asignarlas como global para poder reasignar o usar el valor guardado aqui
    global juego_activo, frame_tablero, frame_controles 

    resetearModo()
    if frame_tablero:
        frame_tablero.destroy()
    if frame_controles:
        frame_controles.destroy()

    lbl_estado.config(text="")

    frame_controles = tk.Frame( #frame sobre el que estan los botones de control(volver, reiniciar, poner bandera, contador)
        ventana,
        bg="#ddd7ce", #color de la barra de controles
        bd=2,
        relief="ridge",
        padx=20,
        pady=5
    )

    frame_controles.pack(pady=1)
    
    btn_inicio_menu = tk.Button(
    frame_controles,
    image=RECURSOS["icono_inicio"],
    command=irAinicio,
    relief="flat",
    #bg="#e0e0e0",
    bg="#ddd7ce", 
    activebackground="#d0d0d0",
    padx=20,
    pady=20,
    cursor="hand2"
    )
    btn_inicio_menu.pack(side="left", padx=30)

    
    global btn_reiniciar
    btn_reiniciar = tk.Button(
        frame_controles,
        image=RECURSOS["icono_reiniciar"],
        command=iniciarJuego,
        relief="flat",
        #bg="#e0e0e0",
        bg="#ddd7ce", 
        activebackground="#d0d0d0",
        padx=20,
        pady=20,
        cursor="hand2"
    )
    btn_reiniciar.pack(side="left", padx=30)
    
    
    global btn_bandera
    btn_bandera = tk.Button(
        frame_controles,
        image=RECURSOS["icono_bandera"],
        command=lambda: eventos(2), #llama a la función de eventos
        relief="flat",
        #bg="#e0e0e0",
        bg="#ddd7ce", 
        activebackground="#d0d0d0",
        padx=20,
        pady=20,
        cursor="hand2"
    )
    btn_bandera.pack(side="left", padx=30)
    
    
    global lbl_contador
    lbl_contador = tk.Label(
        frame_controles,
        text="0",
        font=("Arial", 20, "bold"),
        bg="#7b1e1e",     # vinotinto
        fg="red",
        width=4
    )
    lbl_contador.pack(side="left", padx=30)
    
    
    frame_tablero = tk.Frame( #frame principal sobre el que se imprime el tablero para jugar
    ventana,
    bg="#1a1a1a",     # fondo interno del tablero
    bd=4,             # grosor del borde
    relief="ridge"    # estilo del borde (queda bien tipo juego)
    )
    frame_tablero.place(relx=0.5, rely=0.51, anchor="center")
    
    iniciarTableros()
    colocarMinas()
    ponerNumerosAbyacentes()
    imprimirTableros()
    juego_activo = False
    animarAparicionTablero()
    reproducirSonido(RECURSOS["SONIDO_INICIO"]) #se reproduce cuando el juego ya arranco correctamente.

def actualizarContador():
    if lbl_contador is None:
        return
    
    total_validas = FILAS * COLUMNAS - MINAS
    reveladas = 0

    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tableroDeJuegoMatriz[i][j] == 1 and tablero_logico[i][j] != 9:
                reveladas += 1

    restantes = total_validas - reveladas
    lbl_contador.config(text=str(restantes))
    
    

#función para volver al menú inicial
def irAinicio():
    global juego_activo, frame_tablero, frame_controles
    resetearModo()
    juego_activo = False #se devuelve a false porque ya estamos en el menú de inicio

    if frame_tablero:
        frame_tablero.destroy()
        frame_tablero = None

    if frame_controles:
        frame_controles.destroy()
        frame_controles = None

    lbl_estado.config(text="")

    frame_inicio.place(relx=0.5, rely=0.5, anchor="center")


# ---------- EVENTOS Y MODOS----------
def eventos(tipo):
    global modo_actual
    modo_actual = tipo

    if tipo == 2:
        btn_bandera.config(bg="#c0392b", activebackground="#c0392b")

def resetearModo():
    global modo_actual
    modo_actual = 0 #queda en modo revelar
    
# poner bandera
def ponerBandera(fil, col):
    global modo_actual #el modo actual debe ser dos

    if tableroDeJuegoMatriz[fil][col] == 1:
        return

    if tableroDeJuegoMatriz[fil][col] == 3:
        tableroDeJuegoMatriz[fil][col] = 0
    else:
        tableroDeJuegoMatriz[fil][col] = 3

    imprimirTableros() #dado que se hace un cambio en tableroDeJuegoMatriz volvemos a imprimir los tableros para que se vea la bandera puesta

    btn_bandera.config(bg="#ddd7ce", activebackground="#d0d0d0")
    modo_actual = 0


# ---------- LOGICA DEL JUEGO ----------
def revelacionRecursiva(fil, col):
    if fil < 0 or fil >= FILAS or col < 0 or col >= COLUMNAS:
        return
    if tableroDeJuegoMatriz[fil][col] == 1:
        return

    tableroDeJuegoMatriz[fil][col] = 1

    if tableroDeJuego[fil][col] is not None:
        tableroDeJuego[fil][col].destroy()
        tableroDeJuego[fil][col] = None

    if tablero_logico[fil][col] > 0:
        return

    for df in range(-1, 2):
        for dc in range(-1, 2):
            if df == 0 and dc == 0:
                continue
            revelacionRecursiva(fil + df, col + dc)

# derrota
def perderJuego(fil, col):
    global juego_activo

    if not juego_activo:
        return

    reproducirSonido(RECURSOS["SONIDO_PERDER"])
    juego_activo = False #se desactiva el juego

    # Mina clickeada primero (impacto)
    if tableroDeJuego[fil][col] is not None:
        tableroDeJuego[fil][col].destroy()
        tableroDeJuego[fil][col] = None

    tableroDeJuegoMatriz[fil][col] = 1
    imprimirTableros()

    # Animación del resto de minas
    minas = obtenerMinas()
    ventana.after(150, lambda: animarDerrota(minas))

    btn_reiniciar.config(image=RECURSOS["icono_perder"])
    btn_reiniciar.image = RECURSOS["icono_perder"]

    lbl_estado.config(text="Has perdido", fg="red")

    
    
def verificarVictoria():
    global juego_activo

    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tablero_logico[i][j] != 9 and tableroDeJuegoMatriz[i][j] == 0:
                return 0

    reproducirSonido(RECURSOS["SONIDO_GANAR"])
    # VICTORIA
    juego_activo = False
    lbl_estado.config(text="Has ganado", fg="green")

    # Bloqueo visual del tablero
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tableroDeJuego[i][j] is not None:
                tableroDeJuego[i][j].destroy()
                tableroDeJuego[i][j] = None

    return 1

#cuando el usuario da click al un boton del tablero de juego
def revelar(fil, col):
    global modo_actual

    if not juego_activo:
        return

    # Modo bandera
    if modo_actual == 2:
        ponerBandera(fil, col)
        return

    # Ya revelada o con bandera
    if tableroDeJuegoMatriz[fil][col] != 0:
        return
    
    reproducirSonido(RECURSOS["SONIDO_REVELAR"])
    valor = tablero_logico[fil][col]

    # Mina
    if valor == 9:
        perderJuego(fil, col)
        return

    # Número (>0) no se aplica revelación recursiva, solo se revela la celda
    if valor > 0:
        tableroDeJuegoMatriz[fil][col] = 1
        if tableroDeJuego[fil][col] is not None:
            tableroDeJuego[fil][col].destroy()
            tableroDeJuego[fil][col] = None

        imprimirTableros()
        return

    # Celda vacía → recursivo
    revelacionRecursiva(fil, col)

    # IMPORTANTE: actualizar todo después
    imprimirTableros()

def colocarMinas():
    minas = 0
    while minas < MINAS:
        f = random.randint(0, FILAS - 1)
        c = random.randint(0, COLUMNAS - 1)
        if tablero_logico[f][c] != 9:
            tablero_logico[f][c] = 9
            minas += 1

def ponerNumerosAbyacentes():
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tablero_logico[i][j] == 9:
                for df in range(-1, 2):
                    for dc in range(-1, 2):
                        nf, nc = i + df, j + dc
                        if 0 <= nf < FILAS and 0 <= nc < COLUMNAS:
                            if tablero_logico[nf][nc] != 9:
                                tablero_logico[nf][nc] += 1
                                
                                
                            
        
#=====Animaciones(aparicion del tablero de juego, aparición progresiva de las minas al ser derrotado, aparición progresiva de las minas al ser ganador)
                                
def animarConfigSalida():
    global config_x, config_visible

    if config_x >= 1.0:
        config_visible = False
        return

    config_x += 0.03
    frame_config.place(relx=config_x, rely=0.5, anchor="w")
    ventana.after(15, animarConfigSalida)
    
    
def animarConfigEntrada():
    global config_x

    if config_x <= 0.72:
        return

    config_x -= 0.03
    frame_config.place(relx=config_x, rely=0.5, anchor="w")
    ventana.after(15, animarConfigEntrada)

def animarAparicionTablero(index=0):
    if index >= len(celdas_animacion):
        activarTablero()
        return

    btn = celdas_animacion[index]
    btn.place(x=0, y=0, width=TAM_CELDA, height=TAM_CELDA)

    ventana.after(3, lambda: animarAparicionTablero(index + 1))
    
#funciones para la animacion de la perdida
def obtenerMinas():
    minas = []
    for i in range(FILAS):
        for j in range(COLUMNAS):
            if tablero_logico[i][j] == 9:
                minas.append((i, j))
    return minas
  
def animarDerrota(minas, index=0):
    if index >= len(minas):
        return

    i, j = minas[index]

    tableroDeJuegoMatriz[i][j] = 1

    if tableroDeJuego[i][j] is not None:
        tableroDeJuego[i][j].destroy()
        tableroDeJuego[i][j] = None

    lbl = labels_tablero[i][j]
    lbl.config(image=RECURSOS["imagen_mina"], text="")
    lbl.image = RECURSOS["imagen_mina"]
    delay = max(2, 400 // len(minas))
    ventana.after(delay, lambda: animarDerrota(minas, index + 1))




# ---------- GENERACIÓN DE TABLERO Y UI ----------
def iniciarTableros():
    # Limpia la lista usada para la animación de aparición del tablero
    # Se hace cada vez que se genera un tablero nuevo
    celdas_animacion.clear()

    # Variables globales que representan el estado lógico y visual del juego
    global tablero_logico, labels_tablero
    global tableroDeJuego, tableroDeJuegoMatriz

    # Reinicio de todas las estructuras del tablero
    tablero_logico = []            # Matriz con la información real del juego (minas / números)
    labels_tablero = []            # Labels donde se mostrarán los valores del tablero lógico
    tableroDeJuego = []            # Botones interactivos del jugador
    tableroDeJuegoMatriz = []      # Matriz de estado: no revelada / revelada / bandera

    # Creación de filas del tablero
    for i in range(FILAS):
        fila_logica = []    # Datos reales de la fila
        fila_labels = []    # Labels de la fila
        fila_botones = []   # Botones de la fila
        fila_estado = []    # Estado de cada celda de la fila

        for j in range(COLUMNAS):
            # Inicialización del contenido lógico y estado de la celda
            fila_logica.append(0)
            fila_estado.append(0)

            # Frame que actúa como contenedor de cada celda
            celda = tk.Frame(
                frame_tablero,
                width=TAM_CELDA,
                height=TAM_CELDA,
                bg="#7b7b7b"
            )
            celda.grid(row=i, column=j)
            celda.grid_propagate(False)

            # Label que mostrará el número o la mina (tablero lógico)
            # Se crea desde el inicio pero permanece oculto
            lbl = tk.Label(
                celda,
                bg="#bdbdbd",
                fg="black",
                font=("Arial", 23, "bold"),
                relief="sunken"
            )
            lbl.place_forget()   # No se muestra aún, pero existe en memoria

            fila_labels.append(lbl)

            # Botón que el jugador utiliza para interactuar con la celda
            btn = tk.Button(
                celda,
                relief="raised",
                bg="#cfcfcf",
                activebackground="#b8b8b8",
                borderwidth=1,
                command=lambda f=i, c=j: revelar(f, c),
                cursor="hand2"
            )

            # El botón también se crea oculto y deshabilitado inicialmente
            btn.place_forget()
            btn.config(state="disabled")

            # Se guarda para la animación de entrada del tablero
            celdas_animacion.append(btn)

            fila_botones.append(btn)

        # Al finalizar la fila, se agregan todas las estructuras a sus matrices
        tablero_logico.append(fila_logica)
        labels_tablero.append(fila_labels)
        tableroDeJuego.append(fila_botones)
        tableroDeJuegoMatriz.append(fila_estado)
        
        
def activarTablero():
    global juego_activo

    # Muestra todos los labels del tablero lógico
    # Estos quedan debajo de los botones de juego
    for i in range(FILAS):
        for j in range(COLUMNAS):
            lbl = labels_tablero[i][j]
            lbl.place(x=0, y=0, width=TAM_CELDA, height=TAM_CELDA)

    # Habilita todos los botones para permitir la interacción del jugador
    for fila in tableroDeJuego:
        for btn in fila:
            if btn is not None:
                btn.config(state="normal")

    # Marca el juego como activo
    juego_activo = True




                                                    
def imprimirTableros():
    victoria = verificarVictoria()
    for i in range(FILAS):
        for j in range(COLUMNAS):
            valor = tablero_logico[i][j]
            lbl = labels_tablero[i][j]
            btn = tableroDeJuego[i][j]

            if tableroDeJuegoMatriz[i][j] == 3 and victoria == 0:
                if btn is not None:
                    btn.config(image=RECURSOS["imagen_bandera_puesta"], text="")
                    btn.image = RECURSOS["imagen_bandera_puesta"]
                continue
            else:
                if btn is not None:
                    btn.config(image="", text="")

            if valor == 0:
                lbl.config(text="", image="")
            elif valor == 9:
                if victoria == 1:
                    lbl.config(image=RECURSOS["imagen_mina_segura"], text="")
                    lbl.image = RECURSOS["imagen_mina_segura"]
                else:
                    lbl.config(image=RECURSOS["imagen_mina"], text="")
                    lbl.image = RECURSOS["imagen_mina"]

            else:
                lbl.config(
                    text=str(valor),
                    image="",
                    fg=COLORES_NUMEROS.get(valor, "black")
                )
    actualizarContador()

def cargarRecursos():
    recursos = {}
    # ---------- IMÁGENES ----------
    recursos["icono_inicio"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "iralinicio.png")
    ).subsample(6, 6)

    recursos["imagen_mina"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "bomba.png")
    ).subsample(10, 10)

    recursos["imagen_mina_segura"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "minasegura.png")
    ).subsample(30, 30)

    recursos["icono_reiniciar"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "reiniciar.png")
    ).subsample(13, 13)

    recursos["icono_perder"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "perder.png")
    ).subsample(13, 13)

    recursos["icono_bandera"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "bandera.png")
    ).subsample(19, 19)

    recursos["imagen_bandera_puesta"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "banderaPuesta.png")
    ).subsample(14, 14)

    recursos["imagen_portada"] = tk.PhotoImage(
        file=os.path.join(IMAGES_DIR, "portada.png")
    ).subsample(3, 3)

    # ---------- SONIDOS ----------
    recursos["SONIDO_REVELAR"] = os.path.join(BASE_DIR, "sounds", "revelar.wav")
    recursos["SONIDO_GANAR"] = os.path.join(BASE_DIR, "sounds", "ganar.wav")
    recursos["SONIDO_PERDER"] = os.path.join(BASE_DIR, "sounds", "perder.wav")
    recursos["SONIDO_INICIO"] = os.path.join(BASE_DIR, "sounds", "juegoinciado.wav")

    return recursos


#función principal
def main():
    global ventana, lbl_estado
    global var_filas, var_columnas, var_minas
    global RECURSOS

    ventana = tk.Tk()
    ventana.title("Buscaminas")
    ventana.state("zoomed")
    ventana.configure(bg="#dfe8b6")

    lbl_estado = tk.Label(
        ventana,
        text="",
        font=("Arial", 22, "bold"),
        fg="red",
        bg="#dfe8b6"
    )
    lbl_estado.place(relx=0.5, rely=0.97, anchor="center")

    var_filas = tk.StringVar(value="8")
    var_columnas = tk.StringVar(value="8")
    var_minas = tk.StringVar(value="10")

    #  referencia global
    RECURSOS = cargarRecursos()

    crearFrameInicio()

    ventana.mainloop()


if __name__ == "__main__":  #entry point loop principal
    main()

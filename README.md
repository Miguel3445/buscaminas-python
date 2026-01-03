# Buscaminas en Python (Tkinter)

Juego clásico de **Buscaminas** desarrollado en Python utilizando Tkinter para la interfaz gráfica.

Este proyecto fue construido de forma incremental.
Primero se desarrolló el **algoritmo del juego en lenguaje C**, junto con su diagrama de flujo, creando una versión funcional del Buscaminas en consola.
Posteriormente, utilizando la misma lógica y estructura algorítmica, el proyecto fue migrado a Python, incorporando una **interfaz gráfica** con Tkinter.

El objetivo principal del proyecto fue comprender e implementar la lógica interna del Buscaminas, separando claramente la lógica del juego de la interfaz gráfica, de modo que la integración con la UI fuese más clara y mantenible.


## Características
- Aplicación de consola en (C) + diagrama de flujo 
- Interfaz gráfica con Tkinter
- Menú de inicio de juego
- Panel de controles que cuenta con: volver al inicio, reiniciar, poner bandera, contador
- Generación dinámica del tablero
- Sistema de banderas
- Animaciones al iniciar el juego
- Sonidos incorporados de derrota, victoria e inicio de juego
- Configuración personalisable de filas, columnas y minas(con limites determinados)
- Lógica separada entre tablero lógico y UI
- Manejo de estados del juego (ganar / perder)

---

## Tecnologías utilizadas
- codeblocks, lenguaje C para app de consola
- Draw.io para el diagrama de flujo
- **Python 3**
- **Tkinter** (GUI)
- Manejo de eventos y estados
- Estructuras de datos (matrices, diccionarios)
- Programación con funciones para mejor orden y optimisar el codigo

---
## Ejecución

1. Clonar el repositorio
   ```bash
   git clone https://github.com/usuario/buscaminas-python.git
2. ir al directorio de app_tkinter 
3. ejecutar el main.py
- otra opción es ejecutar el .exe, lo encuentras en la carpeta app_tkinter/dist/main/main.exe

 

## Estructura del proyecto

app_tkinter/
│
├── images/          # Imágenes del juego (iconos, minas, banderas)
├── sounds/          # Sonidos del juego
├── main.py          # Archivo principal
├── README.md
└── dist/            #app empaquetada en el .exe


## Mejoras futuras

- Modularización del código
- Guardado de estadísticas
- Selector de dificultad predefinida
- Temporizador
- Mejoras en el diseño

## Autor
Miguel Ángel Blandón  
Estudiante de Tecnología en Instrumentación Electrónica

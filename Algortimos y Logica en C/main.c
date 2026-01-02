#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Dimensiones del tablero
#define COLUMNAS 8
#define FILAS 8

// Cantidad total de minas
#define MINAS 6

// tableroPrincipal:
//  - 9  -> mina
//  - 0+ -> número de minas adyacentes
int tableroPrincipal[FILAS][COLUMNAS];

// tablerodeJuego (estado visible para el jugador):
//  - 0 -> celda no revelada
//  - 1 -> celda revelada
//  - 3 -> celda marcada con bandera
int tablerodeJuego[FILAS][COLUMNAS];

// Inicializa ambos tableros en cero
// tableroPrincipal: sin minas ni números
// tablerodeJuego: todas las celdas ocultas
void iniciarTableros() {
    for(int i=0;i<FILAS;i++){
        for(int j=0;j<COLUMNAS;j++){
            tablerodeJuego[i][j]=0;
            tableroPrincipal[i][j]=0;
        }
    }
}

// Coloca las minas de forma aleatoria en el tablero principal
// Garantiza que no se sobreescriban minas ya colocadas
void colocarMinas() {
    int contador=0;
    srand(time(NULL));
    int filaAleatoria,columnaAleatoria;

    while(contador<MINAS) {
        filaAleatoria= rand() % FILAS;
        columnaAleatoria= rand() % COLUMNAS;

        if(tableroPrincipal[filaAleatoria][columnaAleatoria] != 9) {
            tableroPrincipal[filaAleatoria][columnaAleatoria] = 9;
            contador++;
        }
    }
}

// Calcula los números adyacentes a cada mina
// Recorre el tablero y, por cada mina encontrada,
// incrementa las celdas vecinas que no sean minas
void ponerNumerosAbyacentes() {
    for(int i=0;i<FILAS; i++) {
        for(int j=0;j<COLUMNAS;j++){
            if(tableroPrincipal[i][j] == 9) { // celda es una mina
                // Desplazamientos relativos (-1, 0, 1) alrededor de la mina
                for(int adyacenteFil=-1; adyacenteFil<=1; adyacenteFil++) {
                    for(int adyacenteCol=-1; adyacenteCol<=1; adyacenteCol++) {
                        int posAdyacenteFil= i + adyacenteFil;
                        int posAdyacenteCol= j + adyacenteCol;

                        // Verifica que la posición esté dentro del tablero
                        if(posAdyacenteCol >= 0 && posAdyacenteCol < COLUMNAS
                            && posAdyacenteFil >= 0 && posAdyacenteFil < FILAS) {

                            // Incrementa solo si la celda no es una mina
                            if(tableroPrincipal[posAdyacenteFil][posAdyacenteCol] != 9) {
                                tableroPrincipal[posAdyacenteFil][posAdyacenteCol]++;
                            }
                        }
                    }
                }
            }
        }
    }
}

// Revela una celda y propaga recursivamente si es un cero
// Retorna 1 si se revela una mina (fin del juego)
// Retorna 0 en cualquier otro caso
int revelacionRecursiva(int fil, int col) {

    // Validación de límites del tablero
    if (fil < 0 || fil >= FILAS || col < 0 || col >= COLUMNAS)
        return 0;

    // Si la celda ya fue revelada, no se procesa de nuevo
    if (tablerodeJuego[fil][col] == 1){
        return 0;
    }

    // Si se selecciona una mina, se pierde el juego
    if (tableroPrincipal[fil][col] == 9){
        return 1;
    }

    // Se revela la celda actual
    tablerodeJuego[fil][col] = 1;

    // Si la celda tiene un número (>0), no se expande
    if (tableroPrincipal[fil][col] > 0) {
        return 0;
    }

    // Si la celda es cero, se revelan recursivamente las vecinas
    for (int adyacenteFila = -1; adyacenteFila <= 1; adyacenteFila++) {
        for (int adyacenteColumna = -1; adyacenteColumna<= 1; adyacenteColumna++) {

            // Evita volver a llamar a la misma celda
            if (adyacenteFila == 0 && adyacenteColumna == 0){
                continue;
            }

            // Propagación de error por seguridad (no debería ocurrir)
            if (revelacionRecursiva(fil + adyacenteFila, col + adyacenteColumna) == 1){
                return 1;
            }
        }
    }
    return 0;
}

// Verifica si el jugador ganó
// Condición de victoria:
// todas las celdas que NO son minas deben estar reveladas
int verificarVictoria() {
    for (int i = 0; i < FILAS; i++) {
        for (int j = 0; j < COLUMNAS; j++) {

            // Si existe alguna celda que:
            // - no es mina
            // - y aún no ha sido revelada
            // entonces el juego no se ha ganado todavía
            if (tableroPrincipal[i][j] != 9 &&
                tablerodeJuego[i][j] == 0) {
                return 0;
            }
        }
    }
    return 1;
}

// Coloca una bandera en una celda no revelada
void ponerBandera(int fil, int col) {

    // Validación de límites del tablero
    if (fil < 0 || fil >= FILAS || col < 0 || col >= COLUMNAS) {
        // Fuera del tablero: no hace nada
    } else {
        // Solo se puede poner bandera si la celda no está revelada
        if(tablerodeJuego[fil][col] != 1) {
            tablerodeJuego[fil][col]=3;
        }
    }
}

// Imprime el tablero según el modo seleccionado
// opcion 1: tablero completo (debug / fin de juego)
// opcion 2: tablero visible para el jugador
void imprimirTablero(int opcion) {

    if(opcion == 1){
        for(int i = 0; i < FILAS; i++){
            for(int j = 0; j < COLUMNAS; j++){
                if(tableroPrincipal[i][j] == 9){
                    printf("* ");
                }else{
                    printf("%d ", tableroPrincipal[i][j]);
                }
            }
            printf("\n");
        }
    }

    if(opcion == 2){
        for(int i = 0; i < FILAS; i++){
            for(int j = 0; j < COLUMNAS; j++){
                if(tablerodeJuego[i][j] == 1){
                    printf("%d ", tableroPrincipal[i][j]);
                }
                else if(tablerodeJuego[i][j] == 3){
                    printf("? ");
                }
                else{
                    printf(". ");
                }
            }
            printf("\n");
        }
    }
}

int main() {
    int opcion=0;
    int gameState=0;
    int winner=0;
    int salir=0;
    int bandera=0;
    int col, fil;

    while(salir!=1) {
        printf("Buscaminas en C, presiona 1 para jugar: \n");
        scanf("%d",&opcion);

        if(opcion==1) {
            gameState=0;
            winner=0;

            iniciarTableros();
            colocarMinas();
            ponerNumerosAbyacentes();

            while(gameState!=1) {
                printf("_________________\n");
                imprimirTablero(2);
                printf("\n________________ \n");

                printf("Selecciona Fila : ");
                scanf("%d",&fil);

                printf("Selecciona columna: ");
                scanf("%d",&col);

                do {
                    printf("Ingresa 1 para revelar o 2 para poner bandera: ");
                    scanf("%d",&bandera);

                    if(bandera==1) {
                        gameState = revelacionRecursiva(fil,col);
                        winner=verificarVictoria();

                        if(gameState == 1) {
                            printf("!!Pisaste una mina!!. Juego terminado.\n");
                            imprimirTablero(1);
                            continue;
                        }

                        if(winner==1) {
                            printf("Ganaste el Juego.\n");
                            imprimirTablero(1);
                            gameState=1;
                        }
                    }

                    if(bandera==2){
                        ponerBandera(fil,col);
                    }

                }while(bandera>2 || bandera<0);
            }
        } else {
            printf("Ingresa una opcion correcta.\n");
        }
    }
    return 0;
}

"""Caso 7 - Academia: registro de notas y rendimiento.

Programa de consola para Fundamentos de Programacion 1.
Incluye los datos de prueba oficiales y permite registrar mas alumnos.
"""

import sys


# R1: constante del dominio y calculo secuencial.
BONO = 0.05

# R9: cinco arreglos paralelos.
codigos = []
nombres = []
puntajes_base = []
puntajes_ponderados = []
asistencias = []

# R10: matriz; cada fila es un alumno y cada columna una evaluacion.
notas = []


# R13: normalizacion de cadenas.
def normalizar_nombre(nombre):
    """Quita espacios repetidos y aplica mayuscula inicial a cada palabra."""
    return " ".join(nombre.strip().split()).title()


# R13: validacion caracter por caracter, sin expresiones regulares.
def codigo_valido(codigo):
    """Valida una letra seguida de cuatro digitos, por ejemplo A2201."""
    if len(codigo) != 5:
        return False
    if not codigo[0].isalpha():
        return False
    for posicion in range(1, 5):
        if not codigo[posicion].isdigit():
            return False
    return True


# R1 y R2: formula encapsulada en un metodo con parametro y retorno.
def calcular_puntaje_ponderado(puntaje_base):
    """Aplica el bono de asistencia del dominio."""
    return puntaje_base * (1 + BONO)


# R3: selectiva anidada; se evalua primero el umbral mayor.
def clasificar_rendimiento(puntaje_acumulado):
    if puntaje_acumulado > 48:
        return "Alto"
    elif puntaje_acumulado > 36:
        return "Medio"
    else:
        return "Bajo"


def agregar_alumno(codigo, nombre, puntaje_base, asistencia, fila_notas):
    """Agrega un registro manteniendo alineados los arreglos y la matriz."""
    codigo = codigo.strip().upper()
    if not codigo_valido(codigo) or codigo in codigos:
        return False
    codigos.append(codigo)
    nombres.append(normalizar_nombre(nombre))
    puntajes_base.append(float(puntaje_base))
    puntajes_ponderados.append(calcular_puntaje_ponderado(float(puntaje_base)))
    asistencias.append(int(asistencia))
    notas.append([float(nota) for nota in fila_notas])
    return True


def cargar_datos_prueba():
    """Carga una sola vez los tres registros oficiales del caso."""
    if codigos:
        return
    agregar_alumno("A2201", "  sofia   RAMOS vega ", 17, 18, [18, 17, 16])
    agregar_alumno("A2202", "diego HUAMAN", 11, 9, [12, 11, 10])
    agregar_alumno("A2203", "lucia flores", 14, 15, [14, 15, 13])


# R6: ciclo mientras con centinela y validacion.
def registrar_alumnos():
    print("\nREGISTRO DE ALUMNOS (0 para terminar)")
    codigo = input("Codigo: ").strip().upper()
    while codigo != "0":
        while not codigo_valido(codigo) or codigo in codigos:
            print("Codigo invalido o repetido. Use una letra y cuatro digitos.")
            codigo = input("Codigo (0 para terminar): ").strip().upper()
            if codigo == "0":
                return
        nombre = input("Apellidos y nombres: ")
        base = float(input("Puntaje base: "))
        asistencia = int(input("Asistencias: "))
        fila_notas = []
        for evaluacion in range(3):
            fila_notas.append(float(input(f"Nota de evaluacion {evaluacion + 1}: ")))
        agregar_alumno(codigo, nombre, base, asistencia, fila_notas)
        print("Alumno registrado.")
        codigo = input("Codigo (0 para terminar): ").strip().upper()


# R7: for con acumulador y contador condicionado en la misma pasada.
def obtener_resumen_listado():
    acumulador_ponderado = 0.0
    contador_menos_12 = 0
    filas = []
    for i in range(len(codigos)):
        acumulador_ponderado += puntajes_ponderados[i]
        if asistencias[i] < 12:
            contador_menos_12 += 1
        total_notas = sum(notas[i])
        filas.append((codigos[i], nombres[i], puntajes_base[i],
                      puntajes_ponderados[i], asistencias[i], total_notas,
                      clasificar_rendimiento(total_notas)))
    promedio = acumulador_ponderado / len(codigos) if codigos else 0.0
    return filas, promedio, contador_menos_12


def listar_notas():
    filas, promedio, contador = obtener_resumen_listado()
    print("\nLISTADO DE NOTAS")
    for fila in filas:
        print(f"{fila[0]} | {fila[1]:18} | base {fila[2]:.2f} | "
              f"ponderado {fila[3]:.2f} | asist. {fila[4]} | "
              f"acumulado {fila[5]:.2f} | {fila[6]}")
    print(f"Puntaje ponderado promedio del grupo: {promedio:.2f}")
    print(f"Alumnos con menos de 12 asistencias: {contador}")
    return promedio, contador


# R8: bucles anidados para totales por fila, columna y total general.
def calcular_consolidado(matriz):
    if not matriz:
        return [], [], 0.0
    totales_alumno = []
    for fila in range(len(matriz)):
        total_fila = 0.0
        for columna in range(len(matriz[fila])):
            total_fila += matriz[fila][columna]
        totales_alumno.append(total_fila)

    totales_evaluacion = []
    for columna in range(len(matriz[0])):
        total_columna = 0.0
        for fila in range(len(matriz)):
            total_columna += matriz[fila][columna]
        totales_evaluacion.append(total_columna)

    total_general = sum(totales_alumno)
    return totales_alumno, totales_evaluacion, total_general


def mostrar_consolidado():
    por_alumno, por_evaluacion, general = calcular_consolidado(notas)
    print("\nCONSOLIDADO DE EVALUACIONES")
    for i in range(len(codigos)):
        print(f"{codigos[i]} {nombres[i]}: {por_alumno[i]:.2f}")
    for j in range(len(por_evaluacion)):
        print(f"Evaluacion {j + 1}: {por_evaluacion[j]:.2f}")
    print(f"Total general: {general:.2f}")
    print(f"Comprobacion por columnas: {sum(por_evaluacion):.2f}")
    return por_alumno, por_evaluacion, general


# R11: burbuja descendente, moviendo codigo, nombre y total juntos.
def ordenar_ranking_burbuja(codigos_origen, nombres_origen, totales_origen):
    codigos_ranking = codigos_origen.copy()
    nombres_ranking = nombres_origen.copy()
    totales_ranking = totales_origen.copy()
    for limite in range(len(totales_ranking) - 1, 0, -1):
        for i in range(limite):
            if totales_ranking[i] < totales_ranking[i + 1]:
                totales_ranking[i], totales_ranking[i + 1] = (
                    totales_ranking[i + 1], totales_ranking[i])
                codigos_ranking[i], codigos_ranking[i + 1] = (
                    codigos_ranking[i + 1], codigos_ranking[i])
                nombres_ranking[i], nombres_ranking[i + 1] = (
                    nombres_ranking[i + 1], nombres_ranking[i])
    return codigos_ranking, nombres_ranking, totales_ranking


def mostrar_ranking():
    totales, _, _ = calcular_consolidado(notas)
    cod_rank, nom_rank, tot_rank = ordenar_ranking_burbuja(
        codigos, nombres, totales)
    print("\nRANKING DE RENDIMIENTO")
    for i in range(len(cod_rank)):
        nivel = clasificar_rendimiento(tot_rank[i])
        print(f"{i + 1}. {cod_rank[i]} | {nom_rank[i]} | "
              f"{tot_rank[i]:.2f} | {nivel}")
    return cod_rank, nom_rank, tot_rank


# R12: busqueda secuencial con conteo de comparaciones.
def busqueda_secuencial(arreglo_codigos, buscado):
    comparaciones = 0
    for i in range(len(arreglo_codigos)):
        comparaciones += 1
        if arreglo_codigos[i] == buscado:
            return i, comparaciones
    return -1, comparaciones


# R12: busqueda binaria sobre un arreglo ascendente.
def busqueda_binaria(arreglo_ordenado, buscado):
    izquierda = 0
    derecha = len(arreglo_ordenado) - 1
    comparaciones = 0
    while izquierda <= derecha:
        centro = (izquierda + derecha) // 2
        comparaciones += 1
        if arreglo_ordenado[centro] == buscado:
            return centro, comparaciones
        elif buscado < arreglo_ordenado[centro]:
            derecha = centro - 1
        else:
            izquierda = centro + 1
    return -1, comparaciones


def buscar_alumno(codigo_buscado=None):
    if codigo_buscado is None:
        codigo_buscado = input("Codigo a buscar: ").strip().upper()
    else:
        codigo_buscado = codigo_buscado.strip().upper()

    posicion_sec, comp_sec = busqueda_secuencial(codigos, codigo_buscado)
    codigos_ordenados = codigos.copy()
    codigos_ordenados.sort()
    posicion_bin, comp_bin = busqueda_binaria(codigos_ordenados, codigo_buscado)

    print("\nBUSQUEDA")
    if posicion_sec >= 0:
        print(f"Secuencial: {codigo_buscado} en posicion {posicion_sec + 1}; "
              f"comparaciones: {comp_sec}")
        print(f"Binaria: {codigo_buscado} en posicion ordenada {posicion_bin + 1}; "
              f"comparaciones: {comp_bin}")
    else:
        print(f"{codigo_buscado} no encontrado.")
        print(f"Comparaciones: secuencial {comp_sec}, binaria {comp_bin}")
    return posicion_sec, comp_sec, posicion_bin, comp_bin


def ejecutar_demo():
    """Ejecuta y muestra la prueba completa solicitada para A2201-A2203."""
    cargar_datos_prueba()
    listar_notas()
    mostrar_consolidado()
    mostrar_ranking()
    buscar_alumno("A2202")


# R4 y R5: match sobre menu y repeticion hasta elegir 6.
def programa_principal():
    cargar_datos_prueba()
    while True:
        print("\nACADEMIA - NOTAS Y RENDIMIENTO")
        print("1. Registrar alumno")
        print("2. Listar notas")
        print("3. Consolidado de evaluaciones")
        print("4. Ranking de rendimiento")
        print("5. Buscar alumno")
        print("6. Salir")
        opcion = input("Opcion: ").strip()

        match opcion:
            case "1":
                registrar_alumnos()
            case "2":
                listar_notas()
            case "3":
                mostrar_consolidado()
            case "4":
                mostrar_ranking()
            case "5":
                buscar_alumno()
            case "6":
                print("Programa finalizado.")
                break
            case _:
                print("Opcion inexistente.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        ejecutar_demo()
    else:
        programa_principal()

import statistics
import itertools

#Listas de Participantes, equipos y partidas
participantes = []
equipos = []
partidas = []

# Funciones de validación
def validar_nombre(nombre):
    return len(nombre.strip()) > 0

def validar_edad(edad):
    try:
        edad_int = int(edad)
        return 12 <= edad_int <= 70
    except ValueError:
        return False

def validar_nivel(nivel):
    try:
        nivel_int = int(nivel)
        return 1 <= nivel_int <= 5
    except ValueError:
        return False

#Registro de participantes
def registrar_participante():
    """
    Solicita y valida los datos de un nuevo participante.
    Agrega el participante a la lista global 'participantes'.
    """
    print("\n" + "="*40)
    print("   REGISTRO DE NUEVO PARTICIPANTE")
    print("="*40)

    # Validar Nombre
    while True:
        nombre = input("Ingresa tu nombre: ").strip()
        if validar_nombre(nombre):
            break
        print(" El nombre no puede estar vacío. Intenta de nuevo.")

    # Validar Edad
    while True:
        edad_input = input("Ingresa tu edad (12-70): ")
        if validar_edad(edad_input):
            edad = int(edad_input)
            break
        print(" La edad debe ser un número entre 12 y 70. Intenta de nuevo.")

    # Validar Nivel
    while True:
        nivel_input = input("Ingresa tu nivel de experiencia (1-5): ")
        if validar_nivel(nivel_input):
            nivel = int(nivel_input)
            break
        print(" El nivel debe ser un número entre 1 y 5. Intenta de nuevo.")

    nuevo_participante = {
        "nombre": nombre,
        "edad": edad,
        "nivel": nivel
    }

    participantes.append(nuevo_participante)
    print(f"\n ¡{nombre} registrado/a exitosamente!")
    return nuevo_participante


def registrar_multiples_participantes():
    """Permite registrar varios participantes en secuencia."""
    print("\n  BIENVENIDO AL TORNEO PIXELES RETRO")
    while True:
        registrar_participante()
        continuar = input("\n¿Registrar otro participante? (s/n): ").strip().lower()
        if continuar != 's':
            break
    print(f"\n Se registraron {len(participantes)} participante(s) en total.")

#Registro de Equipos
def jugador_ya_en_equipo(nombre_jugador): #Busca si un jugador ya está en algún equipo
    for equipo in equipos:
        if nombre_jugador in equipo["jugadores"]:
            return True
    return False

def nombre_equipo_existe(nombre_equipo): #Busca si un nombre de equipo ya existe
    
    for equipo in equipos:
        if equipo["nombre"].lower() == nombre_equipo.lower():
            return True
    return False


def mostrar_participantes_disponibles(): #Muestra los participantes que aún no están en ningún equipo
    return [p for p in participantes if not jugador_ya_en_equipo(p["nombre"])]

def formar_equipo(): #Elige 2 jugadores disponibles para formar un equipo
    disponibles = mostrar_participantes_disponibles()

    if len(disponibles) < 2:
        print("No hay suficientes jugadores disponibles para formar un equipo.")
        return None

    print("\n" + "="*40)
    print("       FORMACIÓN DE EQUIPO")
    print("="*40)
    print("Jugadores disponibles:")
    for i, p in enumerate(disponibles):
        print(f"  [{i+1}] {p['nombre']} — Edad: {p['edad']}, Nivel: {p['nivel']}")

    # Selecciona el primer jugador del equipo
    while True:
        try:
            idx1 = int(input("\nElige el número del Jugador 1: ")) - 1
            if 0 <= idx1 < len(disponibles):
                break
            print("Número fuera de rango.")
        except ValueError:
            print("Ingresa un número válido.")
    # Selecciona el segundo jugador del equipo
    while True:
        try:
            idx2 = int(input("Elige el número del Jugador 2: ")) - 1
            if 0 <= idx2 < len(disponibles) and idx2 != idx1:
                break
            print(" Elige un jugador diferente al primero.")
        except ValueError:
            print(" Ingresa un número válido.")

    jugador1 = disponibles[idx1]["nombre"]
    jugador2 = disponibles[idx2]["nombre"]

    # Elegir nombre único para el equipo
    while True:
        nombre_equipo = input("Ingresa el nombre del equipo: ").strip()
        if not nombre_equipo:
            print(" El nombre no puede estar vacío.")
        elif nombre_equipo_existe(nombre_equipo):
            print(" Ya existe un equipo con ese nombre. Elige otro.")
        else:
            break

    nuevo_equipo = {
        "nombre": nombre_equipo,
        "jugadores": [jugador1, jugador2],
        "puntos": 0,
        "partidas_jugadas": 0,
        "victorias": 0
    }

    equipos.append(nuevo_equipo)
    print(f"\n Equipo '{nombre_equipo}' formado con {jugador1} y {jugador2}")
    return nuevo_equipo

def formar_multiples_equipos():
    """Repite la formación de equipos mientras haya jugadores disponibles."""
    while len(mostrar_participantes_disponibles()) >= 2:
        formar_equipo()
        disponibles = mostrar_participantes_disponibles()
        if len(disponibles) >= 2:
            continuar = input("\n Quieres formar otro equipo? (s/n):").strip().lower()
            if continuar != 's':
                break
        else:
            print("\nNo quedan más jugadores disponibles para formar equipos.")
            break
    print(f"\n✅ Se formaron {len(equipos)} equipo(s) en total.")

#Registro de Partidas
def registrar_partida():
    """
    Registra el resultado de una partida entre dos equipos.
    Asigna 3 puntos al equipo ganador.
    """
    if len(equipos) < 2:
        print(" Necesitas al menos 2 equipos para registrar una partida.")
        return

    print("\n" + "="*40)
    print("       REGISTRO DE PARTIDA")
    print("="*40)
    print("Equipos disponibles:")
    for i, eq in enumerate(equipos):
        print(f"  [{i+1}] {eq['nombre']} (Puntos: {eq['puntos']})")

    # Elegir equipo 1
    while True:
        try:
            idx1 = int(input("\nElige el número del Equipo 1: ")) - 1
            if 0 <= idx1 < len(equipos):
                break
            print(" Número fuera de rango.")
        except ValueError:
            print(" Ingresa un número válido.")

    # Elegir equipo 2
    while True:
        try:
            idx2 = int(input("Elige el número del Equipo 2: ")) - 1
            if 0 <= idx2 < len(equipos) and idx2 != idx1:
                break
            print(" Elige un equipo diferente al primero.")
        except ValueError:
            print(" Ingresa un número válido.")

    equipo1 = equipos[idx1]
    equipo2 = equipos[idx2]

    print(f"\n¿Quién ganó? [1] {equipo1['nombre']}  [2] {equipo2['nombre']}")
    while True:
        try:
            resultado = int(input("Elige el ganador (1 o 2): "))
            if resultado in [1, 2]:
                break
            print(" Elige 1 o 2.")
        except ValueError:
            print(" Ingresa 1 o 2.")

    ganador = equipo1 if resultado == 1 else equipo2
    perdedor = equipo2 if resultado == 1 else equipo1

    ganador["puntos"] += 3
    ganador["victorias"] += 1
    ganador["partidas_jugadas"] += 1
    perdedor["partidas_jugadas"] += 1

    partida = {
        "equipo1": equipo1["nombre"],
        "equipo2": equipo2["nombre"],
        "ganador": ganador["nombre"],
        "puntos_otorgados": 3
    }
    partidas.append(partida)

    print(f"\n ¡{ganador['nombre']} ganó la partida y obtuvo 3 puntos!")
    return partida


def registrar_multiples_partidas():
    """Permite registrar varias partidas en secuencia."""
    while True:
        registrar_partida()
        continuar = input("\n¿Registrar otra partida? (s/n): ").strip().lower()
        if continuar != 's':
            break
    print(f"\n Se registraron {len(partidas)} partida(s) en total.")


def calcular_rendimiento(equipo):
    """Calcula el porcentaje de victorias de un equipo."""
    if equipo["partidas_jugadas"] == 0:
        return 0.0
    return (equipo["victorias"] / equipo["partidas_jugadas"]) * 100


def calcular_estadisticas():
    """Usa el módulo statistics para calcular métricas de puntos."""
    if not equipos:
        return None
    lista_puntos = [eq["puntos"] for eq in equipos]
    return {
        "promedio": statistics.mean(lista_puntos),
        "maximo": max(lista_puntos),
        "minimo": min(lista_puntos)
    }

#Reportes de resultados
def reporte_participantes():
    """Muestra la lista completa de participantes registrados."""
    print("\n" + "="*50)
    print("        LISTA DE PARTICIPANTES REGISTRADOS")
    print("="*50)

    if not participantes:
        print("  No hay participantes registrados.")
        return

    print(f"  {'N°':<4} {'Nombre':<20} {'Edad':<8} {'Nivel':<8}")
    print("  " + "-"*44)

    for i, p in enumerate(participantes, start=1):
        print(f"  {i:<4} {p['nombre']:<20} {p['edad']:<8} {'⭐' * p['nivel']:<8}")

    print(f"\n  Total de participantes: {len(participantes)}")


def reporte_equipos():
    """Muestra los equipos formados con sus integrantes."""
    print("\n" + "="*50)
    print("           EQUIPOS FORMADOS")
    print("="*50)

    if not equipos:
        print("  No hay equipos formados.")
        return

    for i, eq in enumerate(equipos, start=1):
        print(f"\n  Equipo {i}: {eq['nombre']}")
        print(f"     Jugador 1: {eq['jugadores'][0]}")
        print(f"     Jugador 2: {eq['jugadores'][1]}")
        print(f"     Puntos: {eq['puntos']}")
        print(f"     Partidas jugadas: {eq['partidas_jugadas']}")
        print(f"     Victorias: {eq['victorias']}")


def reporte_ranking():
    """Muestra el ranking de equipos ordenado por puntos de mayor a menor."""
    print("\n" + "="*50)
    print("           RANKING DE EQUIPOS")
    print("="*50)

    if not equipos:
        print("  No hay equipos para mostrar.")
        return

    ranking = sorted(equipos, key=lambda eq: eq["puntos"], reverse=True)

    print(f"  {'Pos':<5} {'Equipo':<20} {'Puntos':<10} {'Victorias':<12} {'Rendimiento':<12}")
    print("  " + "-"*55)

    medallas = ["Oro", "Plata", "Bronce"]
    for i, eq in enumerate(ranking, start=1):
        medalla = medallas[i-1] if i <= 3 else "  "
        rendimiento = calcular_rendimiento(eq)
        print(f"  {medalla} {i:<3} {eq['nombre']:<20} {eq['puntos']:<10} {eq['victorias']:<12} {rendimiento:.1f}%")


def reporte_historial_partidas():
    """Muestra el historial completo de partidas jugadas."""
    print("\n" + "="*50)
    print("          HISTORIAL DE PARTIDAS")
    print("="*50)

    if not partidas:
        print("  No se han jugado partidas aún.")
        return

    for i, p in enumerate(partidas, start=1):
        print(f"  Partida {i}: {p['equipo1']} vs {p['equipo2']}")
        print(f"  Ganador: {p['ganador']} (+{p['puntos_otorgados']} puntos)")
        print()


def reporte_estadisticas_generales():
    """Muestra estadísticas generales del torneo usando el módulo statistics."""
    print("\n" + "="*50)
    print("       ESTADÍSTICAS GENERALES DEL TORNEO")
    print("="*50)

    stats = calcular_estadisticas()
    if not stats:
        print("  No hay datos suficientes para estadísticas.")
        return

    print(f"   Promedio de puntos por equipo : {stats['promedio']:.2f}")
    print(f"   Puntaje máximo                : {stats['maximo']}")
    print(f"   Puntaje mínimo                : {stats['minimo']}")
    print(f"   Total de partidas jugadas     : {len(partidas)}")
    print(f"   Total de participantes        : {len(participantes)}")
    print(f"   Total de equipos              : {len(equipos)}")


def reporte_completo():
    """Ejecuta todos los reportes en secuencia."""
    print("\n" + "#"*55)
    print("#" + " "*18 + "REPORTE FINAL DEL TORNEO" + " "*11 + "#")
    print("#"*55)

    reporte_participantes()
    reporte_equipos()
    reporte_ranking()
    reporte_historial_partidas()
    reporte_estadisticas_generales()

    print("\n" + "="*50)
    print("  🕹️  ¡Gracias por participar en Pixeles Retro!  🕹️")
    print("="*50)


# =============================================================
# PARTE 7 — MENÚ PRINCIPAL
# =============================================================

def menu_principal():
    """
    Menú principal del sistema de gestión del torneo.
    Agrupa todas las funcionalidades en opciones numeradas.
    """
    while True:
        print("\n" + "="*45)
        print("   " \
        "" \
        "  TORNEO PIXELES RETRO — MENÚ PRINCIPAL")
        print("="*45)
        print("  [1] Registrar participante")
        print("  [2] Formar equipo")
        print("  [3] Registrar partida")
        print("  [4] Ver lista de participantes")
        print("  [5] Ver equipos formados")
        print("  [6] Ver ranking de equipos")
        print("  [7] Ver historial de partidas")
        print("  [8] Ver estadísticas generales")
        print("  [9] Reporte completo")
        print("  [0] Salir")
        print("-"*45)

        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            registrar_participante()
        elif opcion == "2":
            formar_equipo()
        elif opcion == "3":
            registrar_partida()
        elif opcion == "4":
            reporte_participantes()
        elif opcion == "5":
            reporte_equipos()
        elif opcion == "6":
            reporte_ranking()
        elif opcion == "7":
            reporte_historial_partidas()
        elif opcion == "8":
            reporte_estadisticas_generales()
        elif opcion == "9":
            reporte_completo()
        elif opcion == "0":
            print("\n ¡Hasta la próxima partida! Game Over... for now.")
            break
        else:
            print(" Opción inválida. Elige un número entre 0 y 9.")

#Entrada al menu de sistema de registro de torneo
if __name__ == "__main__":
    menu_principal()

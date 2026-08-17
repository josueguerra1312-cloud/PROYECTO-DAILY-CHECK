from flights import load_flights, filter_gdl_flights, build_sequences
from overnight import calculate_overnight_windows
from dailycheck import load_tasks, assign_tasks
from exporter import export_daily_check

VUELOS_FILE = "VUELOS.xlsx"
PERNOCTA_FILE = "PERNOCTAGDL.xlsx"
OUTPUT_FILE = "DAILY_CHECK_GDL.xlsx"

def main():
    vuelos = load_flights(VUELOS_FILE)
    vuelos_gdl = filter_gdl_flights(vuelos)
    secuencias = build_sequences(vuelos_gdl)
    ventanas = calculate_overnight_windows(secuencias)
    tareas = load_tasks(PERNOCTA_FILE)
    resultado = assign_tasks(ventanas, tareas)
    export_daily_check(resultado, OUTPUT_FILE)
    print("DAILY CHECK GENERADO")

if __name__ == '__main__':
    main()

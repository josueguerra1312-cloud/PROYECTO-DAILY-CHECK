# GDL Pernocta Scheduler

Aplicación en Python para generar y ordenar las ventanas de pernocta y tránsito de aeronaves en Guadalajara (`GDL`) a partir de un archivo Excel de vuelos.

El proyecto reproduce la intención de la macro original y mejora sus puntos frágiles:

- Agrupa movimientos por matrícula.
- Normaliza matrículas como `XAVSC` a `XA-VSC`.
- Construye fechas y horas completas.
- Corrige automáticamente vuelos que cruzan medianoche.
- Por cada llegada a GDL busca la primera salida posterior desde GDL de la misma matrícula.
- Clasifica ventanas menores de 3 horas como `TRANSIT CHECK`.
- Conserva el criterio original: una ventana exactamente de 3 horas es `PERNOCTA`.
- Ordena la noche como una línea continua de 18:00 a 06:00.
- Conserva el orden de grupos del macro: tránsito antes de medianoche, pernoctas, tránsito después de medianoche y casos especiales.
- Puede generar resultados en Excel o CSV.

## Requisitos

- Python 3.10 o superior.
- Archivo `.xlsx` o `.xlsm` con una hoja llamada `VUELOS`.
- Encabezados requeridos:
  - `LEG DEPT DATE`
  - `AC REG NUMBER`
  - `FLT NUM`
  - `DEP`
  - `STD LT`
  - `STA LT`
  - `DST`

## Instalación

```bash
git clone <URL-DE-TU-REPOSITORIO>
cd gdl-pernocta-scheduler
python -m venv .venv
```

Activación en Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Activación en macOS o Linux:

```bash
source .venv/bin/activate
```

Instala el proyecto:

```bash
python -m pip install -e .
```

Para desarrollo y pruebas:

```bash
python -m pip install -e ".[dev]"
```

## Uso básico

```bash
gdl-pernocta "DAILY CHECK STA GDL MMM DD YEAR - Copy.xlsm" --output SecuenciaGDL.xlsx
```

El comando lee la hoja `VUELOS` y crea `SecuenciaGDL.xlsx`.

## Ejemplos

Incluir aeronaves sin una salida posterior identificada:

```bash
gdl-pernocta vuelos.xlsm --include-spares
```

Cambiar el umbral de tránsito a 2.5 horas:

```bash
gdl-pernocta vuelos.xlsm --transit-hours 2.5
```

Generar CSV:

```bash
gdl-pernocta vuelos.xlsm --output SecuenciaGDL.csv
```

Usar otra estación o ventana nocturna:

```bash
gdl-pernocta vuelos.xlsm --station GDL --night-start 18:00 --night-end 06:00
```

## Salida

La salida contiene:

- `A/C`: matrícula normalizada.
- `FL ARR`: vuelo que llega a GDL.
- `FECHA ARR` y `ARR`: fecha y hora real de llegada.
- `FL DEPT`: siguiente vuelo que sale desde GDL.
- `FECHA DEPT` y `DEPT`: fecha y hora real de salida.
- `TIEMPO TIERRA`: ventana total disponible.
- `TIPO`: `TRANSIT CHECK`, `PERNOCTA`, `SPARE` o `REVISAR`.
- `OBSERVACION`: explicación de casos especiales.

## Reglas de negocio

1. Solo se procesan movimientos relacionados con GDL.
2. Cada llegada a GDL se enlaza con la primera salida posterior desde GDL de la misma matrícula.
3. Se conservan llegadas dentro de 18:00–06:00, igual que la lógica original.
4. Menos de 3 horas en tierra es `TRANSIT CHECK`.
5. Tres horas o más es `PERNOCTA`.
6. El orden final es:
   1. Tránsitos con llegada de 18:00 a 23:59.
   2. Pernoctas.
   3. Tránsitos con llegada de 00:00 a 06:00.
   4. Casos especiales.

## Pruebas

```bash
pytest -q
```

Las pruebas cubren:

- Cruce de medianoche.
- Ventanas menores a tres horas.
- Límite exacto de tres horas.
- Búsqueda de la primera salida posterior, aunque haya filas intermedias.
- Orden original por grupos.

## Estructura

```text
gdl-pernocta-scheduler/
├── .gitignore
├── pyproject.toml
├── README.md
├── examples/
│   └── vuelos_ejemplo.csv
├── src/gdl_pernocta/
│   ├── __init__.py
│   ├── cli.py
│   ├── io_excel.py
│   ├── models.py
│   ├── normalization.py
│   └── scheduler.py
└── tests/
    └── test_scheduler.py
```

## Publicación inicial en GitHub

```bash
git init
git add .
git commit -m "Initial GDL overnight scheduler"
git branch -M main
git remote add origin <URL-DE-TU-REPOSITORIO>
git push -u origin main
```

## Seguridad de datos

No subas archivos operacionales reales al repositorio. El `.gitignore` excluye archivos Excel y CSV, salvo el CSV ficticio dentro de `examples/`.

## Licencia

El repositorio no incluye una licencia por defecto. Antes de hacerlo público, define con tu organización si el código será privado o qué licencia puede utilizarse.

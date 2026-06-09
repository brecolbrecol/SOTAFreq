1. Generar el fichero csv con formato similar al de `inscritos_*.csv`

2. Ejecutar: `uv run lib/Summit.py -i inscritos_$(date +%Y).csv`, o si no está instalado `uv`: `python lib/Summit.py -i inscritos_2024v2.csv`

Opcionalmente, se pueden definir las frecuencias previamente o ajustarlas en lib/FrequenciesAssign.py

3. Despliegue: `npx wrangler pages deploy ./www --project-name=vhf-fm-sota`

Previamente se debe haber iniciado sesion con `npm wrangler login`


```venv/bin/python3 lib/Summit.py -i inscritos_2025.csv && npx wrangler pages deploy ./www --project-name=vhf-fm-sota```

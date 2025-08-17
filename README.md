# Land Usage Dash App

Interactive web app to analize land usage across different types of food.

## Despliegue en Render

### Opción 1: Usando Render Blueprint (render.yaml)

1. Fork o clona este repositorio
2. Conecta tu repositorio de GitHub a Render
3. Crea un nuevo "Blueprint" en Render
4. Render detectará automáticamente el archivo `render.yaml` y configurará el servicio

### Opción 2: Configuración manual

1. Crea un nuevo "Web Service" en Render
2. Conecta tu repositorio de GitHub
3. Configura las siguientes opciones:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn land_usage_dash_app:server --bind 0.0.0.0:$PORT`
   - **Python Version**: 3.11.0 (opcional)

## Estructura de archivos

```
Visualización/
├── land_usage_dash_app.py
├── requirements.txt
├── render.yaml
├── README.md
└── data/
    └── land-use-kcal-poore.csv
```

## Variables de entorno

El app está configurado para usar la variable de entorno `PORT` automáticamente, que Render proporciona por defecto.

## Desarrollo local

Para ejecutar localmente:

```bash
pip install -r requirements.txt
python land_usage_dash_app.py
```

La aplicación estará disponible en `http://localhost:8051`

## Datos

Los datos provienen del estudio de Poore & Nemecek (2018) sobre el impacto ambiental de los sistemas alimentarios.

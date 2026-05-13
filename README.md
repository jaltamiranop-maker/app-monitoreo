# Kingspan Optimizer — React + FastAPI

Este proyecto reemplaza la interfaz Streamlit por un frontend **React** moderno,
manteniendo el backend **FastAPI** y la lógica de optimización intactos.

---

## Estructura de archivos

```
backend/
  main.py            ← API FastAPI (nuevo, con CORS y endpoints adicionales)
  optimizer.py       ← Algoritmo de optimización (sin cambios)
  database.py        ← Base de datos SQLite (sin cambios)
  pdf_generator.py   ← Generación de PDF extraída a módulo propio

frontend/
  App.jsx            ← Componente React principal (toda la UI)
```

---

## 1. Backend (Python / FastAPI)

### Instalar dependencias

```bash
pip install fastapi uvicorn reportlab pandas
```

### Copiar archivos al mismo directorio

Coloca en la misma carpeta:
- `main.py`
- `pdf_generator.py`
- `optimizer.py` (sin cambios, el tuyo original)
- `database.py` (sin cambios, el tuyo original)

### Ejecutar

```bash
uvicorn main:app --reload --port 8000
```

La API queda disponible en `http://127.0.0.1:8000`.
Puedes explorar los endpoints en `http://127.0.0.1:8000/docs`.

---

## 2. Frontend (React)

Puedes usar el frontend de dos maneras:

### Opción A — Pegar en Claude.ai como Artifact
Sube `App.jsx` directamente como un artefacto React en Claude.ai.

### Opción B — Proyecto Create React App / Vite

```bash
# Con Vite (recomendado)
npm create vite@latest kingspan-optimizer -- --template react
cd kingspan-optimizer
cp /ruta/de/App.jsx src/App.jsx
npm install
npm run dev
```

El frontend se conecta automáticamente a `http://127.0.0.1:8000`.
Si cambias el puerto del backend, actualiza la constante `API_BASE` al inicio de `App.jsx`.

---

## Endpoints de la API

| Método | Ruta                        | Descripción                                  |
|--------|-----------------------------|----------------------------------------------|
| GET    | `/siguiente_orden`          | Próximo número de orden disponible           |
| POST   | `/optimizar`                | Ejecuta el algoritmo de optimización         |
| POST   | `/guardar_pedido`           | Guarda la orden en SQLite                    |
| POST   | `/generar_pdf`              | Genera y descarga el PDF de la orden         |
| GET    | `/historial`                | Lista todas las órdenes guardadas            |
| POST   | `/regenerar_pdf/{id}`       | Regenera el PDF de una orden existente       |

---

## Notas

- El backend usa **CORS abierto** (`allow_origins=["*"]`). En producción reemplaza
  `"*"` con la URL exacta del frontend.
- La base de datos `kingspan_pedidos.db` se crea automáticamente en el directorio
  donde ejecutes `uvicorn`.
- El logo de Kingspan se puede agregar al frontend editando el `<header>` en `App.jsx`.

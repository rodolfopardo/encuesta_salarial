# 🚀 Guía de Inicio Rápido

## Para ejecutar el Dashboard en 3 pasos:

### 1️⃣ Abre la Terminal

En Mac:
- Presiona `Cmd + Espacio`
- Escribe "Terminal"
- Presiona Enter

### 2️⃣ Navega a la carpeta del proyecto

```bash
cd /Users/mariova/Documents/proyecto_encuesta
```

### 3️⃣ Ejecuta el Dashboard

```bash
streamlit run app.py
```

**¡Listo!** El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

---

## 📌 Comandos Útiles

### Ver estadísticas calculadas
```bash
open data/processed/estadisticas_salarios.xlsx
```

### Re-procesar datos (si actualizas el CSV)
```bash
python src/etl/normalizer.py
python src/analytics/estadisticas.py
streamlit run app.py
```

### Detener el dashboard
En la terminal donde está corriendo, presiona: `Ctrl + C`

---

## 🎯 Navegación en el Dashboard

1. **Home**: Vista inicial con resumen
2. **📊 Visión General**: Click en el menú lateral
   - Filtra por Rubro y Tamaño
   - Explora gráficos interactivos
3. **👤 Análisis por Cargo**: Click en el menú lateral
   - Selecciona un área funcional
   - Elige un cargo específico
   - Compara Grande vs Pyme

---

## ❓ Problemas Comunes

### "command not found: streamlit"
```bash
pip install -r requirements.txt
```

### El navegador no se abre automáticamente
Abre manualmente: `http://localhost:8501`

### Errores de datos
```bash
python src/etl/normalizer.py
python src/analytics/estadisticas.py
```

---

**¡Disfruta explorando los datos de la Encuesta Salarial!** 🎉

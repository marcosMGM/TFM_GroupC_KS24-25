# ✅ To-Do List de la recta final del proyecto

Lista de tareas colaborativas del equipo. Actualiza el estado y añade comentarios conforme avancemos.

---

## 🧾 Backoffice

| Tarea                                                                          | Responsable(s) | Estado        | Comentarios                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------ | -------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Añadir ROI en `/idealista/`                                                    | Mario, David   | ✅ Completado | Mostrar rentabilidad basada en ROI                                                                                                                                                                                                                                                                                                                                                                                  |
| Añadir coste +10% como dato adicional para calcular rentabilidad               | Mario, David   | ✅ Completado | Coste total vivienda incluido impuesto                                                                                                                                                                                                                                                                                                                                                                              |
| Ajustar el orden de la `DataTable`                                             | Mario, David   | ✅ Completado | Mejorar visualización                                                                                                                                                                                                                                                                                                                                                                                               |
| Implementar área de filtrado y búsqueda                                        | Mario, David   | ✅ Completado | Filtros por parámetros clave                                                                                                                                                                                                                                                                                                                                                                                        |
| Añadir widget de parámetros ROI ajustables en tiempo real                      | Mario, David   | ✅ Completado | Refrescar sin recargar página `/idealista`                                                                                                                                                                                                                                                                                                                                                                          |
| Añadir métrica PER (Coste adquisición / Ingresos anuales)                      | Mario, David   | ✅ Completado | Estimar años de recuperación de inversión. @Mario, he puesto ingresos anuales netos, es ¿ok?                                                                                                                                                                                                                                                                                                                        |
| Eliminar el menú de AIRBNB                                                     | David          | ✅ Completado |                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Poner BADGES que ayuden a predecir ROI                                         | David          | ✅ Completado | En `/idealista`                                                                                                                                                                                                                                                                                                                                                                                                     |
| Analizar si tiene cabida poner objetos ribbon con alguna vivienda              | David          | ⬜ Pendiente  | En `/home` u otra página nueva                                                                                                                                                                                                                                                                                                                                                                                      |
| Mover mapa a otra ruta y clasificar por roi                                    | David          | ⬜ Pendiente  |                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Refactorizar la personalización, calculando en la bd la estimación fact anual. | David          | ✅ Completado | He añadido un campo a la DB, llamado ARR (Annual Reccuring Revenue), cuando se actualiza el % de ocupación precalculamos en la base de datos los ingresos anuales para poderlos ordenar después en la lista y poder manejarlos de otra forma. Introduzco también PURCHASE_COST para reflejar el coste de la operación (impuestos y gastos) y TOTAL_PURCHASE_COST que refleja Importe de la vivienda + PURCHASE_COST |

---

## 🧪 Modelado

| Tarea                                     | Responsable(s) | Estado        | Comentarios                     |
| ----------------------------------------- | -------------- | ------------- | ------------------------------- |
| Crear notebook ETL estructurado           | Joseba, Marcos | ✅ Completado | Pipeline limpio y reutilizable  |
| Crear notebook final con modelo entrenado | Joseba, Marcos | ✅ Completado | Incluir validaciones y métricas |
| Scraping definitivo y robusto             | Joseba, Marcos | ✅ Completado | Manejar límites y errores       |

---

## 🧩 GitHub

| Tarea                                       | Responsable(s) | Estado         | Comentarios                          |
| ------------------------------------------- | -------------- | -------------- | ------------------------------------ |
| Consolidar trabajo en rama definitiva `dev` | Todos          | 🔄 En progreso | Fusionar ramas actuales. - JPTX: OK. |

---

## 📌 Notas

- Usa los siguientes íconos para el estado:
  - ⬜ Pendiente
  - 🔄 En progreso
  - ✅ Completado
  - ⌛ OK con anotación

---

## 📋Para tratar en la próxima reunión

- DSG: ¿Sería necesario reajustar todas las consultas, incluida la clasificación de oportunidades en función a la personalización del usuario? (Ej: Tengo un presupuesto máximo de 400k. El cálculo de percentiles para clasificar la rentabilidad de la vivienda lo saco con la población filtrada, o global?)
- DSG: Definir que KPI y otros indicadores queremos mostrar definitivamente. Se me ocurre crear una pantalla de recomendaciones y que salgan las 3 viviendas más rentables de cada distrito, aquí sí, complementando a la cuestión a tratar anterior, sería necesario que atienda a las personalizaciones.
- DSG: Separar el mapa quitandolo de la home para que no tarde en cargar, y cambiar el color de los puntos del mapa en función a la clasificación hecha según su rentabilidad? Actualizar los popup incluyendo información relevante.
- DSG: La mayoría de propiedades en las que pincho ya no están publicadas. Además, ahora que funciona el ordenado de la tabla, se ve facilmente que las propiedades más rentables son en realidad outliers. (Afueras de Madrid). ¿Hacemos un nuevo scrapping o lo dejamos así? ¿Hacemos una limpieza de datos?

**Última actualización:** 12/07/2025 19:30

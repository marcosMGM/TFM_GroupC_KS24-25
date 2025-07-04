# ✅ To-Do List de la recta final del proyecto

Lista de tareas colaborativas del equipo. Actualiza el estado y añade comentarios conforme avancemos.

---

## 🧾 Backoffice

| Tarea                                                                          | Responsable(s) | Estado              | Comentarios                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------ | -------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Añadir ROI en `/idealista/`                                                    | Mario, David   | ✅ Completado       | Mostrar rentabilidad basada en ROI                                                                                                                                                                                                                                                                                                                                                                                  |
| Añadir coste +10% como dato adicional para calcular rentabilidad               | Mario, David   | ✅ Completado       | Coste total vivienda incluido impuesto                                                                                                                                                                                                                                                                                                                                                                              |
| Ajustar el orden de la `DataTable`                                             | Mario, David   | ⬜ Pendiente        | Mejorar visualización                                                                                                                                                                                                                                                                                                                                                                                               |
| Implementar área de filtrado y búsqueda                                        | Mario, David   | ✅ Completado       | Filtros por parámetros clave                                                                                                                                                                                                                                                                                                                                                                                        |
| Añadir widget de parámetros ROI ajustables en tiempo real                      | Mario, David   | ⬜ Pendiente        | Refrescar sin recargar página `/idealista`                                                                                                                                                                                                                                                                                                                                                                          |
| Añadir métrica PER (Coste adquisición / Ingresos anuales)                      | Mario, David   | ⌛ OK con anotación | Estimar años de recuperación de inversión. @Mario, he puesto ingresos anuales netos, es ¿ok?                                                                                                                                                                                                                                                                                                                        |
| Eliminar el menú de AIRBNB                                                     | David          | ✅ Completado       |                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Poner BADGES que ayuden a predecir ROI                                         | David          | ⬜ Pendiente        | En `/idealista`                                                                                                                                                                                                                                                                                                                                                                                                     |
| Analizar si tiene cabida poner objetos ribbon con alguna vivienda              | David          | ⬜ Pendiente        | En `/home` u otra página nueva                                                                                                                                                                                                                                                                                                                                                                                      |
| Mover mapa a otra ruta y clasificar por roi                                    | David          | ⬜ Pendiente        |                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Refactorizar la personalización, calculando en la bd la estimación fact anual. | David          | ✅ Completado       | He añadido un campo a la DB, llamado ARR (Annual Reccuring Revenue), cuando se actualiza el % de ocupación precalculamos en la base de datos los ingresos anuales para poderlos ordenar después en la lista y poder manejarlos de otra forma. Introduzco también PURCHASE_COST para reflejar el coste de la operación (impuestos y gastos) y TOTAL_PURCHASE_COST que refleja Importe de la vivienda + PURCHASE_COST |

---

## 🧪 Modelado

| Tarea                                     | Responsable(s) | Estado        | Comentarios                     |
| ----------------------------------------- | -------------- | ------------- | ------------------------------- |
| Crear notebook ETL estructurado           | Joseba, Marcos | ⬜ Pendiente  | Pipeline limpio y reutilizable  |
| Crear notebook final con modelo entrenado | Joseba, Marcos | ⬜ Pendiente  | Incluir validaciones y métricas |
| Scraping definitivo y robusto             | Joseba, Marcos | ✅ Completado | Manejar límites y errores       |

---

## 🧩 GitHub

| Tarea                                       | Responsable(s) | Estado         | Comentarios                            |
| ------------------------------------------- | -------------- | -------------- | -------------------------------------- |
| Consolidar trabajo en rama definitiva `dev` | Todos          | 🔄 En progreso | Fusionar ramas actuales. - DSG: Yo OK. |

---

## 📌 Notas

- Usa los siguientes íconos para el estado:
  - ⬜ Pendiente
  - 🔄 En progreso
  - ✅ Completado
  - ⌛ OK con anotación

---

**Última actualización:** 04/07/2025 21:15

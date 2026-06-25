# Plan de Pruebas — Track QA · Gestor de Inventario

## 1. Estrategia

Probar `gestor-inventario` como caja negra sobre HTTP, sin modificar el código de la app.

- **API contract**: status codes, shape, campos obligatorios, manejo de errores.
- **Funcional**: happy path, boundary values, valores inválidos.
- **Integridad de datos**: stock refleja exactamente los movimientos.
- **Resiliencia / fallo simulado**: `ALERTS_FAIL=1` produce 503 donde aplique.
- **UI / E2E**: flujo real desde el frontend (movimiento + consulta de alertas).

## 2. Alcance

- Backend: endpoints bajo `/api`.
- Frontend: página en `/` (SPA estática).
- Fuera de alcance: rendimiento, carga, seguridad avanzada.

## 3. Herramientas

- `pytest` + `httpx` (API)
- `playwright` (E2E, deseable)
- Servicio local: `uvicorn app:app --port 8000`
- Evidencias: capturas, logs y reporte en markdown.

## 4. Criterios de aceptación

- Cobertura del 100% de endpoints.
- Detección verificada de los defects planteados.
- Suite pasando en forma consistente.

# Casos de prueba — Gestor de Inventario

## Matriz de cobertura

| ID | Feature | Endpoint | Happy path | Edge | Negativo | Prioridad |
|---|---|---|---|---|---|---|
| TC-API-01 | Health | GET /api/health | 200 + status ok | - | - | Alta |
| TC-API-02 | Suppliers | GET /api/suppliers | 200 lista supplier | Cantidad inicial 3 | Campo vacío en seed | Alta |
| TC-API-03 | Products | GET /api/products | 200 lista productos | Filtro stock bajo | - | Alta |
| TC-API-04 | Detail | GET /api/products/{id} | 200 detalle existente | 1, 9999 | body detallado | Alta |
| TC-API-05 | Create | POST /api/products | 201 + headers Location | Costo/stock igual a 0 | SKU duplicado (409), proveedor inválido (400) | Alta |
| TC-API-06 | Movement | POST /api/stock/movement | IN/OUT normal | qty 0, tipo mixto | tipo inválido (400), producto inexistente (404) | Alta |
| TC-API-07 | Alerts | GET /api/stock/alerts | 200 lista con alertas | Sin alertas | ALERTS_FAIL=1 → 503 | Alta |
| TC-API-08 | Movements | GET /api/movements | 200 lista ordenada desc | Paginación ausente | - | Media |
| TC-API-09 | E2E humo | / | Frontend carga | Assets faltantes | 500 en página | Media |

## Notas
- Se priorizan las ramas de producto-activo (active = 1).
- `ALERTS_FAIL=1` acota los escenarios 503 solo en `/api/stock/alerts` y movimiento `OUT`.

# Defect Report — Gestor de Inventario (SUT)

## Resumen

Suite API ejecutada: 17/17 PASS
Modo de fallo `ALERTS_FAIL=1` validado.
Defects conocidos confirmados en comportamiento observable.

## Defects confirmados

### D1 — Stock negativo permitido
- Severidad: Alta
- Hallazgo: `POST /api/stock/movement` con `type=OUT` y `qty > stock` retorna 201; el producto queda con stock negativo.
- Evidencia: `tests/test_api.py::TestStockMovements::test_register_out_movement_negative_stock_accepted`
- Repro:
  1. Crear producto con stock=10
  2. Registrar salida de 999
  3. Validar stock < 0

### D2 — Cantidades decimales aceptadas
- Severidad: Media
- Hallazgo: `qty` acepta valores como `2.5` y se almacena sin rechazo.
- Evidencia: `tests/test_api.py::TestStockMovements::test_register_movement_decimal_qty_accepted`
- Repro:
  1. Registrar movimiento IN con `qty=2.5`
  2. Observar respuesta 201 con `qty == 2.5`

### D3 — `min_stock` negativo aceptado
- Severidad: Media
- Hallazgo: `POST /api/products` acepta `min_stock=-1`; este producto nunca entrará a alertas aunque su stock sea 0.
- Evidencia: `tests/test_api.py::TestProducts::test_create_product_negative_min_stock_is_accepted`

### D4 — `cost_cents` negativo aceptado
- Severidad: Media
- Hallazgo: `POST /api/products` acepta `cost_cents=-1000` sin validación.
- Evidencia: `tests/test_api.py::TestProducts::test_create_product_negative_cost_cents_is_accepted`

## Modo falla alertas

- `GET /api/stock/alerts` retorna 503 cuando `ALERTS_FAIL=1`.
- `POST /api/stock/movement` con `type=OUT` retorna 503 cuando `ALERTS_FAIL=1`.
- Caso: `tests/test_api.py::TestAlertsFailMode`

## Pendiente E2E

- Completado: suite E2E con Playwright (5 tests) validando flujos UI.
- Tests: carga tabla productos, productos bajos resaltados, registro movimientos IN/OUT, consulta alertas.

## Recomendaciones (no ejecutadas por alcance)

- Rechazar `qty` decimales a nivel de modelo/schema.
- Validar `min_stock >= 0` y `cost_cents >= 0`.
- Validar `stock >= 0` antes de aplicar salida.

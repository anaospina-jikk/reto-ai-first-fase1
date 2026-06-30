# Casos de prueba Gherkin – gestor-inventario

## API REST

```gherkin
Feature: Salud del sistema
  Scenario: Health check responde OK
    Given la aplicación está corriendo
    When hago GET /api/health
    Then recibo HTTP 200
    And el JSON es { "status": "ok" }

  Scenario: Listar proveedores
    When hago GET /api/suppliers
    Then recibo HTTP 200
    And el body es una lista con al menos 3 proveedores
```

```gherkin
Feature: Productos
  Scenario: Listar productos
    When hago GET /api/products
    Then recibo HTTP 200
    And el body es una lista con al menos 6 productos

  Scenario: Obtener producto existente
    When hago GET /api/products/1
    Then recibo HTTP 200
    And el body incluye id=1, name y sku

  Scenario: Obtener producto inexistente
    When hago GET /api/products/9999
    Then recibo HTTP 404

  Scenario: Crear producto exitoso
    When hago POST /api/products con datos válidos
    Then recibo HTTP 201
    And el body incluye name y sku enviados

  Scenario: Crear producto con SKU duplicado
    When creo un producto con un SKU ya existente
    Then recibo HTTP 409

  Scenario: Crear producto con proveedor inexistente
    When hago POST /api/products con supplier_id inválido
    Then recibo HTTP 400

  Scenario: Crear producto acepta valores negativos (min_stock y cost_cents)
    When envío min_stock=-1 y cost_cents=-1000
    Then recibo HTTP 201
    And el body refleja esos valores negativos
```

```gherkin
Feature: Movimientos de stock
  Scenario: Registrar entrada de stock
    When creo un producto y envío un movimiento IN qty=5
    Then recibo HTTP 201
    And el movimiento incluye type="IN" y qty=5

  Scenario: Salida de stock descuenta existencia
    Cuando creo un producto con stock inicial 10
    And envío un movimiento OUT qty=2
    Then el stock actual del producto es 8

  Scenario: Salida de stock no valida stock negativo (bug aceptado)
    Cuando creo un producto con stock inicial 10
    And envío un movimiento OUT qty=999
    Then recibo HTTP 201
    And el stock puede quedar negativo

  Scenario: Movimiento acepta cantidad decimal
    When envío un movimiento IN con qty=2.5
    Then recibo HTTP 201
    And el movimiento registra qty=2.5
```

```gherkin
Feature: Alertas de stock
  Scenario: Consultar alertas
    When hago GET /api/stock/alerts
    Then recibo HTTP 200
    And el body es una lista

  Scenario: Simular caída del servicio de alertas
    Given defino ALERTS_FAIL=1
    When hago GET /api/stock/alerts
    Then recibo HTTP 503

  Scenario: Movimiento OUT cuando servicio de alertas no disponible
    Given defino ALERTS_FAIL=1
    When creo un producto y envío un movimiento OUT
    Then recibo HTTP 503
```

## Frontend (E2E)

```gherkin
Feature: Interfaz web
  Scenario: Tabla de productos renderiza con datos iniciales
    Given abro la página principal
    When espero la tabla de productos
    Then hay al menos 6 filas
    And cada fila tiene al menos 7 columnas

  Scenario: Productos en alerta se resaltan
    Given abro la página principal
    Then se muestran badges de estado en las filas

  Scenario: Registrar movimiento IN desde la UI
    Given abro la página principal
    When selecciono producto, tipo IN, cantidad 5 y envío
    Then veo "Movimiento #"
    And veo "Entrada" o "IN"

  Scenario: Registrar movimiento OUT desde la UI
    Given abro la página principal
    When selecciono producto, tipo OUT, cantidad 1 y envío
    Then veo "Movimiento #"
    And veo "Salida" o "OUT"

  Scenario: Consultar alertas desde la UI
    Given abro la página principal
    When hago clic en #refresh-alerts
    Then veo la tabla de alertas o el mensaje "sin alertas"
```

## Matriz de resultados (expected)

| ID | Feature | Scenario | Estado | Observación |
|---|---|---|---|---|
| API-01 | Salud | Health check responde OK | PASS | 200 + JSON status ok |
| API-02 | Salud | Listar proveedores | PASS | 200 + lista >= 3 |
| API-03 | Productos | Listar productos | PASS | 200 + lista >= 6 |
| API-04 | Productos | Obtener producto existente | PASS | 200 con id=1 |
| API-05 | Productos | Obtener producto inexistente | PASS | 404 |
| API-06 | Productos | Crear producto exitoso | PASS | 201 |
| API-07 | Productos | Crear producto con SKU duplicado | PASS | 409 |
| API-08 | Productos | Crear producto proveedor inexistente | PASS | 400 |
| API-09 | Productos | Acepta valores negativos | PASS | 201 y body refleja negativos |
| API-10 | Movimientos | Registrar entrada | PASS | 201 + campos correctos |
| API-11 | Movimientos | Salida descuenta stock | PASS | stock=8 |
| API-12 | Movimientos | Salida sin validación de negativo | PASS | 201 y stock negativo (bug aceptado) |
| API-13 | Movimientos | Decimal en cantidad | PASS | 201 y qty=2.5 |
| API-14 | Alertas | Consultar alertas | PASS | 200 + lista |
| API-15 | Alertas | Simular caída | PASS | 503 |
| API-16 | Alertas | OUT con servicio caído | PASS | 503 |
| UI-01 | Frontend | Tabla renderizada | PASS | filas >=6 con columnas >=7 |
| UI-02 | Frontend | Resaltado de alertas | PASS | badges visibles |
| UI-03 | Frontend | Movimiento IN | PASS | confirmación IN/Entrada |
| UI-04 | Frontend | Movimiento OUT | PASS | confirmación OUT/Salida |
| UI-05 | Frontend | Alertas UI | PASS | tabla o mensaje sin alertas |

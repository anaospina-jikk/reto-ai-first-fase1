# Plan de pruebas — Reto AI-First · Track QA

## 1. Estrategia
Verificación funcional y no funcional mínima del backend FastAPI del Gestor de Inventario.
Enfoque:
- API REST: caja negra con verificaciones de contrato y códigos HTTP.
- E2E (opcional): recorridos contra UI estática en `localhost:8000` para validar humo/flujo del frontend.

## 2. Alcance
### Incluido
- `/api/health`, `/api/suppliers`, `/api/products`, `/api/products/{id}`
- `/api/products` (POST), `/api/stock/movement` (POST)
- `/api/stock/alerts`, `/api/movements`

### Excluido
- Código fuente (no se modifica el SUT)
- Datos.gov.co / SECOP (no aplica)
- Seguridad avanzada (CORS abierto por diseño del SUT)

## 3. Riesgos
- Dependencia de estado (DB SQLite local), requiere datos seed.
- Simulación de fallo `ALERTS_FAIL=1` acota solo dos endpoints.
- Ejecución concurrente compartiendo `inventario.db`.

## 4. Criterios de aceptación
- Suite API pasa 100% en ambiente controlado.
- Defectos críticos documentados con repro + evidence.

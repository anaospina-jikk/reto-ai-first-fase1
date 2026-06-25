# SOUL.md — Reto AI First · Fase 1 · Track QA

Rama del reto: main (clone personal)
SUT: `3-challenge/gestor-inventario`
Estado: Completado
Fecha inicio: 2026-06-25

---

## 1. Alcance

- Probar el SUT como caja negra sobre HTTP sin modificar su código.
- Cubrir API contract, funcional, integridad de datos y fallo simulado de alertas (`ALERTS_FAIL=1`).
- Incluir al menos un flujo E2E mínimo sobre la UI cuando sea posible.
- Entregar: plan de pruebas, suite de API ejecutable, defect report y proceso documentado aquí.

## 2. Herramientas y stack

- Orquestación: Hermes Agent
- Suite API: `pytest` + `httpx` + `TestClient`
- E2E (si aplica): Playwright sobre `http://localhost:8000`
- Control de versiones: Git + GitHub

## 3. Decisiones

- Usar `TestClient` para ejecutar la API sin levantar servidor HTTP externo.
- Mantener la suite en el SUT, fuera del repo de entregas del reto, para no contaminar la app.
- Generar SKUs únicos por test para evitar 409s por estado compartido.
- Priorizar primero una suite verde y estable.

## 4. Ejecución

### API
```bash
cd 3-challenge/gestor-inventario
python -m pytest tests/test_api.py -q
```
Resultado: 17 tests PASS.

### E2E
```bash
cd 3-challenge/gestor-inventario
uvicorn app:app --port 8001 &
python -m pytest tests/test_e2e.py -v
```
Resultado: 5 tests PASS (Playwright + Chromium).

## 5. Hallazgos y defects

Ver `QA-defect-report.md`.

## 6. Pendientes

- [x] Definir ubicación de documentación y artefactos de QA.
- [x] Crear suite API inicial.
- [x] Ejecutar y estabilizar suite E2E con Playwright (5/5 PASS).
- [x] Cerrar reporte de defects con severidad y evidencias.
- [x] Revisar cobertura frente a los 4 defects conocidos (todos detectados).

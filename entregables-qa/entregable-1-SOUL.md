# SOUL.md — Reto AI-First · Track QA

## Proyecto
Aplicación probada: **Gestor de Inventario** (FastAPI + SQLite) bajo `3-challenge/gestor-inventario/`.
Ruta local: `C:\Users\vkos7\QA-IA\reto-ai-first-fase1\3-challenge\gestor-inventario`.
Repositorio: https://github.com/anaospina-jikk/reto-ai-first-fase1 (rama `anaospina`).

Estrategia de cobertura:
- Fase 1: Reconocimiento del SUT y endpoints.
- Fase 2: Generación asistida con Hermes + LLM de suite API completa (contrato, errores, casos límite).
- Fase 3: Pruebas E2E contra `localhost:8000` (cuando aplica).
- Fase 4: Ejecución y reporte de defectos.

## Stack de pruebas
- **Backend test runner**: pytest + httpx
- **E2E**: Playwright (unofficial) o navegador headless
- **API**: Suite generada con Hermes/LLM sobre FastAPI
- **Documentación**: Markdown tablas + Gherkin

## Uso de Hermes y LLMs
- Prompt inicial: generar suite API completa para gestor-inventario.
- Iteraciones: ajuste de casos negativos (SKU duplicado, 404, ALERTS_FAIL).
- Mejora continua: agregar validación de schemas y pruebas de contract.

## Decisiones y trade-offs
- Dado que no se puede modificar el SUT, las pruebas son **observacionales** (caja negra).
- Se prioriza validar:
  - Health, suppliers, productos y movimientos.
  - Errores esperados (404, 409, 503).
- E2E se marca como deseable por tiempo.

## Hallazgos
Ver `entregable-6-reporte-defectos.md`.

## Bloqueos y resolución
- Acceso remoto limitado al hosting de Hermes para ejecución automática; se resolvió usando ejecución local (`uvicorn app:app --port 8000`).
- ALERTS_FAIL requiere entorno en la misma sesión; ajuste documentado en pruebas.

## Enlace al repositorio
https://github.com/anaospina-jikk/reto-ai-first-fase1/tree/anaospina

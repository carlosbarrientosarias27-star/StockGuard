# AUDIT.md — Auditoría de Vulnerabilidades de StockGuard

### Vulnerabilidades Identificadas

## 1. Sin validación de `qty` y `price` (CRÍTICA)

**Descripción:** Las funciones `add_item()` y `update_price()` aceptan
cualquier valor numérico, incluyendo negativos y cero. Un usuario puede
introducir `qty=-100` o `price=-9.99` sin que el sistema lo rechace.

**Riesgo real:** En producción, un inventario con valores negativos
produciría un valor total incorrecto (`get_total_value()` negativo),
corrompería los informes financieros y podría enmascarar robos o errores
de stock.

**Corrección aplicada:** Se creó `validator.py` con `validate_qty()` y
`validate_price()`. La dataclass `Item` lanza `ValueError` en
`__post_init__`. `storage.py` llama al validador antes de persistir.

---

## 2. Sin manejo de JSON corrupto (ALTA)

**Descripción:** `load_inventory()` llama directamente a `json.load()`
sin capturar `json.JSONDecodeError`. Si el archivo `inventory.json` está
corrupto (escritura interrumpida, edición manual errónea), el programa
lanza una excepción no controlada y se detiene.

**Riesgo real:** Un fallo de escritura en disco o un reinicio inesperado
del sistema puede corromper el archivo. Sin manejo de errores, el sistema
queda completamente inutilizable hasta intervención manual.

**Corrección aplicada:** `storage.py` envuelve `json.load()` en un bloque
`try/except json.JSONDecodeError` y devuelve `[]` como fallback seguro.
También se maneja `FileNotFoundError` de forma explícita.

---

## 3. Ausencia total de tests y documentación (MEDIA)

**Descripción:** El código heredado no tiene ningún test unitario ni
docstrings. Cualquier cambio en el código puede introducir regresiones
sin que el equipo lo detecte.

**Riesgo real:** Sin tests, no hay forma automática de verificar que las
correcciones de las vulnerabilidades 1 y 2 funcionan correctamente. En
un entorno con múltiples desarrolladores, esto multiplica el riesgo de
bugs en producción.

**Corrección aplicada:** Se añadieron tests con `pytest` para modelos,
validadores y storage (incluyendo mocks). Todas las funciones públicas
tienen docstrings en formato Google. Se configuró un pipeline CI/CD con
GitHub Actions para ejecutar los tests en cada push.
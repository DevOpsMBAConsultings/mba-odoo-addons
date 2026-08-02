# Estándar de la casa

Reglas para cualquier módulo que entre a este repositorio. Antes de commitear,
`python3 tools/check_manifests.py` las verifica todas de un tirón.

## Manifiesto

Comillas simples, este orden de claves, sin excepciones:

```python
{
    'name': 'Nombre visible del módulo',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Reporting',
    'summary': 'Una línea, sin punto final',
    'description': 'Párrafo corto explicando qué resuelve.',
    'author': 'MBA Consultings, Brooks Gonzalez',
    'website': 'https://mbaconsultings.com',
    'depends': ['account'],
    'data': [],
    'demo': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
```

- **`author` es innegociable.** Siempre `MBA Consultings, Brooks Gonzalez`, tal
  cual. No se omite, no se abrevia, no se reemplaza por el nombre del cliente.
- **`website`** apunta a mbaconsultings.com, no al repositorio.
- **`version`** sigue el formato de la OCA: `18.0.<mayor>.<menor>.<parche>`.
  El prefijo `18.0` es el de la serie de Odoo y no cambia dentro de la rama.
- **`license`**: `LGPL-3` salvo que haya una razón deliberada para otra cosa.

## Nombre técnico

Prefijo `mba_` más el área funcional: `mba_account_aging`,
`mba_finance_dashboard`. El nombre describe qué hace el módulo, no dónde se
ve. Un módulo que agrega datos contables no se llama `..._dashboard` porque
alguien vaya a graficarlos después.

## Estructura mínima

```
mba_mi_modulo/
├── README.md                        obligatorio
├── __init__.py
├── __manifest__.py
├── i18n/es.po                       si hay cadenas visibles
├── models/
├── security/
│   ├── ir.model.access.csv          siempre
│   └── *_security.xml               reglas de registro si hay company_id
├── static/description/icon.png      obligatorio, 140x140
└── views/
```

## Seguridad

Todo modelo nuevo lleva su línea en `ir.model.access.csv`. Los modelos de solo
lectura llevan `perm_read` en 1 y el resto en 0. Si el modelo tiene
`company_id`, lleva además una `ir.rule` multicompañía **global** (sin grupos
asignados): el aislamiento entre compañías tiene que aplicar a todos, gerentes
incluidos.

## Idioma

Código y cadenas en inglés; traducción al español en `i18n/es.po`. Así el
módulo sirve para cualquier cliente sin tocar el código.

## Antes de subir

```bash
python3 tools/check_manifests.py
```

# MBA Odoo Addons

Módulos Odoo 18 desarrollados y mantenidos por **MBA Consultings**, listos para
instalar en cualquier proyecto.

| Módulo | Qué hace |
| --- | --- |
| [`mba_account_aging`](mba_account_aging) | Antigüedad de cuentas por cobrar y por pagar por días vencidos, como modelo analizable. Tramos configurables por compañía. |
| [`mba_finance_dashboard`](mba_finance_dashboard) | Tablero financiero listo para usar: antigüedad, posición neta y resultado del año. Se instala armado. |

## Instalación

```bash
git clone -b 18.0 https://github.com/DevOpsMBAConsultings/mba-odoo-addons.git \
    /opt/odoo/custom-addons/mba-odoo-addons
```

Agregue la ruta al parámetro `addons_path` de su `odoo.conf`, reinicie el
servicio, actualice la lista de aplicaciones e instale el módulo deseado.

```
addons_path = /opt/odoo/addons,/opt/odoo/custom-addons/mba-odoo-addons
```

## Compatibilidad

Odoo 18.0 Community y Enterprise. Los módulos no dependen de Enterprise.

## Licencia

LGPL-3. Vea [LICENSE](LICENSE).

## Soporte

MBA Consultings — Desarrollo y Arquitectura Cloud | DevOps & Odoo Specialists.

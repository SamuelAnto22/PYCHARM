# -*- coding: utf-8 -*-
import sys
import xmlrpc.client

ODOO_URL = "http://localhost:8069"
ODOO_DB = "samuel"
ODOO_USER = "samuelantoniocordovarojas@gmail.com"
ODOO_PASSWORD = "SamAnt22.!"

ALLOWED_COMMANDS = {"crear", "consultar", "borrar", "salir", "sortir"}


def _clean_value(value: str) -> str:
    value = value.strip()
    if value and value[0] in ('"', "'", "“", "”"):
        value = value[1:]
    if value and value[-1] in ('"', "'", "“", "”"):
        value = value[:-1]
    return value.strip()


def _parse_params(parts):
    params = {}
    for part in parts:
        if "=" not in part:
            continue
        key, val = part.split("=", 1)
        key = key.strip()
        val = _clean_value(val)
        if key:
            params[key] = val
    return params


def _connect():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
    if not uid:
        raise RuntimeError("No se pudo autenticar en Odoo. Revisa usuario/clave/BD.")
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models


def _crear(models, uid, nombre, ref):
    partner_id = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "create",
        [{"name": nombre, "ref": ref}],
    )
    return partner_id


def _consultar(models, uid, ref):
    ids = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "search",
        [[("ref", "=", ref)]],
        {"limit": 1},
    )
    if not ids:
        return None
    data = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "read",
        [ids],
        {"fields": ["name", "ref"]},
    )
    return data[0] if data else None


def _borrar(models, uid, ref):
    ids = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "search",
        [[("ref", "=", ref)]],
        {"limit": 1},
    )
    if not ids:
        return False
    ok = models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        "res.partner",
        "unlink",
        [ids],
    )
    return bool(ok)


def main():
    try:
        uid, models = _connect()
    except Exception as exc:
        print(f"Error de conexión: {exc}")
        sys.exit(1)

    print("Conectado a Odoo (uid: %s). Escribe 'salir' o 'sortir' para terminar." % uid)

    while True:
        try:
            raw = input("Orden > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo...")
            break

        if not raw:
            continue

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            continue

        command = parts[0].lower()
        if command in {"salir", "sortir"}:
            print("Saliendo...")
            break

        if command not in ALLOWED_COMMANDS:
            print("Orden no soportada")
            continue

        params = _parse_params(parts[1:])
        try:
            if command == "crear":
                nombre = params.get("nombre")
                ref = params.get("num_socio")
                if not nombre or not ref:
                    print("Faltan parámetros. Usa: Crear,nombre=\"Nombre\",num_socio=\"REF001\"")
                    continue
                partner_id = _crear(models, uid, nombre, ref)
                print(f"Socio creado con éxito en Odoo (ID: {partner_id}).")

            elif command == "consultar":
                ref = params.get("num_socio")
                if not ref:
                    print("Falta num_socio. Usa: Consultar,num_socio=\"REF001\"")
                    continue
                data = _consultar(models, uid, ref)
                if not data:
                    print("Socio no encontrado.")
                else:
                    print(f"Datos de Odoo -> Nombre: {data.get('name')} | Referencia: {data.get('ref')}")

            elif command == "borrar":
                ref = params.get("num_socio")
                if not ref:
                    print("Falta num_socio. Usa: Borrar,num_socio=\"REF001\"")
                    continue
                ok = _borrar(models, uid, ref)
                if ok:
                    print("Socio eliminado con éxito.")
                else:
                    print("Socio no encontrado.")

            else:
                print("Orden no soportada")

        except Exception as exc:
            print(f"Error al procesar la orden: {exc}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Valida el catálogo maestro y prepara dos CSV de revisión para TikTok Shop.

Los CSV NO son plantillas oficiales de Seller Center; la categoría y atributos
requeridos se mapearán cuando la cuenta de vendedor esté configurada.
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalogo.json"


def load_and_validate():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if data.get("moneda") != "MXN" or not isinstance(data.get("productos"), list):
        raise ValueError("El catálogo requiere moneda MXN y una lista de productos.")
    skus = set()
    for p in data["productos"]:
        for field in ("id", "sku", "title", "category", "price", "image", "desc", "tipo_venta"):
            if not p.get(field):
                raise ValueError(f"Producto incompleto: falta {field} en {p.get('sku', '?')}")
        if p["sku"] in skus:
            raise ValueError(f"SKU duplicado: {p['sku']}")
        skus.add(p["sku"])
        if p["tipo_venta"] not in ("fijo", "desde", "cotizacion"):
            raise ValueError(f"Tipo de venta inválido en {p['sku']}")
        if p["tipo_venta"] == "fijo" and (
            not isinstance(p.get("precio_fijo_mxn"), (int, float))
            or isinstance(p.get("precio_fijo_mxn"), bool)
            or p["precio_fijo_mxn"] <= 0
        ):
            raise ValueError(f"Precio fijo inválido en {p['sku']}")
        stock = p.get("stock")
        if stock is not None and (not isinstance(stock, int) or isinstance(stock, bool) or stock < 0):
            raise ValueError(f"Stock inválido en {p['sku']}")
    return data["productos"]


def export(products, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    approved, pending = [], []
    for p in products:
        reasons = []
        if p["tipo_venta"] != "fijo":
            reasons.append("Definir variante y precio final")
        if p.get("stock") is None:
            reasons.append("Confirmar inventario o disponibilidad")
        if not p.get("derechos_confirmados"):
            reasons.append("Revisar derechos/licencia del diseño")
        if not p.get("aprobado_tiktok"):
            reasons.append("Aprobar producto para TikTok")
        if not str(p.get("image", "")).startswith("https://"):
            reasons.append("Agregar foto HTTPS válida")
        if reasons:
            pending.append({"sku": p["sku"], "nombre": p["title"], "motivos": "; ".join(reasons)})
        else:
            approved.append({
                "sku": p["sku"], "nombre": p["title"], "descripcion": p["desc"],
                "precio_mxn": p["precio_fijo_mxn"], "stock": p["stock"],
                "imagen_url": p["image"], "categoria_interna": p["category"],
            })
    def write_csv(filename, fieldnames, rows):
        with (output_dir / filename).open("w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    write_csv("tiktok_preparacion.csv",
              ["sku", "nombre", "descripcion", "precio_mxn", "stock", "imagen_url", "categoria_interna"], approved)
    write_csv("tiktok_pendientes.csv", ["sku", "nombre", "motivos"], pending)
    print(f"Catálogo: {len(products)} productos; {len(approved)} listos para preparar; {len(pending)} pendientes.")
    print("Los CSV son de preparación, NO se suben directamente como plantilla oficial.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Solo valida el catálogo")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "exports")
    args = parser.parse_args()
    products = load_and_validate()
    print(f"Validación correcta: {len(products)} productos y SKUs únicos.")
    if not args.check:
        export(products, args.out_dir)

# Pendragon Forge Studios — catálogo maestro

La web de Pendragon Forge está alojada como sitio estático. Los productos del catálogo público se administran en **catalogo.json**: la página los carga automáticamente, permite buscarlos y conserva las solicitudes por WhatsApp.

## Cómo editar el catálogo

1. Abrir `catalogo.json` y modificar el producto correspondiente (título, descripción, foto, categoría, precio visible).
2. Mantener el `sku` estable: será el identificador para cruzar web, inventario y TikTok Shop.
3. Validar con `python3 scripts/catalogo.py --check`.
4. Revisar la vista previa de Vercel antes de fusionar el cambio a `main`.

Los campos `price` y `precio_fijo_mxn` no son intercambiables: el primero es el texto público, y el segundo es un importe definitivo solo para artículos de `tipo_venta: "fijo"`. Los productos con `tipo_venta: "desde"` o `"cotizacion"` necesitan variantes o una cotización antes de venderse con checkout.

`stock: null` significa **inventario no confirmado**, no que esté agotado. Completar también materiales, medidas, peso, plazo de fabricación y variantes antes de publicar en un marketplace.

## Exportación preparatoria para TikTok Shop

Ejecutar `python3 scripts/catalogo.py`. El script genera dos CSV en `exports/`:

- `tiktok_preparacion.csv`: productos con precio fijo, stock definido, derechos revisados y aprobación interna.
- `tiktok_pendientes.csv`: lista de productos y datos que faltan.

**No son plantillas oficiales de TikTok Shop y no publican nada automáticamente.** El Seller Center de México puede exigir categorías, atributos, imágenes, dimensiones y variantes específicas. Después de verificar la cuenta de vendedor, adaptaremos el exportador a la plantilla real o a un integrador/API autorizado.

Todos los productos empiezan con `derechos_confirmados: false` y `aprobado_tiktok: false` hasta revisión. Especial atención a figuras basadas en Pokémon, Yu-Gi-Oh!, Sanrio u otras marcas: no se deben publicar sin los derechos o licencias correspondientes.

## Siguientes integraciones

- **Checkout web:** definir proveedor de cobro/carrito y política de envíos; actualmente WhatsApp sigue siendo la vía de pedidos.
- **TikTok Shop:** completar Seller Center, validar productos y habilitar importación o sincronización autorizada.
- **Catálogo editable sin tocar código:** conectar una hoja de Google Sheets como interfaz de administración y automatizar la generación validada del JSON, con revisión antes de publicar.

Nunca colocar contraseñas, tokens o claves de TikTok en este repositorio ni en el JavaScript del navegador.

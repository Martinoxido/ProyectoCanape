def calcular_total(lista_items_texto):
    total = 0.0
    for texto in lista_items_texto:
        try:
            # Extraemos el monto después del último '$'
            precio_str = texto.split("$")[-1]
            precio = float(precio_str)
            total += precio
        except Exception:
            # Ignorar items con formato incorrecto
            pass
    return total

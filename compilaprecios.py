import pandas as pd
import glob
import os

# Diccionario de categorías y sus palabras clave
categorias_palabras = {
    "EXCLUSIVOS ARETE": ["exclusivo", "premium", "arete", "selecto"],
    "SABORES DE ASIA": ["asiático", "sushi", "soja", "sésamo", "curry", "ramen", "wasabi", "ginger", "matcha"],
    "PROMOCIONES Y OFERTAS": ["oferta", "promo", "descuento", "rebaja", "promoción"],
    "ADEREZOS/CONDIMENTOS": ["aderezo", "condimento", "salsa", "mayonesa", "mostaza", "ketchup", "vinagre", "picante"],
    "ALMACEN": ["arroz", "pasta", "legumbres", "harina", "aceite", "azúcar", "sal", "cereal"],
    "BAZAR": ["utensilio", "vajilla", "menaje", "cocina", "decoración", "hogar"],
    "BEBIDAS CON ALCOHOL": ["vino", "cerveza", "licor", "champán", "whisky", "ron", "tequila", "coctel", "alcohol"],
    "BEBIDAS SIN ALCOHOL": ["jugo", "refresco", "agua", "soda", "batido", "limonada", "té helado"],
    "CARNICERIA": ["carne", "costilla", "lomo", "filete", "pollo", "pavo", "embutido", "asado"],
    "CHOCOLATE Y GOLOSINAS": ["chocolate", "dulce", "bombón", "caramelo", "golosina", "confitería"],
    "CONFITERÍA": ["confitería", "galleta", "pastel", "postre", "mermelada"],
    "CONGELADOS": ["congelado", "helado", "frozen", "pizza congelada", "guiso congelado"],
    "CUIDADO DEL HOGAR": ["limpieza", "detergente", "jabón", "desinfectante", "escoba", "mopa", "insecticida"],
    "CUIDADO PERSONAL": ["cuidado personal", "shampoo", "acondicionador", "jabón", "desodorante", "crema", "loción", "perfume"],
    "DESAYUNO": ["cereal", "leche", "pan", "mantequilla", "café", "té", "mermelada", "huevo", "yogur"],
    "ENLATADOS": ["enlatado", "conserva", "atún", "maíz", "sopa", "frijol", "verdura enlatada"],
    "FIAMBRES": ["fiambre", "jamón", "salchicha", "mortadela", "queso procesado"],
    "FRUTAS Y VERDURAS": ["fruta", "verdura", "vegetal", "ensalada", "manzana", "banana", "naranja", "lechuga", "tomate"],
    "ELECTRODOMESTICOS": ["electrodoméstico", "microondas", "licuadora", "refrigerador", "lavadora", "televisor"],
    "LACTEOS": ["lácteo", "leche", "yogur", "queso", "mantequilla", "crema"],
    "MASCOTAS": ["mascota", "alimento para mascotas", "comida para perro", "comida para gato", "pienso", "accesorio para mascotas"],
    "PANADERIA": ["pan", "baguette", "croissant", "pan dulce", "bollería", "pastelería"],
    "PASTAS FRESCAS": ["pasta fresca", "ravioli", "tallarines", "fettuccine", "pasta casera"],
    "QUESOS": ["queso", "queso rallado", "queso fresco", "queso curado"],
    "ROTISERÍA": ["rotisería", "pollo asado", "pollo rostizado", "carne rostizada", "comida preparada"],
    "TIENDA": ["tienda", "miscelánea", "diversos", "accesorios", "varios"],
    "JUGUETERIA": ["juguete", "juguetería", "juego", "muñeca", "pelota", "rompecabezas"],
    "FERRETERIA Y JARDIN": ["ferretería", "jardín", "herramienta", "tijeras", "cinta métrica", "martillo"],
    "COTILLON": ["cotillón", "fiesta", "disfraz", "globos", "confeti"],
    "LIBRERIA": ["librería", "libro", "cuaderno", "papelería", "escolar"]
}

def clasificar_producto(producto):
    """Revisa el campo 'Producto' y asigna una categoría según las palabras clave."""
    producto_lower = producto.lower() if isinstance(producto, str) else ""
    for categoria, palabras in categorias_palabras.items():
        if any(palabra in producto_lower for palabra in palabras):
            return categoria
    return "Sin clasificación"

# Definir el directorio donde se encuentran los archivos CSV
directory = r'C:\Users\dmeza\preciossupermercados'
# Construir el patrón de búsqueda para los archivos CSV generados
pattern = os.path.join(directory, "preciossupermercados_*.csv")
# Obtener la lista de archivos que cumplen con el patrón
csv_files = glob.glob(pattern)

if not csv_files:
    print("No se encontraron archivos CSV con el patrón especificado.")
else:
    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
        except Exception as e:
            print(f"Error al cargar el archivo {file}: {e}")
    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)
        print("Datos combinados de todos los archivos:")
        print(final_df.head())
        
        # Limpieza y conversión de precios: reemplazar comas por puntos, eliminar caracteres no numéricos y convertir a numérico
        final_df['Precio'] = final_df['Precio'].astype(str).str.replace(',', '.')
        final_df['Precio'] = final_df['Precio'].str.replace(r'[^\d.]', '', regex=True)
        final_df['Precio'] = pd.to_numeric(final_df['Precio'], errors='coerce')
        
        # Clasificación: si ya existe la columna "Grupo", se usa; de lo contrario, se genera "Categoria_Nueva" usando la función
        if "Grupo" in final_df.columns:
            final_df["Categoria_Nueva"] = final_df["Grupo"]
        else:
            final_df["Categoria_Nueva"] = final_df["Producto"].apply(clasificar_producto)
        
        print("Datos con la nueva columna 'Categoria_Nueva':")
        print(final_df.head())
        
        # Exportar a CSV y Excel
        csv_file = os.path.join(directory, "preciossupermercados_combined.csv")
        excel_file = os.path.join(directory, "preciossupermercados_combined.xlsx")
        try:
            final_df.to_csv(csv_file, index=False)
            final_df.to_excel(excel_file, index=False)
            print(f"Archivo CSV guardado correctamente en: {csv_file}")
            print(f"Archivo Excel guardado correctamente en: {excel_file}")
        except Exception as e:
            print("Error al guardar los archivos combinados:", e)
    else:
        print("No se pudieron cargar los DataFrames.")

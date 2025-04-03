import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

##############################################
# SCRAPING DE STOCK
##############################################

def scrape_stock():
    """
    Scrapea productos del supermercado Stock.com.py y asigna grupos según la URL.
    Retorna una lista de diccionarios con los datos y asigna "Supermercado": "Stock".
    """
    stock_urls = [
        "https://www.stock.com.py/category/5-almacen-aderezoscondimentos-especias.aspx",
        "https://www.stock.com.py/category/245-bebidas-alcoholicas-aperitivos-con-alcohol.aspx",
        "https://www.stock.com.py/category/608-perecedero-carnes-cerdo-granel.aspx",
        "https://www.stock.com.py/category/466-limpieza-hogar-escobas.aspx",
        "https://www.stock.com.py/category/676-perecedero-huevos-huevos-de-gallinas.aspx",
        "https://www.stock.com.py/category/705-perecedero-panaderia-panes-frescos.aspx?idFiltro=1512"
    ]
    
    grupo_mapping = {
        "aderezoscondimentos": "Almacén y Condimentos",
        "bebidas-alcoholicas": "Bebidas y Aperitivos",
        "carnes": "Carnicería",
        "limpieza-hogar": "Cuidado del Hogar",
        "huevos": "Huevos",
        "panaderia": "Panadería"
    }
    
    data = []
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for url in stock_urls:
        print(f"Procesando Stock: {url}")
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error al conectar con {url}: {e}")
            continue
        if response.status_code != 200:
            print(f"Error al obtener {url}: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="product-item")
        if not products:
            print(f"No se encontraron productos en {url}")
            continue
        
        # Determinar grupo según la URL
        grupo = "Otros"
        for key, val in grupo_mapping.items():
            if key in url:
                grupo = val
                break
        
        for product in products:
            h2 = product.find("h2", class_="product-title")
            nombre = h2.get_text(strip=True) if h2 else "No encontrado"
            span = product.find("span", class_="price-label")
            precio = span.get_text(strip=True) if span else "No encontrado"
            data.append({
                "Supermercado": "Stock",
                "Categoría": url,
                "Producto": nombre,
                "Precio": precio,
                "FechaConsulta": fecha_consulta,
                "Grupo": grupo
            })
    return data

##############################################
# SCRAPING DE SUPERSEIS
##############################################

def scrape_superseis():
    """
    Scrapea productos del supermercado Superseis y asigna "Supermercado": "Superseis".
    Retorna una lista de diccionarios con los datos.
    """
    superseis_urls = [
        "https://www.superseis.com.py/category/676-perecedero-huevos-huevos-de-gallinas.aspx",
        "https://www.superseis.com.py/category/665-perecedero-frutas-y-verduras-de-frutos.aspx",
        "https://www.superseis.com.py/category/618-perecedero-carnes-pollos.aspx",
        "https://www.superseis.com.py/category/605-perecedero-carnes-carnes-a-granel.aspx",
        "https://www.superseis.com.py/Ofertas.aspx"
    ]
    
    data = []
    fecha_consulta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for url in superseis_urls:
        print(f"Procesando Superseis: {url}")
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error al conectar con {url}: {e}")
            continue
        if response.status_code != 200:
            print(f"Error al obtener {url}: {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="product-item")
        # En algunos casos, los productos pueden encontrarse con otro selector:
        if not products:
            products = soup.find_all("h2", class_="ecommercepro-loop-product__title")
        if not products:
            print(f"No se encontraron productos en {url}")
            continue
        
        for product in products:
            if product.name == "div":
                h2 = product.find("h2", class_="product-title")
                nombre = h2.get_text(strip=True) if h2 else "No encontrado"
                span = product.find("span", class_="price-label")
                precio = span.get_text(strip=True) if span else "No encontrado"
            else:
                nombre = product.get_text(strip=True)
                precio = "No encontrado"
            data.append({
                "Supermercado": "Superseis",
                "Categoría": url,
                "Producto": nombre,
                "Precio": precio,
                "FechaConsulta": fecha_consulta,
                "Grupo": "Ofertas"
            })
    return data

##############################################
# STUBS PARA OTROS SUPERMERCADOS (Ejemplo)
##############################################

def scrape_arete():
    print("Scrape de ARETE no implementado.")
    return []

def scrape_los_jardines():
    print("Scrape de LOS JARDINES no implementado.")
    return []

def scrape_salemma():
    print("Scrape de SALEMMA no implementado.")
    return []

def scrape_real():
    print("Scrape de REAL no implementado.")
    return []

def scrape_biggies():
    print("Scrape de BIGGIES no implementado.")
    return []

##############################################
# FUNCIÓN PRINCIPAL DE SCRAPING
##############################################

def main_scrape():
    """
    Combina los datos de Stock, Superseis y otros supermercados (stubs)
    y guarda el resultado en un archivo CSV con timestamp.
    """
    data = []
    data.extend(scrape_stock())
    data.extend(scrape_superseis())
    data.extend(scrape_arete())
    data.extend(scrape_los_jardines())
    data.extend(scrape_salemma())
    data.extend(scrape_real())
    data.extend(scrape_biggies())
    
    df = pd.DataFrame(data)
    
    directory = r'C:\Users\dmeza\preciossupermercados'
    filename = f"preciossupermercados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = os.path.join(directory, filename)
    try:
        df.to_csv(file_path, index=False)
        print(f"Datos guardados correctamente en {file_path}")
    except Exception as e:
        print("Error al guardar el archivo:", e)

if __name__ == "__main__":
    main_scrape()

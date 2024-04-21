import requests
import pandas as pd
import time

def obtener_ids_criptomonedas():
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    if response.status_code == 200:
        criptomonedas = response.json()
        # Tomar solo los primeros 9000 IDs
        ids = [cripto["id"] for cripto in criptomonedas[:9000]]
        return ids
    else:
        print("Error al obtener la lista de criptomonedas:", response.status_code)
        return []

def get_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?x_cg_demo_api_key=	CG-xrS6Bj6uiVqy46SL8Ha1KNML"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Verificar si la criptomoneda pertenece a una de las categorías especificadas
        categories = data.get('categories', [])
        if any(category in categories for category in ["Real World Assets (RWA)", "Meme", "Artificial Intelligence (AI)", "Gaming (GameFi)"]):

            market_data = data.get('market_data', {})
            market_cap = market_data.get('market_cap', {}).get('usd')
            # Extraer solo los datos requeridos
            required_data = {
                'Coin ID': coin_id,
                'Capitalización total de mercado (market cap)': market_cap,
                'Categorías': categories  # Agregar las categorías
            }
            return required_data
        else:
            return None
    else:
        print(f"Error al obtener los datos de la criptomoneda {coin_id}: {response.status_code}")
        return None


# Obtener los IDs de las criptomonedas
lista_ids_criptomonedas = obtener_ids_criptomonedas()

# Obtener datos de las criptomonedas que cumplen con las categorías especificadas y que existen en la API
crypto_data_list = []
crypto_count = 0

for i, coin_id in enumerate(lista_ids_criptomonedas, start=1):
    coin_data = get_coin_data(coin_id)
    if coin_data is not None:
        crypto_data_list.append(coin_data)
        crypto_count += 1
        print(f"Crypto {crypto_count}: {coin_id} agregada al CSV")
    
    # Agregar un retraso de 60 segundos cada vez que se procesan 30 coin_id
    if i % 30 == 0:
        time.sleep(60)

# Convertir el diccionario a DataFrame
df = pd.DataFrame(crypto_data_list)

# Guardar el DataFrame en un archivo CSV
df.to_csv('datasettokens.csv', index=False)

print("Proceso completado. Se agregaron", crypto_count, "criptomonedas al archivo CSV.")
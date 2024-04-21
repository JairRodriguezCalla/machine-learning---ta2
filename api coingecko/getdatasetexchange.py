import pandas as pd
import requests
import time

# Función para obtener los exchanges
def obtener_exchanges():
    url = "https://api.coingecko.com/api/v3/exchanges"
    response = requests.get(url)
    if response.status_code == 200:
        exchanges = response.json()
        return exchanges
    else:
        print("Error al obtener la lista de exchanges:", response.status_code)
        return []

# Función para obtener los datos de criptomonedas por exchange
def obtener_criptomonedas_por_exchange(exchange_id):
    url = f"https://api.coingecko.com/api/v3/exchanges/{exchange_id}?x_cg_demo_api_key=CG-xrS6Bj6uiVqy46SL8Ha1KNML"
    response = requests.get(url)
    if response.status_code == 200:
        exchange_data = response.json()
        return exchange_data.get('tickers', [])
    else:
        print(f"Error al obtener los datos del exchange {exchange_id}: {response.status_code}")
        return []

# Función para obtener el ID de la criptomoneda
def get_crypto_id(symbol):
    url = f"https://api.coingecko.com/api/v3/coins/list?x_cg_demo_api_key=CG-xrS6Bj6uiVqy46SL8Ha1KNML"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for crypto in data:
            if crypto['symbol'].lower() == symbol.lower():
                return crypto['id']
    return None

# Función para actualizar el DataFrame con los IDs de las criptomonedas
def update_crypto_ids(df):
    new_data = []
    for i, row in df.iterrows():
        crypto_id = get_crypto_id(row['Crypto ID'])
        if crypto_id:
            row['Crypto ID'] = crypto_id
            new_data.append(row)
            print(f"ID actualizado para {row['Crypto ID']}")
        else:
            print(f"No se pudo encontrar el ID para el símbolo {row['Crypto ID']}. Se omitirá esta fila.")
    new_df = pd.DataFrame(new_data, columns=df.columns)
    return new_df

# Obtener los exchanges
exchanges = obtener_exchanges()

# Obtener datos de criptomonedas por exchange
exchange_crypto_data = []
for exchange in exchanges:
    exchange_id = exchange['id']
    exchange_name = exchange['name']
    print(f"Obteniendo datos de criptomonedas para el exchange: {exchange_name}")
    tickers = obtener_criptomonedas_por_exchange(exchange_id)
    crypto_volumes = {}  # Diccionario para almacenar el volumen total de cada criptomoneda en el exchange
    for ticker in tickers:
        crypto_id = ticker['base']
        volume = ticker.get('converted_volume', {}).get('usd', 0)  # Volumen convertido a USD
        crypto_volumes[crypto_id] = crypto_volumes.get(crypto_id, 0) + volume

    # Agregar datos al DataFrame
    for crypto_id, volume in crypto_volumes.items():
        crypto_data = {
            'Exchange': exchange_name,
            'Crypto ID': crypto_id,
            'Cantidad en el Exchange (USD)': volume
        }
        exchange_crypto_data.append(crypto_data)
    time.sleep(3)  # Agregar un pequeño retardo para evitar exceder las restricciones de la API

# Convertir los datos a DataFrame
df = pd.DataFrame(exchange_crypto_data)

# Guardar el DataFrame en un archivo CSV
df.to_csv('exchange_cryptos.csv', index=False)

# Cargar el CSV en un DataFrame
df = pd.read_csv('exchange_cryptos.csv')

# Actualizar los IDs de las criptomonedas y obtener un nuevo DataFrame
new_df = update_crypto_ids(df)

# Guardar el nuevo DataFrame en un nuevo archivo CSV
new_df.to_csv('exchange_cryptos.csv', index=False)
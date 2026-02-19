from pymongo import InsertOne, mongo_client
import csv
from dotenv import load_dotenv
import os

load_dotenv()

mongo_client = mongo_client.MongoClient(os.getenv('MONGODB_URI'))
db = mongo_client[os.getenv('MONGODB_DATABASE')]
collection = db[os.getenv('COLLECTION_NAME')]

def bulk_write(collection, operations):
    if not isinstance(operations, list):
        raise ValueError("Operations must be a list of MongoDB write operations.")
    
    return collection.bulk_write(operations)
# Example usage:
# operations = [
#     InsertOne({'name': 'Alice', 'age': 30}),
#     UpdateOne({'name': 'Bob'}, {'$set': {'age': 25}}, upsert=True),
#     DeleteOne({'name': 'Charlie'})
# ]
# result = bulk_write(collection, operations)
# Hace el bulk write de las operaciones proporcionadas en la colección especificada. 
# Asegura que las operaciones sean una lista válida antes de ejecutarlas.

def read_csv(path):
    with open(path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
# Example usage:
# data = read_csv('data.csv')
# print(data)
# Lee un archivo CSV y devuelve su contenido como una lista de diccionarios, 
# donde cada diccionario representa una fila del CSV con los encabezados como claves.


def create_embeded_doc(data):
    for row in data:
        row['location'] = {
            'type': 'Point',
            'address': row['address'],
            'postcode': row['postcode'],
            'coordinates': [
                float(row['longitude']),
                float(row['latitude'])
            ]
        }
        row.pop('latitude', None)
        row.pop('longitude', None)
        row.pop('address', None)
        row.pop('postcode', None)
    return data
# Example usage:
# csv_data = read_csv('data.csv')
# parse_data = create_embeded_doc(csv_data)
# Crea un nuevo campo llamado 'location' que contiene un documento embebido con la información de ubicación, 
# y elimina los campos originales relacionados con la ubicación.

def main():
    path = input("Ingresa la ruta del archivo CSV: ")
    print(f"Leyendo el archivo CSV...")
    csv_data = read_csv(path)
    print(f"Creando documentos embebidos...")
    parse_data = create_embeded_doc(csv_data)
    #print(csv_data)
    #print(parse_data)
    print(f"Cantidad de lineas: {len(parse_data)}...")
    print(f"Subiendo los datos a MongoDB")
    DataUpload = bulk_write(collection, [InsertOne(row) for row in parse_data])
    print(DataUpload.bulk_api_result)

if __name__ == "__main__":
    main()
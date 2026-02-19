from pymongo import InsertOne, UpdateOne, UpdateMany, ReplaceOne, DeleteOne, DeleteMany
import csv

def bulk_write(collection, operations):
    """
    Perform bulk write operations on a MongoDB collection.

    :param collection: The MongoDB collection to perform the operations on.
    :param operations: A list of operations to perform. Each operation should be an instance of one of the following:
        - InsertOne(document)
        - UpdateOne(filter, update, upsert=False)
        - UpdateMany(filter, update, upsert=False)
        - ReplaceOne(filter, replacement, upsert=False)
        - DeleteOne(filter)
        - DeleteMany(filter)
    :return: The result of the bulk write operation.
    """
    if not isinstance(operations, list):
        raise ValueError("Operations must be a list of MongoDB write operations.")
    
    return collection.bulk_write(operations)
# Example usage:
# from pymongo import MongoClient   
# client = MongoClient('mongodb://localhost:27017/')
# db = client['mydatabase']
# collection = db['mycollection']
# operations = [
#     InsertOne({'name': 'Alice', 'age': 30}),
#     UpdateOne({'name': 'Bob'}, {'$set': {'age': 25}}, upsert=True),
#     DeleteOne({'name': 'Charlie'})
# ]
# result = bulk_write(collection, operations)
# print(result.bulk_api_result) 

def read_csv(path):
    """
    Read a CSV file and return its contents as a list of dictionaries.

    :param path: The file path to the CSV file.
    :return: A list of dictionaries representing the rows in the CSV file.
    """
    with open(path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]
# Example usage:
# data = read_csv('data.csv')
# print(data)

read = read_csv('test.csv')
print(read)
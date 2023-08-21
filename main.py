from sensor.configuration.mongo_db_connection import MongoDBClient

if __name__ == '__main__':
    mongodb_clint = MongoDBClient()
    print(mongodb_clint.database.list_collection_names())
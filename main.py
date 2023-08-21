# mongodb
# from sensor.configuration.mongo_db_connection import MongoDBClient

# if __name__ == '__main__':
#     mongodb_clint = MongoDBClient()
#     print(mongodb_clint.database.list_collection_names())


#for exception handling
# import sys
# from sensor.exception import SensorException

# def test_exception():
#     try:
#         x=1/0
#     except Exception as e:
#         raise SensorException(e,sys)
    
# if __name__ == '__main__':
#     try:
#         test_exception()
        
#     except Exception as e:
#         print(e)



# for logging
from sensor.logger import logging

logging.info("We have divieding by zero")
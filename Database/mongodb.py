# import
from pymongo import MongoClient
from basics.basic_utility import load_env_credentials
from pymongo.errors import  DuplicateKeyError
from typing import List
id_vector = List[float]
from bson import ObjectId


class Database:
    URI = load_env_credentials('mongodb_url')
    DATABASE = None
    @staticmethod
    def initialize():
        if Database.DATABASE is None:
            client=MongoClient(Database.URI)
            Database.DATABASE = client['Chatbot']

    @staticmethod
    def insert_agent(sid,collection_name='Embeddings'):

        agents_info = {
            'Agents': [
                {
                    'Agent_sid' : sid
                }
            ]
        }

        try:
            Database.DATABASE[collection_name].insert_one(agents_info)
        except DuplicateKeyError:
            print(f'Duplicate data detected in collection {Database.DATABASE} Skipping insertion')

    @staticmethod
    def update_agent_info(collection_name: str, time:int) -> List[str]:

        filter_dic = {'_id': ObjectId('6641b52f96f1f5e072ee1a62')}
        new_values = {"$set": {'Agents.1.time': time}}
        Database.DATABASE[collection_name].update_one(
            filter_dic, new_values
        )


        

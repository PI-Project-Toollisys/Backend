import pymongo

CONNECTION_STRING = "mongodb+srv://simpleUser:AovgIGUoYKSbpczO@cluster0.ynrb3.mongodb.net/maindb?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)

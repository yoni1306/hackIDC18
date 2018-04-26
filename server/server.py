import tornado.ioloop
import tornado.web
import json
import pymongo
import logging
import sys
from geopy.distance import geodesic
from pymongo import MongoClient
import time

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client['shoutout']
mongo_collection = mongo_db['messages']

# Global variable to hold last message ID in storage. This is ugly as hell, but should work
LAST_INSERTED_ID = 3

class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def SaveMessage(data):
    global LAST_INSERTED_ID
    # TODO save data in mongodb and return OK if succeeded
    data["timestamp"] = int(time.time())
    data["_id"] = LAST_INSERTED_ID + 1
    LAST_INSERTED_ID += 1
    return mongo_collection.insert_one(data).inserted_id

def GetMessages(latitude, longitude, radius, lastmsgid):
    messages = mongo_collection.find({"_id": {"$gt": int(lastmsgid)}})
    user_location = (latitude, longitude)
    relevant_messages = []
    
    for message in messages:
        message_location = (message["latitude"], message["longitude"])
        if message["radius"] >= geodesic(user_location, message_location).m:
            relevant_messages.append({
                "id": message["_id"], 
                "userid": message["userid"], 
                "location": {"latitude": message["latitude"], "longitude": message["longitude"]},
                "data": message["message"],
                "timestamp": message["timestamp"]})

    ret = {"lastid": LAST_INSERTED_ID, "messages": relevant_messages}
    return ret

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        command = self.get_argument("cmd", None)
        
        if (command == "getmsgs"):
            logging.info("Received get messages request")
            latitude = self.get_argument("latitude", None)
            longitude = self.get_argument("longitude", None)
            radius = self.get_argument("radius", None)
            lastmsgid = self.get_argument("lastmsgid", None)
            ret = GetMessages(latitude, longitude, radius, lastmsgid)
            self.set_status(200)
            self.write(json.dumps(ret))

    def post(self):
        command = self.get_argument("cmd", None)

        if (command == "newmsg"):
            logging.info("Received post new message request")
            data = tornado.escape.json_decode(self.request.body)
            if SaveMessage(data):
                self.set_status(200)
                self.write("")
            else:
                self.set_status(500)
                self.write("Error in saving message to database")
        

def make_app():
    return tornado.web.Application([
        (r"/", RootHandler),
        (r"/api", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    logging.info("Starting to listen on port 8888")
    tornado.ioloop.IOLoop.current().start()

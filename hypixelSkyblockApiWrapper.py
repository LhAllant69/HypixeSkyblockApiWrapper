from requests import get
from time import time as unixtime
class SkyblockApi:
    def __init__(self, key=""):
        #To make an api key, just do /api new in hypixel
        self.key = key
        if key == "":
            with open("apikey.txt") as file:
                self.key = file.read()
        #If the api limit is reached, program will wait 60 seconds before allowing a new request
        self.limitReached = [False, 0]
        
        #Base url
        self.BASE = "https://api.hypixel.net/"

    def request(self, endpoint):
        if not self.limitReached[0]:
            data = get(self.BASE + endpoint)
            if data.status_code == 429:
                self.limitReached = [True, unixtime()]
            return data.json()
        else:
            if unixtime() - self.limitReach[1] > 3:
                if get("https://api.hypixel.net/key?key={}".format(self.key)).json()["sucess"] == False:
                    self.limitReached[1] = unixtime()
                else:
                    self.limitReached[0] = False
                    return self.request(endpoint)
                return {}
            

    def get_bazaar(self):
        endpoint = "skyblock/bazaar"

        return self.request(endpoint)

    def get_auctions(self):
        endpoint = "skyblock/auctions"

        #This is used to determine the number of pages
        auctions = self.request(endpoint)
        totalPages = auctions["totalPages"]
        auctions = auctions["auctions"]
        totalAuctions = auctions["totalAuctions"]
        lastUpdated = auctions["lastUpdated"]

        for i in range(1, totalPages):
            url = "{}?key={}&page={}".format(endpoint, self.key, i)
            auctions.append(self.request(url).json()["auctions"])
        
        return {"totalPages":totalPages, "totalAuctions":totalAuctions, "lastUpdated":lastUpdated, "auctions":auctions}
    
    def get_recently_ended_auctions(self):
        endpoint = "skyblock/auctions_ended"
        return self.request(endpoint)

    def get_profile_by_player_uuid(self, uuid):
        endpoint = "skyblock/profiles"
        id = uuid.replace("-", "")
        return self.request("{}?key={}&uuid={}".format(endpoint, self.key, id))

    def get_profile_by_profile_id(self, id):
        endpoint = "skyblock/profile"
        return self.request("{}?key={}&profile={}".format(endpoint, self.key, id))

    def get_news(self):
        endpoint = "skyblock/news"
        return self.request("{}?key={}".format(endpoint, self.key))

    def get_collection_info(self):
        endpoint = "resources/skyblock/collections"
        return self.request(endpoint)

    def get_skills_info(self):
        endpoint = "resources/skyblock/skills"
        return self.request(endpoint)

    def get_items_info(self):
        endpoint = "resources/skyblock/items"
        return self.request(endpoint)

    def get_election_info(self):
        endpoint = "resources/skyblock/election"
        return self.request(endpoint)

    def get_bingo_info(self):
        endpoint = "resources/skyblock/bingo"
        return self.request(endpoint)

    def get_auction(self, type, uuid):
        endpoint = "skyblock/auction"
        
        #this function can be used to request by a player uuid, an auction uuid or a profile uuid
        a = ""
        if type == 0:
            a = "&player="
        if type == 1:
            a = "&uuid="
        if type == 2:
            a = "&profile="

        return self.request("{}?key={}{}{}".format(endpoint, self.key, a, uuid))

    def get_auction_of_a_player(self, player):
        return self.get_auction(0, player)

    def get_auction_of_a_uuid(self, uuid):
        return self.get_auction(1, uuid)
    
    def get_auction_of_a_profile(self, profile):
        return self.get_auction(2, profile)
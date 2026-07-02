import json

# print(data[0]["label_values"][4]["dict"][0]["dict"][0]["value"])
def get_reels_url():
    with open("saved_collections.json", "r", encoding = "utf-8") as f:
        data = json.load(f)
    savedReels = []
    for i in data[0]["label_values"][4]["dict"]:
        if "/reel/" in i["dict"][0]["value"]:
            savedReels.append(i["dict"][0]["value"])
    return savedReels





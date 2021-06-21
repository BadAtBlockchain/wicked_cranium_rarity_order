#!/bin/python3
import json
from datetime import datetime
import os

class CraniumResult:
    def __init__(self, name, pic, weighting, seperate_weights):
        self.name = name
        self.total_weighting = weighting
        self.seperate_weights = seperate_weights
        self.pic = pic

        num = name.split("#")[1]
        self.opensea_url = "https://opensea.io/assets/0x85f740958906b317de6ed79663012859067e745b/{}".format(num)
        self.metadata_url = "https://raw.githubusercontent.com/recklesslabs/wickedcraniums/main/{}".format(num)

    def set_rank(self, rank):
        self.rank = rank

    def json_friendly(self):
        return {
            "name" : self.name,
            "pic" : self.pic,
            "rank" : self.rank,
            "total_weight" : self.total_weighting,
            "seperate_weights" : self.seperate_weights,
            "opensea" : self.opensea_url,
            "metadata" : self.metadata_url
        }


METADATA_JSON = "metadata.json"
TRAITS_TOTALS = "traits.txt"
RESULTS_FILE = "results.json"

traits = {}
metadata = {}

results = [] # array of CraniumResult

def banner():
    print("Cranium rarity orderer!")
    print("- @badatblockchain")
    print("")

def populate_metadata():
    global metadata

    with open(METADATA_JSON, 'r') as f:
        metadata = json.load(f)

    print("[*] Loaded metadata dump")

def populate_traits_map():
    global traits
    with open(TRAITS_TOTALS) as f:
        lines = f.readlines()
        
        for index, line in enumerate(lines):
            split = line.split(":")
            trait = split[0]
            count = int(split[1].strip())
            traits[trait] = count

    print("[*] Loaded traits and their totals")

def create_final_json_obj(sorted_results):
    final_json_obj = {}

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    final_json_obj["author"] = "@badatblockchain"
    final_json_obj["date_time"] = dt_string
    final_json_obj["traits_count"] = 6
    final_json_obj["total_minted"] = 10762

    final_results = []
    for cr in sorted_results:
        final_results.append(cr.json_friendly())

    final_json_obj["ordered_results"] = final_results

    return final_json_obj

def create_results_unordered():
    global results
    for md in metadata:
        name = md["name"]
        pic = md["image"]
        total_attrib_weight = 0
        cranium_attribs_weights = {}

        for a in md["attributes"]:
            # get values from traits dump
            attribute_value = a["value"]
            weight = traits[attribute_value]

            # create our own little dictionary for final results
            cranium_attribs_weights[attribute_value] = weight

            # add currentr attrib weight to overall cranium weighting
            total_attrib_weight += weight
        
        # create and append out cranium's result
        cranium = CraniumResult(name, pic, total_attrib_weight, cranium_attribs_weights)
        results.append(cranium)

    print("[*] Total Cranium Results: {}".format(len(results)))

def patch_final_results_data(sorted_results):
    idx = 1
    for cr in sorted_results:
        cr.set_rank(idx)
        idx += 1

def write_out_results(final):
    # check if we already have a results file
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

    with open(RESULTS_FILE, 'a') as f:
        json.dump(final, f, indent = 4)

def main():
    populate_traits_map()
    populate_metadata()

    create_results_unordered()

    # sort our results
    sorted_results = sorted(results, key=lambda x: x.total_weighting)
    patch_final_results_data(sorted_results)

    final_obj = create_final_json_obj(sorted_results)
    write_out_results(final_obj)

if __name__ == "__main__": 
    banner()
    main()
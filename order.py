#!/bin/python3
import json

METADATA_JSON = "metadata.json"
TRAITS_TOTALS = "traits.txt"
RESULTS_FILE = "results.txt"

traits = {}
metadata = {}

class CraniumResult:
   def __init__(self, name, weighting):
      self.name = name
      self.weighting = weighting

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

def create_results_unordered():
    global results
    for md in metadata:
        name = md["name"]
        total_attrib_weight = 0

        for a in md["attributes"]:
            attribute_value = a["value"]
            weight = traits[attribute_value]
            total_attrib_weight += weight
        
        cranium = CraniumResult(name, total_attrib_weight)
        results.append(cranium)

    print("[*] Total Cranium Results: {}".format(len(results)))

def write_out_results(sorted_results):
    with open(RESULTS_FILE, 'a') as f:
        for cr in sorted_results:
            num = cr.name.split("#")[1]
            f.write('{} | {} | https://raw.githubusercontent.com/recklesslabs/wickedcraniums/main/{}\n'.format(
                cr.name,
                cr.weighting,
                num
            ))

def main():
    populate_traits_map()
    populate_metadata()
    create_results_unordered()

    sorted_results = sorted(results, key=lambda x: x.weighting)
    write_out_results(sorted_results)

if __name__ == "__main__": 
    banner()
    main()
import csv
import json
import os
if __name__ == "__main__":
    immo_ids = os.listdir("/Users/a2/Desktop/immo_cache")
    for i in immo_ids:
        #exists?
        _data_points = int(os.listdir(f"/Users/a2/Desktop/immo_cache/{i}")).sort()
        _first_seen = _data_points[0]
        props = json.load(f"/Users/a2/Desktop/immo_cache/{i}/{_first_seen}")
        

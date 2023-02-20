from csv import reader

def import_csv_layout(path): 
    with open(path) as level_map: 
        layout = reader(level_map, delimiter = ',')
        for row in layout: 
            print(row)

import_csv_layout('./levelSelector/Custom/Ninja Tilemaps/csv/LevelSelector._Buildings.csv')

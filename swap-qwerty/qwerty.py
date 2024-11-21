import sys
import json

def swap_keys_values(dictionary):
    swapped_dict = {value: key for key, value in dictionary.items()}
    return swapped_dict

def swap_qwerty(string, mode="qwerty-iytsuken"):
    with open(f"layouts\\{mode}.json", "r") as file:
        conf = json.loads(file.read())
    conf = {**conf, **swap_keys_values(conf)}
    
    res = ""
    for symbol in string:
        if symbol in conf.keys():
            res += conf[symbol]
        else:
            res += symbol
    return res
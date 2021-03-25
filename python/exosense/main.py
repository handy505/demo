#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import time
import requests
import random
from datetime import datetime

import exosense
from ablerex import AblerexInverterSimulator, GatewaySimulator
from meter import IlluMeterSimulator, TempMeterSimulator


def activate():
    url = 'https://m21d2g4j50cu80000.m2.exosite.io/provision/activate'
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'charset': 'utf-8' }
    data = 'id=Ablerex_010'
    response = requests.post(url, headers=headers, data=data)
    print(data)
    print(response)
    print(response.text)


token1 = 'ejrCJW7AC3Sud0c0y691bbUj7zSzT1YZqvsmu8FJ'
token2 = '3OkFwBFRDYuvfcFunfNJKAjTDNWS4sAOEpRJCoee'
token3 = '7rHUQiXsciKCZ93jdf3GsreKSnfdxLKVwY4ZfC9X'
token4 = 'ALJHgNxkyNf7FXGvyaPTmoDE2YoWFgvtfvjTRkXp'
token5 = 'bp5dZgS0ms1VA002qL24NiR7V9MIolIenMsz58c9'
token6 = 'nVVY8yGCWFTsMaVH82L5nh4kc8IWePplKAShuIbK'
token7 = 'ZGnRLjst9qdgu7xUti8DMLmh58B4mFINOsKGHvPs'
token8 = 'LDXIwnEebOXZxnL7hpFV1Fr3Jf9ATw42DK5YpQjP'
token9 = '2OIKqs26lXkSUlPvs2B9J2ZYak2PNAmygaCvUAB8'
token10 = 'abb428e4cdb1fa891c197811dd249e7c884c6cd9'

token_dict = {'Ablerex_001': token1,
              'Ablerex_002': token2,
              'Ablerex_003': token3,
              'Ablerex_004': token4,
              'Ablerex_005': token5,
              'Ablerex_006': token6,
              'Ablerex_007': token7,
              'Ablerex_008': token8,
              'Ablerex_009': token9,
              'Ablerex_010': token10,
             }

device_name_dict = {1:  'Ablerex_001',
                    2:  'Ablerex_002',
                    3:  'Ablerex_003',
                    4:  'Ablerex_004',
                    5:  'Ablerex_005',
                    6:  'Ablerex_006',
                    7:  'Ablerex_007',
                    8:  'Ablerex_008',
                    9:  'Ablerex_009',
                    10: 'Ablerex_010',
                   }

def get_token(id):
    device_name = device_name_dict.get(id)
    return token_dict.get(device_name)


def single_machine():
    inv = AblerexInverterSimulator(1)
    d = inv.create_config_io_dict()
    print(d)
    t = get_token(inv.id)
    exosense.post_config_to_exosense(d, t)

    while True:
        inv.sync_with_hardware()
        d = inv.create_record_dict()
        #print(d)
        print(d.get('HourlyKWH'))
        t = get_token(inv.id)
        exosense.post_data_to_exosence(d, t)
        time.sleep(3)


def power_station():
    inv1 = AblerexInverterSimulator(1)
    inv2 = AblerexInverterSimulator(2)
    inv3 = AblerexInverterSimulator(3)
    imeter4 = IlluMeterSimulator(4)
    tmeter5 = TempMeterSimulator(5)
    gw6 = GatewaySimulator(6, 'B827EBB62B45', '781924159')
    inv7 = AblerexInverterSimulator(7)
    inv8 = AblerexInverterSimulator(8)
    gw9 = GatewaySimulator(9, 'B827EB222222', '987654321')
    inv10 = AblerexInverterSimulator(10)
    

    devices = [inv1, inv2, inv3, imeter4, tmeter5, gw6, inv7, inv8, gw9, inv10]
    #devices = [inv1, inv2, inv3, inv7, inv8, inv10]
    #devices = [inv1]

    #send config_io
    for device in devices:
        d = device.create_config_io_dict()
        t = get_token(device.id)
        print('{} post config_io to exosense'.format(device))
        exosense.post_config_to_exosense(d, t)

    # post data_in
    while True:
        for device in devices:
            device.sync_with_hardware()
            d = device.create_record_dict()
            t = get_token(device.id)
            print('{} post data to exosense at {}'.format(device, datetime.now()))
            #print(d)
            try:
                exosense.post_data_to_exosence(d, t)
            except Exception as ex:
                print(repr(ex))

        time.sleep(60)

if __name__ == '__main__':
    #single_machine()
    power_station()


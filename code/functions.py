# Wenzel, Jennifer

import math

#util functions

# convert cm to m
def cm_to_m(l):
    return l/100

# convert cm to dm
def cm_to_dm(l):
    return l/10

# calculate basal area in m
def calc_ba(d):
    d = cm_to_m(d)
    ba = math.pi * (d/2)**2
    return ba 

#volume functions

def huber(params):
    dbh, h = params
    ba = calc_ba(dbh)
    vol = ba * h
    return round(vol, 3)

const_denzin = {'Picea': {'nh': '19+2*dbh_dm', 'vc': 0.04},
                'Pinus': {'nh': 28, 'vc': 0.03}, 
                'Fagus': {'nh': 25, 'vc': 0.03},
                'Quercus': {'nh': 24, 'vc': 0.03},
                'Betula': {'nh': 31, 'vc': 0.03}}

def get_nh(species, dbh):
    genus = species.split()[0]
    if genus != 'Picea':
        nh = const_denzin[genus]['nh']
    else:
        dbh_dm = cm_to_dm(dbh)
        nh = const_denzin[genus]['nh']
        nh = eval(nh)
    return nh

def denzin(params):
    species, dbh, h = params

    # get correct constants for species
    nh = [get_nh(s, d) for s, d in zip(species, dbh)]
    vc = species.apply(lambda s: const_denzin[s.split()[0]]['vc'])
  
    vol = (dbh**2/1000) + (dbh**2/1000) * (h-nh) * vc
    return round(vol, 3)

def form_factor(real_vol, cylinder_vol):
    return round(real_vol/cylinder_vol, 3)

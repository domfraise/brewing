

#take a starting variation of salts, calculate how much of each ion it gives

#Ca: 23%	SO4: 56%	Gypsum (CaSO4 * 2H20)
#Ca: 36%	Cl: 64%	Calcium Chloride (CaCl2)
#Mg: 20%	SO4: 80%	Epsom (MgSO4)
#Na: 39%	Cl: 61%	Table Salt (NaCl)
#Na: 27%	HCO3: 73%	Baking Soda (NaHCO3)


salts = {
    "CaSO4":  {"ca": 23, "s04": 56},
    "CaCl2":  {"ca": 36, "cl": 64},
    "MgSO4":  {"mg": 20, "s04": 80},
    "NaCl":   {"na": 39, "cl": 61},
    "NaHCO3": {"na": 27, "hc03": 73}
}

ionSources = {}
for name, parts in salts.items():
    for ion,ppm in parts.items():  
        if ionSources.get(ion) is None:
            ionSources[ion] = [name]
        else:
            ionSources[ion].append(name)

print(ionSources)

#Calcium	Magnesium	Sodium	Suphate	Chloride	Bicarbonate
desiredPpm = {"ca":70, "mg":10, "na":150,"s04":150, "cl":225, "hc03":	0}

runningTotals = {}

def getCurrentPpms(salts, runningTotals):
    ionPpms = {}
    for salt, weight in runningTotals.items():
        ions = salts.get(salt)
        print(ions)
        for ion,ppm in ions.items():
            if ionPpms.get(ion) is None:
                ionPpms[ion] = ppm * weight
            else:
                ionPpms[ion]+= ppm * weight
    return ionPpms

#check for only one source

#calculate for all ions with 1 source


for ion, sources in ionSources.items():
    if len(sources) == 1:
        print(sources)
        saltName = sources[0]
        salt = salts[saltName]
        ppmFor1g = salt[ion]
        desired = desiredPpm[ion]
        grammesOfSalt = desired/ppmFor1g
        print(salt)
        runningTotals[saltName] = grammesOfSalt

print(getCurrentPpms(salts, runningTotals))

#for ion in desiredPpm.values():
    

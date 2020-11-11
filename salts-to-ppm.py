

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

class Salts:
    def __init__(self, salts):
        self.salts = salts
        self.ionSources = self.calculateIonSources()

    def calculateIonSources(self):
        ionSources = {}
        for name, parts in self.salts.items():
            for ion,ppm in parts.items():
                if ionSources.get(ion) is None:
                    ionSources[ion] = [name]
                else:
                    ionSources[ion].append(name)

        return ionSources

ionSources = calculateIonSources(salts)

#print(ionSources)

#Calcium	Magnesium	Sodium	Suphate	Chloride	Bicarbonate
minPpms =    {"ca": 60, "mg": 10, "na": 0, "s04": 0, "cl": 0, "hc03": 0}
desiredPpm = {"ca": 70, "mg": 10, "na": 150, "s04": 150, "cl": 225, "hc03": 0}
maxPpms =    {"ca": 100, "mg": 50, "na": 150, "s04": 400, "cl": 400, "hc03": 20}

runningTotals = {}

def getCurrentPpms(salts, runningTotals):
    ionPpms = {}
    for salt, weight in runningTotals.items():
        ions = salts.get(salt)
        for ion,ppm in ions.items():
            if ionPpms.get(ion) is None:
                ionPpms[ion] = ppm * weight
            else:
                ionPpms[ion] += ppm * weight
    return ionPpms

#check for only one source

#calculate for all ions with 1 source

def calculateSaltsWithOneSource(ionSources, salts, runningTotals, desiredPpm):
    for ion, sources in ionSources.items():
        if len(sources) == 1:
            saltName = sources[0]
            #print("One source for " + ion)

            salt = salts[saltName]
            ppmFor1g = salt[ion]
            desired = desiredPpm[ion]
            grammesOfSalt = desired/ppmFor1g

            #check adding salt won't go over threshold
            currentPpms = getCurrentPpms(salts, runningTotals)

            addSalt = True
            for ion, ppm in salt.items():
                if currentPpms.get(ion) is not None and currentPpms.get(ion) + grammesOfSalt * ppm > maxPpms.get(ion):
                    addSalt = False

            if not addSalt:
                continue

            runningTotals[saltName] = grammesOfSalt
           # print("Added " + str(grammesOfSalt) + " of " + saltName)
            ionsAdded = salts[saltName].keys()
            for ion in ionsAdded:
                ionSources[ion].remove(saltName)
           # print("remainingSources: " + str(ionSources))


def initialPassDone(ionSources, runningTotal, desiredPpms, salts):
    # if any ions have sources and desired ppm not met, keep adding
    currentPpms = getCurrentPpms(salts, runningTotal)
    for ion, sources in ionSources.items():
        #print(ion, " - sources: ", sources, " ppm ", currentPpms.get(ion), " desired ", desiredPpms[ion])
        if currentPpms.get(ion) is None:
            return False
        if len(sources) > 0 and currentPpms[ion] < desiredPpms[ion]:
            return False
    return True
        # sources left and desired ppm not met

while not initialPassDone(ionSources, runningTotals, desiredPpm, salts):  
    calculateSaltsWithOneSource(ionSources, salts, runningTotals, desiredPpm)

for ion, ppm in getCurrentPpms(salts, runningTotals).items():
    print("Ion: ", ion, ", desired: ", desiredPpm[ion], ", current: ", ppm)


#print(ionSources)

#for ion in desiredPpm.values():
    

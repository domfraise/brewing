
class SaltDef:
    def __init__(self, name, ions):
        self.name = name
        self.ions = ions


class SaltConcentration:
    def __init__(self, salt_def, weight):
        self.salt_def = salt_def
        self.weight = weight

    def get_current_ppms(self):
        return self.get_ppms_for_weight(self.weight)

    def get_ppms_for_weight(self, weight_in_g):
        return {ion.name: ion.get_ppm_for_weight(weight_in_g) for ion in self.salt_def.ions}

class Ion:
    def __init__(self, name, ppmPerGramme):
        self.name = name
        self.ppmPerGramme = ppmPerGramme

    def get_ppm_for_weight(self, weight):
        return self.ppmPerGramme * weight

class SaltSolution:
    def __init__(self, salt_defs):
        self.salt_concentrations = []
        self.salt_defs = salt_defs
        self.ion_sources = self.calculateIonSources()

    def get_current_ppms(self):
        ionPpms = {}
        for concentration in self.salt_concentrations:
            salt_ppm = concentration.get_current_ppms()
            for ion, ppm in salt_ppm.items():
                if ionPpms.get(ion) is not None:
                    ionPpms[ion] += ppm
                else:
                    ionPpms[ion] = ppm
        return ionPpms

    def addSalt(self, salt_def, weight):
        for concentration in self.salt_concentrations:
            if concentration.salt_def.name is salt_def.name:
                concentration.weight += weight
                return
        self.salt_concentrations.append(SaltConcentration(salt_def, weight))

    def add_salt_for_ppm(self, ion_name, ppm_to_add):
        salt_def = salt_defs[self.ion_sources[ion_name][0]]
        for ion in salt_def.ions:
            if ion.name == ion_name:
                weight_to_add = ppm_to_add/ion.ppmPerGramme
                self.addSalt(salt_def, weight_to_add) #?
                #ion.ppm * x = ppm_add


    def calculateIonSources(self):
        ionSources = {}
        for saltDef in self.salt_defs.values():
            for ion in saltDef.ions:
                if ionSources.get(ion.name) is None:
                    ionSources[ion.name] = [saltDef.name]
                else:
                    ionSources[ion.name].append(saltDef.name)

        return ionSources

salt_defs = {"CaSO4": SaltDef("CaSO4", [Ion("ca", 23), Ion("s04", 56)]),
         "CaCl2": SaltDef("CaCl2", [Ion("ca", 36), Ion("cl", 64)]),
         "MgSO4": SaltDef("MgSO4", [Ion("mg", 20), Ion("s04", 80)]),
         "NaCl": SaltDef("NaCl", [Ion("na", 39), Ion("cl", 61)]),
         "NaHCO3": SaltDef("NaHCO3", [Ion("na", 27), Ion("hc03", 73)])}




soln = SaltSolution(salt_defs)

soln.add_salt_for_ppm('ca', 30)
soln.add_salt_for_ppm('cl', 70)

print([(x.salt_def.name, x.weight) for x in soln.salt_concentrations])
print(soln.get_current_ppms())
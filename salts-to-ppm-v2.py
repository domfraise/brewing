
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

class MaxRestriction:
    def __init__(self, ion_name, max_ppm):
        self.ion_name = ion_name
        self.max_ppm = max_ppm

    def violates_restriction(self, salt_solution):
        ppm_for_ion = salt_solution.get_current_ppms_for_ion(self.ion_name)
        if ppm_for_ion > self.max_ppm:
            return True
        else:
            return False


class MinRestriction:
    def __init__(self, ion_name, min_ppm):
        self.ion_name = ion_name
        self.min_ppm = min_ppm

    def violates_restriction(self, salt_solution):
        ppm_for_ion = salt_solution.get_current_ppms_for_ion(self.ion_name)
        if ppm_for_ion < self.min_ppm:
            return True
        else:
            return False


class SaltSolution:
    def __init__(self, salt_defs, max_restrictions, min_restrictions):
        self.salt_concentrations = []
        self.salt_defs = salt_defs
        self.max_restrictions = max_restrictions
        self.min_restrictions = min_restrictions
        self.ion_sources = self.calculateIonSources()
        self.set_min_restrictions()

    def set_min_restrictions(self):
        for restriction in self.min_restrictions:
            if self.get_current_ppms_for_ion(restriction.ion_name) < restriction.min_ppm:
                self.set_ppm_for_ion(restriction.ion_name, restriction.min_ppm)

    def solution_is_valid(self):
        for restriction in max_restrictions:
            if restriction.violates_restriction(self):
                return False
        return True

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

    def get_current_salt_weights(self):
        salt_weights = {}
        for concentration in self.salt_concentrations:
            salt_weights[concentration.salt_def.name] = concentration.weight
        return salt_weights

    def get_current_ppms_for_ion(self, ion_name):
        ppms = self.get_current_ppms().get(ion_name)
        if ppms is None:
            return 0
        return ppms

    def addSalt(self, salt_def, weight):
        for concentration in self.salt_concentrations:
            if concentration.salt_def.name is salt_def.name:
                concentration.weight += weight
                return
        self.salt_concentrations.append(SaltConcentration(salt_def, weight))

    def remove_salt(self, salt_def, weight):
        for concentration in self.salt_concentrations:
            if concentration.salt_def.name is salt_def.name:
                concentration.weight -= weight
                if concentration.weight <= 0:
                    self.salt_concentrations.remove(concentration)

    def add_salt_for_ppm(self, ion_name, ppm_to_add):
        for salt_name in self.ion_sources[ion_name]:
            weight_aded = self.add_ppm_from_specific_source(ion_name, ppm_to_add, self.salt_defs.get(salt_name))
            if weight_aded == 0:
                break


    def remove_salt_for_ppm(self, ion_name, ppm_to_remove):
        for salt_name in self.ion_sources[ion_name]:
            weight_removed = self.remove_ppm_from_specific_source(ion_name, ppm_to_remove, self.salt_defs.get(salt_name))
            if weight_removed > 0:
                break

    def add_ppm_from_specific_source(self, ion_name, ppm_to_add, salt_def):
        weight_to_add = 0
        for ion in salt_def.ions:
            if ion.name == ion_name:
                weight_to_add = ppm_to_add / ion.ppmPerGramme
                self.addSalt(salt_def, weight_to_add)  # ?
                if not self.solution_is_valid():
                    self.remove_salt(salt_def, weight_to_add)
                weight_to_add = 0

        return weight_to_add

    def remove_ppm_from_specific_source(self, ion_name, ppm_to_remove, salt_def):
        weight_to_remove = 0
        for ion in salt_def.ions:
            if ion.name == ion_name:
                weight_to_remove = ppm_to_remove / ion.ppmPerGramme
                self.remove_salt(salt_def, weight_to_remove)  # ?
                if not self.solution_is_valid():
                    self.addSalt(salt_def, weight_to_remove)
                weight_to_remove = 0

        return weight_to_remove

    def set_ppm_for_ion(self, ion_name, desired_ppm):
        current_ppm = self.get_current_ppms_for_ion(ion_name)
        if current_ppm < desired_ppm:
            self.add_salt_for_ppm(ion_name, desired_ppm - current_ppm)
        if current_ppm > desired_ppm:
            self.remove_salt_for_ppm(ion_name, current_ppm - desired_ppm)

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


max_restrictions = [
    MaxRestriction("ca", 100),
    MaxRestriction("mg", 50),
    MaxRestriction("na", 150),
    MaxRestriction("s04", 400),
    MaxRestriction("cl", 400),
    MaxRestriction("hc03", 20)]

min_restrictions = [
    MinRestriction("ca", 60),
    MinRestriction("mg", 10),
    MinRestriction("na", 0),
    MinRestriction("s04", 0),
    MinRestriction("cl", 0),
    MinRestriction("hc03", 0)
]

desired_ppms = {
    "cl": 225,
    "s04": 150,
    "ca": 70,
    "mg": 40,
    "na": 150,
    "hc03": 0
}
soln = SaltSolution(salt_defs, max_restrictions, min_restrictions)

for ion, ppm in reversed(desired_ppms.items()):
    soln.set_ppm_for_ion(ion, ppm)

print(soln.get_current_salt_weights())

final_ppms = soln.get_current_ppms()
for ion, desired_ppm in desired_ppms.items():
    print(ion, " desired = ", desired_ppm, " actual = ", final_ppms.get(ion))

print(final_ppms)
from guietta import Gui, HSeparator, ___

class SaltDef:
    def __init__(self, name, ions):
        self.name = name
        self.ions = ions


class SaltConcentration:
    def __init__(self, salt_def, weight):
        self.salt_def = salt_def
        self.weight = weight
        self.litres_of_water = 10

    def get_current_ppms(self):
        return self.get_ppms_for_weight(self.weight)

    def get_ppms_for_weight(self, weight_in_g):
        return {ion.name: ion.get_ppm_for_weight(weight_in_g) for ion in self.salt_def.ions}

class Ion:
    def __init__(self, name, ppmPerGrammePer10L):
        self.name = name
        self.ppmPerGrammePer10L = ppmPerGrammePer10L

    def get_ppm_for_weight(self, weight):
        return self.ppmPerGrammePer10L * weight

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
    def __init__(self, salt_defs, max_restrictions, min_restrictions, desired_ppms, ion_rankings):
        self.salt_concentrations = []
        self.salt_defs = salt_defs
        self.max_restrictions = max_restrictions
        self.min_restrictions = min_restrictions
        self.desired_ppms = desired_ppms
        self.ion_rankings = ion_rankings
        self.ion_sources = self.calculateIonSources()
        self.min_restrictions_set = False
        # self.set_min_restrictions()

    def get_litres_of_water(self):
        total = 0
        for concentration in self.salt_concentrations:
            total += concentration.litres_of_water
        return total

    def get_heuristic(self):
        score = 0
        if not self.solution_is_valid():
            score = -1000000
        current_ppms = self.get_current_ppms()
        for ion, current_ppm in current_ppms.items():
            ppm_delta = (abs(self.desired_ppms.get(ion) - current_ppm))
            # print("delta: ", ion, ppm_delta)

            closeness_score = -ppm_delta

            #higher is better
            ion_score = closeness_score * self.ion_rankings.get(ion) #should this not be divide? a high multiplier should give a higher score
            score += ion_score
            # print("ion score", ion, ion_score)

        return score

    def set_min_restrictions(self):
        print("-- Adding for Min Restrictions --")
        for restriction in self.min_restrictions.values():
            if self.get_current_ppms_for_ion(restriction.ion_name) < restriction.min_ppm:
                success = self.set_ppm_for_ion(restriction.ion_name, restriction.min_ppm)
                if not success:
                    raise Exception('Cannot set restriction ', restriction, " without violating other restrictions")
        print("--- Min restrictions set up ---")
        self.min_restrictions_set = True

    def solution_is_valid(self):
        for restriction in self.max_restrictions.values():
            if restriction.violates_restriction(self):
                return False
        for restriction in self.min_restrictions.values():
            if self.min_restrictions_set and restriction.violates_restriction(self):
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
                # print("Added ", salt_deef.name, " weight ", weight)
                return weight
        self.salt_concentrations.append(SaltConcentration(salt_def, weight))
        return weight
        # print("Added ", salt_def.name, " weight ", weight)


    def remove_salt(self, salt_def, weight):
        for concentration in self.salt_concentrations:
            if concentration.salt_def.name is salt_def.name:
                current_weight = concentration.weight
                concentration.weight -= weight
                if concentration.weight <= 0:
                    self.salt_concentrations.remove(concentration)
                    return current_weight
                else:
                    return weight
        return 0
        # print("Removed ", salt_def.name, " weight ", weight)


    def add_salt_for_ppm(self, ion_name, ppm_to_add):
        for salt_name in self.ion_sources[ion_name]:
            success = self.add_ppm_from_specific_source(ion_name, ppm_to_add, self.salt_defs.get(salt_name))
            if success:
                return success
        return False


    def remove_salt_for_ppm(self, ion_name, ppm_to_remove):
        for salt_name in self.ion_sources[ion_name]:
            success = self.remove_ppm_from_specific_source(ion_name, ppm_to_remove, self.salt_defs.get(salt_name))
            if success:
                return success

    def add_ppm_from_specific_source(self, ion_name, ppm_to_add, salt_def):
        success = False
        for ion in salt_def.ions:
            if ion.name == ion_name:
                weight_to_add = ppm_to_add / ion.ppmPerGrammePer10L
                self.addSalt(salt_def, weight_to_add)  # ?
                if not self.solution_is_valid():
                    self.remove_salt(salt_def, weight_to_add)
                else:
                    success = True
                break


        return success

    def remove_ppm_from_specific_source(self, ion_name, ppm_to_remove, salt_def):
        success = False
        for ion in salt_def.ions:
            if ion.name == ion_name:
                weight_to_remove = ppm_to_remove / ion.ppmPerGrammePer10L
                self.remove_salt(salt_def, weight_to_remove)  # ?
                if not self.solution_is_valid():
                    self.addSalt(salt_def, weight_to_remove)
                else:
                    success = True
                break

        return success

    def set_ppm_for_ion(self, ion_name, desired_ppm):
        current_ppm = self.get_current_ppms_for_ion(ion_name)

        if current_ppm < desired_ppm:
            return self.add_salt_for_ppm(ion_name, desired_ppm - current_ppm)
        if current_ppm > desired_ppm:
            return self.remove_salt_for_ppm(ion_name, current_ppm - desired_ppm)
        return True

    def calculateIonSources(self):
        ionSources = {}
        for saltDef in self.salt_defs.values():
            for ion in saltDef.ions:
                if ionSources.get(ion.name) is None:
                    ionSources[ion.name] = [saltDef.name]
                else:
                    ionSources[ion.name].append(saltDef.name)

        return ionSources


class SolutionOptimiser:
    # def __init__(self, salt_defs, max_restrictions, min_restrictions, desired_ppms, ion_rankings):
    #     self.desired_ppms = desired_ppms
    #     self.min_restrictions = min_restrictions
    #     self.max_restrictions = max_restrictions
    #     self.salt_defs = salt_defs
    #     self.ion_rankings = ion_rankings
    #     self.soln = SaltSolution(salt_defs, max_restrictions, min_restrictions, desired_ppms, ion_ranking)
    #     # self.best_concentrations = self.soln.get_current_salt_weights()
    #     self.optimisation_delta = 0.1

    def __init__(self, salt_defs, ion_configs):
        self.desired_ppms = ion_configs.get_desired_ppms()
        self.min_restrictions = ion_configs.get_min_restrictions()
        self.max_restrictions = ion_configs.get_max_restrictions()
        self.salt_defs = salt_defs
        self.ion_rankings = ion_configs.get_ion_rankings()
        self.soln = SaltSolution(salt_defs, self.max_restrictions, self.min_restrictions, self.desired_ppms, self.ion_rankings)
        # self.best_concentrations = self.soln.get_current_salt_weights()
        self.optimisation_delta = 0.1

    def set_ppms_for_desired(self):
        for ion, ppm in reversed(self.desired_ppms.items()):
            print("--- Setting ", ion, " to ", ppm, " ppm ---")
            success = self.soln.set_ppm_for_ion(ion, ppm)
            if not success:
                print("failed to set ", ion, " to ", ppm, " ppm without violating restrictions")
            print("New PPM's", self.soln.get_current_ppms())
            print("New Salt Content", self.soln.get_current_salt_weights())
        self.current_score = self.soln.get_heuristic()

    def optimise_for_salt(self, salt_def):
        current_score = self.soln.get_heuristic()
        # print(current_score)

        weight_added = self.soln.addSalt(salt_def, self.optimisation_delta)
        increase_score = self.soln.get_heuristic()
        self.soln.remove_salt(salt_def, weight_added)

        weight_removed = self.soln.remove_salt(salt_def, self.optimisation_delta)
        decrease_score = self.soln.get_heuristic()
        self.soln.addSalt(salt_def, weight_removed)

        #base case - at local max or platau
        if current_score >= increase_score and current_score >= decrease_score:
            # print(salt_def.name, " peak:", decrease_score, current_score, increase_score)

            return

        if increase_score > current_score:
            # print(decrease_score, current_score, increase_score)
            # print("increase")

            self.soln.addSalt(salt_def, self.optimisation_delta)
            self.optimise_for_salt(salt_def)
        elif decrease_score > current_score:
            # print("decrease")
            # print(decrease_score, current_score, increase_score)

            self.soln.remove_salt(salt_def, self.optimisation_delta)
            self.optimise_for_salt(salt_def)
        else:

            print("no perfect peak found")
            print(decrease_score, current_score, increase_score)
            return

    def optimise_for_all_salts(self):
        for salt, salt_def in self.salt_defs.items():
            # print("Optimising ", salt_def.name)
            self.optimise_for_salt(salt_def)
            # print(self.soln.get_heuristic())

class IonConfig:
    def __init__(self, ion_name, min_ppm, desired_ppm, max_ppm, priority_multiplier):
        self.ion_name = ion_name
        self.min_ppm = min_ppm
        self.desired_ppm = desired_ppm
        self.max_ppm = max_ppm
        self.priority_multiplier = priority_multiplier

class IonConfigs:
    def __init__(self, ion_configs):
        self.ion_configs = ion_configs

    def get_max_restrictions(self):
        return {ion_config.ion_name: MaxRestriction(ion_config.ion_name, ion_config.max_ppm) for ion_config in self.ion_configs}

    def get_min_restrictions(self):
        return {ion_config.ion_name: MinRestriction(ion_config.ion_name, ion_config.min_ppm) for ion_config in self.ion_configs}

    def get_desired_ppms(self):
        return {ion_config.ion_name: ion_config.desired_ppm for ion_config in self.ion_configs}

    def get_ion_rankings(self):
        return {ion_config.ion_name: ion_config.priority_multiplier for ion_config in self.ion_configs}

class GuiModel:
    def __init__(self, salt_defs, ion_configs):
        self.ion_configs = ion_configs
        self.salt_defs = salt_defs
        self.salts_weights = {}

    def get_salts_view(self):
        salts_view = []
        max_columns = 0
        for salt_def in self.salt_defs.values():
            salt_view = []
            salt_view.append(salt_def.name)
            for ion in salt_def.ions:
                salt_view.append("%s: %s" % (ion.name, ion.ppmPerGrammePer10L))
            if len(salt_view) > max_columns:
                max_columns = len(salt_view)
            salts_view.append(salt_view)
        header_row = ["Salt"]
        for i in range(0, max_columns - 1):
            header_row.append("Ion: PPM for 1g in 10L")
        salts_view.insert(0, header_row)
        return salts_view

    def get_ion_config_view(self):
        ion_config_rows = [["Ion", "Min", "Desired", "Max", "Multiplier", "Actual"]]
        for ion_config in self.ion_configs:
            row = [ion_config.ion_name,
                   "__%smin__" % ion_config.ion_name,
                   "__%sdesired__" % ion_config.ion_name,
                   "__%smax__" % ion_config.ion_name,
                   "__%smul__" % ion_config.ion_name,
                   ("", '%sactual' % ion_config.ion_name),
                   ]
            ion_config_rows.append(row)

        return ion_config_rows


    def set_salts_view(self, current_salt_weights):
        for salt, weight in current_salt_weights.items():
            gui.widgets['%sweight' % salt].setText(str(weight))

    def get_salt_weights_view(self):
        salt_rows = [['Salt'], ['Weight (g)']]
        for salt in self.salt_defs.keys():
            salt_rows[0].append(salt)
            salt_rows[1].append(("0", '%sweight' % salt))
            # row = [salt, ("0", '%sweight' % salt)]
            # salt_rows.append(row)
        return salt_rows

    def get_rows(self):
        all_rows = []
        configs = self.get_ion_config_view()

        all_rows.append(['<center>Configs</center>'],)
        all_rows.append([HSeparator],)
        all_rows.extend(configs)

        all_rows.append([(['Calculate'], "calculate")])
        all_rows.append([HSeparator])
        all_rows.append(['<center>Salts in 10L</center>'],)
        all_rows.extend(self.get_salt_weights_view())

        max_columns = 0
        for row in all_rows:
            if len(row) > max_columns:
                max_columns = len(row)

        for row in all_rows:
            if len(row) < max_columns:
                columns_to_add = max_columns - len(row)
                for i in range(0, columns_to_add):
                    row.append(___)


        return all_rows

    def populate_config_fields(self, gui):
        for ion_config in self.ion_configs:
            gui.widgets['%smin' % ion_config.ion_name].setText(str(ion_config.min_ppm))
            gui.widgets['%sdesired' % ion_config.ion_name].setText(str(ion_config.desired_ppm))
            gui.widgets['%smax' % ion_config.ion_name].setText(str(ion_config.max_ppm))
            gui.widgets['%smul' % ion_config.ion_name].setText(str(ion_config.priority_multiplier))

    def set_ion_configs(self, gui):
        for ion_config in self.ion_configs:
            ion_config.min_ppm = float(gui.widgets['%smin' % ion_config.ion_name].text())
            ion_config.desired_ppm = float(gui.widgets['%sdesired' % ion_config.ion_name].text())
            ion_config.max_ppm = float(gui.widgets['%smax' % ion_config.ion_name].text())
            ion_config.priority_multiplier = float(gui.widgets['%smul' % ion_config.ion_name].text())

    def set_actual_ppms(self, gui, ppms):
        for ion_name, ppm in ppms.items():
            gui.widgets['%sactual' % ion_name].setText(str(ppm))
#
def calulate(gui, *args):
    salt_gui_config.set_ion_configs(gui)
    soltion_optimiser = SolutionOptimiser(salt_defs, IonConfigs(salt_gui_config.ion_configs))
    soltion_optimiser.set_ppms_for_desired()
    soltion_optimiser.optimise_for_all_salts()
    salt_gui_config.set_actual_ppms(gui, soltion_optimiser.soln.get_current_ppms())
    salt_gui_config.set_salts_view(soltion_optimiser.soln.get_current_salt_weights())


salt_defs = {
    "CaCl2": SaltDef("CaCl2", [Ion("ca", 36), Ion("cl", 64)]),
    "MgSO4": SaltDef("MgSO4", [Ion("mg", 20), Ion("s04", 80)]),
    "NaCl": SaltDef("NaCl", [Ion("na", 39), Ion("cl", 61)]),
    "NaHCO3": SaltDef("NaHCO3", [Ion("na", 27), Ion("hc03", 73)]),
    "CaSO4": SaltDef("CaSO4", [Ion("ca", 23), Ion("s04", 56)]),
}


ion_configs = [
    IonConfig('cl', 202, 212, 222, 1),
    IonConfig('s04', 145, 155, 165, 1),
    IonConfig('ca', 58, 68, 78, 1),
    IonConfig('mg', 20, 30, 40, 1),
    IonConfig('na', 50, 60, 70, 1),
    IonConfig('hc03', 0, 5, 35, 1),
]
salt_gui_config = GuiModel(salt_defs, ion_configs)


gui = Gui(*salt_gui_config.get_rows())

gui.calculate = calulate
# gui = Gui(['hi'])
salt_gui_config.populate_config_fields(gui)




gui.run()

from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III

from salts_to_ppm import *

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

        all_rows.append([['Calculate']])
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
salt_gui_config.populate_config_fields(gui)


with gui.Calculate:
    salt_gui_config.set_ion_configs(gui)
    soltion_optimiser = SolutionOptimiser(salt_defs, IonConfigs(salt_gui_config.ion_configs))
    soltion_optimiser.set_ppms_for_desired()
    soltion_optimiser.optimise_for_all_salts()
    salt_gui_config.set_actual_ppms(gui, soltion_optimiser.soln.get_current_ppms())
    salt_gui_config.set_salts_view(soltion_optimiser.soln.get_current_salt_weights())

gui.run()

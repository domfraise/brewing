from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III

from salts_to_ppm import *

class SaltGui:
    def __init__(self, salt_defs, ion_configs):
        self.ion_configs = ion_configs
        self.salt_defs = salt_defs
        self.gui = Gui(*self.get_rows())
        self.populate_config_fields()

    def get_salts_view(self):
        salts_view = []
        max_columns = 0
        for salt_def in self.salt_defs:
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
        ion_config_rows = []
        for ion_config in self.ion_configs:
            row = [ion_config.ion_name,
                   "Min:", "__%smin__" % ion_config.ion_name,
                   "Desired:", "__%sdesired__" % ion_config.ion_name,
                   "Max:", "__%smax__" % ion_config.ion_name,
                   "Multiplier:", "__%smul__" % ion_config.ion_name]
            ion_config_rows.append(row)

        return ion_config_rows

    #     ["ion1", "Min", "__ion1min__", "Desired", "__ion1desired__", "Max", "__ion1max__", "Multiplier", "__ion1multiplier__"],


    def get_rows(self):
        all_rows = []
        salts= self.get_salts_view()
        configs= self.get_ion_config_view()

        all_rows.append(['<center>Salt Definitions</center>'],)
        all_rows.extend(salts)
        all_rows.append([HSeparator],)
        all_rows.append(['<center>Configs</center>'],)
        all_rows.extend(configs)

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

    def populate_config_fields(self):
        for ion_config in self.ion_configs:
            self.gui.widgets['%smin' % ion_config.ion_name].setText(str(ion_config.min_ppm))
            self.gui.widgets['%sdesired' % ion_config.ion_name].setText(str(ion_config.desired_ppm))
            self.gui.widgets['%smax' % ion_config.ion_name].setText(str(ion_config.max_ppm))
            self.gui.widgets['%smul' % ion_config.ion_name].setText(str(ion_config.priority_multiplier))


    def run_gui(self):
        self.gui.run()

salt_defs = [
    SaltDef("CaSO4", [Ion("ca", 23), Ion("s04", 56)]),
    SaltDef("CaCl2", [Ion("ca", 36), Ion("cl", 64)]),
    SaltDef("MgSO4", [Ion("mg", 20), Ion("s04", 80)]),
    SaltDef("NaCl", [Ion("na", 39), Ion("cl", 61)]),
    SaltDef("NaHCO3", [Ion("na", 27), Ion("hc03", 73)]),
]

ion_configs = [
    IonConfig('ca', 0, 5, 500, 0.8),
    IonConfig('mg', 0, 5, 500, 0.8),
    IonConfig('s04', 0, 5, 500, 0.8),
    IonConfig('cl', 0, 5, 500, 0.8),
    IonConfig('na', 0, 5, 500, 0.8),
    IonConfig('hc03', 0, 5, 500, 0.8),
]

salt_gui = SaltGui(salt_defs, ion_configs)
salt_gui.run_gui()
# salts = [
#     ["salt name",_ ,_ , "ion 1", '23',_ , "ion 2", '32', _],
#     ["salt name2",_ ,_ , "ion 3", '45',_ , "ion 4", '54', _]
# ]
#
# ion1min = 4
#
# config = [
#     ["ion1", "Min", "__ion1min__", "Desired", "__ion1desired__", "Max", "__ion1max__", "Multiplier", "__ion1multiplier__"],
#     ["ion2", "Min", "__ion2min__", "Desired", "__ion2desired__", "Max", "__ion2max__", "Multiplier", "__ion2multiplier__"],
# ]
#
# rows = [
#     ['<center>Calculate Salts</center>'],
#     [HSeparator],
#     ['Salt Definitions'],
#     [HSeparator]
# ]
#
# rows[3:3] = salts
# rows[6:6] = config
#
# gui = Gui(*rows)
#
# gui.widgets['ion1min'].setText('4')

    # [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
    # [  _         ,     ['button']    , B('another button') ,     III      ],
    # [ '__edit__' ,  E('an edit box') , _                   ,   VSeparator ],
    # [   Quit     ,        Ok         , Cancel              ,     III      ],
    # [    Yes     ,        No         , _                   ,     III      ],
    # [  HS('slider2'),    ___         , ___                 ,      _       ]


# with gui.Calculate:
#     gui.result = float(gui.a) + float(gui.b)

# gui.run()

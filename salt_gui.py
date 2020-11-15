from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III

from salts_to_ppm import *

salts = [
    ["salt name",_ ,_ , "ion 1", '23',_ , "ion 2", '32', _],
    ["salt name2",_ ,_ , "ion 3", '45',_ , "ion 4", '54', _]
]

ion1min = 4

config = [
    ["ion1", "Min", "__ion1min__", "Desired", "__ion1desired__", "Max", "__ion1max__", "Multiplier", "__ion1multiplier__"],
    ["ion2", "Min", "__ion2min__", "Desired", "__ion2desired__", "Max", "__ion2max__", "Multiplier", "__ion2multiplier__"],
]

rows = [
    ['<center>Calculate Salts</center>'],
    [HSeparator],
    ['Salt Definitions'],
    [HSeparator]
]

rows[3:3] = salts
rows[6:6] = config

gui = Gui(*rows)

gui.widgets['ion1min'].setText('4')

    # [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
    # [  _         ,     ['button']    , B('another button') ,     III      ],
    # [ '__edit__' ,  E('an edit box') , _                   ,   VSeparator ],
    # [   Quit     ,        Ok         , Cancel              ,     III      ],
    # [    Yes     ,        No         , _                   ,     III      ],
    # [  HS('slider2'),    ___         , ___                 ,      _       ]


# with gui.Calculate:
#     gui.result = float(gui.a) + float(gui.b)

gui.run()

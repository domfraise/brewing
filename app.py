import flask
from flask import Flask, request
import json
from Models import IonConfig, SaltDef, Ion, SolutionOptimiser, IonConfigs

app = Flask(__name__)

salt_defs = {
    "CaCl2": SaltDef("CaCl2", [Ion("ca", 36), Ion("cl", 64)]),
    "MgSO4": SaltDef("MgSO4", [Ion("mg", 20), Ion("s04", 80)]),
    "NaCl": SaltDef("NaCl", [Ion("na", 39), Ion("cl", 61)]),
    "NaHCO3": SaltDef("NaHCO3", [Ion("na", 27), Ion("hc03", 73)]),
    "CaSO4": SaltDef("CaSO4", [Ion("ca", 23), Ion("s04", 56)]),
}

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/calculate", methods=['POST'])
def calculate():
    ions_json = json.loads(request.data)
    print()
    ions = IonConfigs([IonConfig(ion["ion"], ion["desired"], ion["multiplyer"], ion["plusminus"]) for ion in ions_json])
    optimiser = SolutionOptimiser(salt_defs, ions)
    optimiser.set_ppms_for_desired()
    optimiser.optimise_for_all_salts()

    response = flask.jsonify({"ppms": optimiser.soln.get_current_ppms(),
            "weights": optimiser.soln.get_current_salt_weights()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
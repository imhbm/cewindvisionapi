from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

# Load wind turbine data from JSON file
with open("wind_turbine_data_updated.json", "r") as file:
    wind_turbine_data = json.load(file)


@app.route("/")
def home():
    return "Wind Turbine API"


@app.route("/wind_turbines")
def get_wind_turbines():
    return jsonify(wind_turbine_data)


@app.route("/power_curve/<turbine_id>")
def get_power_curve(turbine_id):
    # Find the turbine with the given ID
    turbine = next((t for t in wind_turbine_data["windTurbines"] if t["id"] == turbine_id), None)

    if turbine:
        power_curve = turbine["powerCurve"]
        return jsonify(power_curve)

    return jsonify({"error": f"Turbine with ID {turbine_id} not found."}), 404


@app.route("/comparison/<turbine_id>")
def get_comparison(turbine_id):
    # Find the turbine with the given ID
    turbine = next((t for t in wind_turbine_data["windTurbines"] if t["id"] == turbine_id), None)

    if turbine:
        comparison = turbine["comparison"]
        turbine_values = turbine.copy()
        turbine_values.pop("comparison")
        comparison["windTurbine"] = turbine_values
        return jsonify(comparison)

    return jsonify({"error": f"Turbine with ID {turbine_id} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)

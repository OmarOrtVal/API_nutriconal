from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=ZyF1kwwWLBGFOnl8YfMUVN9n0aYSxJN1OXrOopLp"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form.get('food_name')

    if not nombre:
        flash("Debes ingresar un nombre de alimento.", "error")
        return redirect(url_for('index'))

    url_completa = f"{API_URL}&query={nombre}&pageSize=1"

    respuesta = requests.get(url_completa)
    

    if respuesta.status_code != 200:
        flash("Error al conectar con la API USDA.", "error")
        return redirect(url_for('index'))

    data = respuesta.json()

    if "foods" not in data or len(data["foods"]) == 0:
        flash("No se encontró información para ese alimento.", "error")
        return redirect(url_for('index'))

    food = data["foods"][0]

    alimento = {
        "descripcion": food.get("description", "Sin descripción"),
        "marca": food.get("brandOwner", "Desconocida"),
        "categoria": food.get("foodCategory", "No especificada"),
        "nutrientes": []
    }

    for n in food.get("foodNutrients", []):
        nombre_nut = n.get("nutrientName", "")
        cantidad = n.get("value", "")
        unidad = n.get("unitName", "")
        alimento["nutrientes"].append(f"{nombre_nut}: {cantidad} {unidad}")

    return render_template("resultado.html", alimento=alimento)


if __name__ == '__main__':
    app.run(debug=True)

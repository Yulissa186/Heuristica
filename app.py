from flask import Flask, render_template, request, jsonify
from arbol import Nodo

app = Flask(__name__)

def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    dato_padre = nodo_padre.get_datos()
    dato_hijo = nodo_hijo.get_datos()

    for n in range(1, len(dato_padre)):
        if dato_padre[n] > dato_padre[n-1]:
            calidad_padre += 1
        if dato_hijo[n] > dato_hijo[n-1]:
            calidad_hijo += 1

    return calidad_hijo >= calidad_padre


def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())

    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato = nodo_inicial.get_datos()

    hijos = [
        Nodo([dato[1], dato[0], dato[2], dato[3]]),
        Nodo([dato[0], dato[2], dato[1], dato[3]]),
        Nodo([dato[0], dato[1], dato[3], dato[2]])
    ]

    nodo_inicial.set_hijos(hijos)

    for hijo in hijos:
        if hijo.get_datos() not in visitados and mejora(nodo_inicial, hijo):
            hijo.set_padre(nodo_inicial)
            sol = buscar_solucion_heuristica(hijo, solucion, visitados)
            if sol:
                return sol

    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resolver", methods=["POST"])
def resolver():
    data = request.json

    estado_inicial = list(map(int, data["inicio"].split(",")))
    solucion = list(map(int, data["final"].split(",")))

    visitados = []
    nodo_inicial = Nodo(estado_inicial)

    nodo = buscar_solucion_heuristica(nodo_inicial, solucion, visitados)

    if nodo is None:
        return jsonify({"error": "No se encontró solución"})

    resultado = []
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    



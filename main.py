from flask import Flask, jsonify, request
from data.car_details import cars
import json


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET"])
def homepage():
    return "<h1>API Running</h1"


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


# A route to return all of the available entries in our catalog.
@app.route("/api/v1/resources/cars/all", methods=["GET"])
def api_all():
    return jsonify(cars)


# Route to filter a Car using the License Plate.
@app.route("/api/v1/resources/cars", methods=["GET", "POST", "PUT", "DELETE"])
def api_car():
    if request.method == "GET":
        if len(request.args) == 0:
            return api_all()
        else:
            list_results = []

            for car in cars:
                found = True
                for key in request.args.keys():
                    # print(car[key])
                    # print(request.args[key])
                    if car[key] == request.args[key]:
                        continue
                    else:
                        found = False
                        break

                if found:
                    list_results.append(car)

            return jsonify(list_results)

    if request.method == "POST":
        license_plate = request.get_json()["license_plate"]

        for car in cars:
            if car["license_plate"] == license_plate:
                return "The Car already exists."
        cars.append(request.get_json())

        dump_data(cars)

        return "POST Registered"

    if request.method == "PUT":
        license_plate = request.args["license_plate"]

        for car in cars:
            if car["license_plate"] == license_plate:
                for key in request.args.keys():
                    if key is None:
                        print("The " + key + " is Null!")
                        continue
                    else:
                        car[key] = request.args[key]
                dump_data(cars)
                return "Updated"

        return "Please inform a valid license-plate!"

    if request.method == "DELETE":
        if "license_plate" in request.args:
            license_plate = request.args["license_plate"]
        else:
            return "Error: No License Plate field provided. Please specify the value. (/cars?license_plate=something)"

        for index in range(len(cars)):
            if cars[index]["license_plate"] == license_plate:
                cars.pop(index)
                dump_data(cars)
                return "The Car with License Plate: " + license_plate + " was Deleted"
        return "This license plate have not been found."


def dump_data(data):
    with open("data/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app.run()

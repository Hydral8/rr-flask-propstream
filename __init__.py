from flask import Flask, abort, redirect, url_for, request, jsonify, Response
from .errors import InvalidRequest
from .request_utils import propstream_req
import json

app = Flask(__name__)

def add_errors(msg, errors):
    msg += ("\n" + "-" * 50)
    for error in errors:
        msg += f"\n -{error}"
    msg += ("\n" + "-" * 50)
    return msg


@app.errorhandler(Exception)
def handle_invalid_data(error):
    # just regular exception with a message. No error.msg or anything, the error HAS a value of msg.
    resp = jsonify({"msg": str(error)})
    resp.status_code = 400
    return resp

@app.errorhandler(InvalidRequest)
def handle_invalid_req(error):
    resp = jsonify(error.to_dict())
    resp.status_code = error.status_code
    return resp


@app.route("/")
def index():
    return redirect(url_for("propstream"))


@app.route("/propstream", methods=["GET", "POST"])
def propstream():
    print(request)
    err_msg = "The following errors were detected in the request:"

    if request.method == "POST":
        data = request.json
        values = []
        errors = []
        print(data)
        for prop in ["city", "state_code", "zip_code", "street_address"]:
            if prop in data:
                values.append(data[prop])
            else:
                errors.append(f"No {prop} was inputted")

        if len(errors) > 0:
            err_msg = add_errors(err_msg, errors)
            raise InvalidRequest(err_msg, 400)

        return propstream_req(*values)


# code to test the /propstream route
json_obj = {"city": "Palo Alto", 
            "state_code": "CA", 
            "zip_code": "94304", 
            "street_address": "3500 Deer Creek Road"}
with app.test_client() as c:
    res = c.post("/propstream", method='POST', json=json_obj)
    print("--------------Response Start---------------")
    if res.status_code == 200:
        print(res.get_json())
    else:
        print(res.get_json()['msg'])
    print("--------------Response End---------------")
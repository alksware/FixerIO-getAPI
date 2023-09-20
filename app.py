from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

api_key = "bc5c33c70c8b77d659337f25800d460e"
url = "http://data.fixer.io/api/latest?access_key=bc5c33c70c8b77d659337f25800d460e"

@app.route("/", methods=["GET", "POST"])
def index():
    currencyDict = {
        "firstCurrency": None,
        "secondCurrency": None,
        "currencyAmount": None,
        "result": None
    }

    if request.method == "POST":
        firstCurrency = request.form.get("firstCurrency")
        secondCurrency = request.form.get("secondCurrency")
        amount = request.form.get("amount")
        
        # API isteği yap
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  # JSON içeriğini çözümle
            firstVAL = data["rates"][firstCurrency]
            secondVAL = data["rates"][secondCurrency]
            res = (secondVAL/firstVAL) * float(amount)

            currencyDict["firstCurrency"] = firstCurrency
            currencyDict["secondCurrency"] = secondCurrency
            currencyDict["currencyAmount"] = amount
            currencyDict["result"] = res

        else:
            app.logger.error("API isteği başarısız oldu. Status code: %s", response.status_code)
            currencyDict["error"] = "API isteği başarısız oldu. Status code: {}".format(response.status_code)

    return render_template("index.html", currencyDict=currencyDict)

if __name__ == "__main__":
    app.run(debug=True)

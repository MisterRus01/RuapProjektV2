from flask import Flask, render_template, request, jsonify
import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

app = Flask(__name__)
# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script



url = 'http://e6d493d4-6aaa-435b-b16e-7fcced2d945e.westeurope.azurecontainer.io/score'
api_key = 'VaY1b33pnHtku07lSWqjnLnTIFdY3BHE'


if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json  # JSON iz zahtjeva

        # Prepravi strukturu JSON-a kako bi odgovarao očekivanom formatu
        formatted_data = {
            "Inputs": {
                "input1": [input_data]  # Azure ML očekuje listu unutar "input1"
            }
        }

        body = json.dumps(formatted_data).encode('utf-8')  # Encode u JSON format
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        req = urllib.request.Request(url, body, headers)
        response = urllib.request.urlopen(req)

        result = json.loads(response.read())
        print(result)
        scored_label = result['Results']['WebServiceOutput0'][0]['Scored Labels']
        return jsonify({"Scored Labels": scored_label})

    except urllib.error.HTTPError as e:
        return jsonify({"error": e.read().decode("utf-8")}), e.code


if __name__ == '__main__':
    app.run(debug=True)
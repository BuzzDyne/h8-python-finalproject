from flask import render_template
import config

connex_app = config.connex_app

# connex_app.add_api("swagger.yml")
connex_app.add_api("openapi3.yml")

@connex_app.route("/")
def home():
    return {'msg':'Welcome to Home!'}


if __name__ == "__main__":
    connex_app.run(host="localhost", port=4041, debug=True)
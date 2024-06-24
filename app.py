from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

@app.route("/template", methods=["POST"])
def get_template():
    data = request.get_json()
    template_name = data.get('templateName')
    title = data.get('title')
    

    if template_name:
        try:
            module = importlib.import_module(f"Templates.{template_name}.app")
            template_func = getattr(module, template_name)
            response = template_func(title)
            return jsonify({"message": response}), 200
        
        except (ModuleNotFoundError, AttributeError) as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "templateName not provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import json
import logging

app = Flask(__name__)

# Activer les logs
logging.basicConfig(level=logging.DEBUG)

# Charger la base de connaissances
def load_knowledge_base():
    with open('knowledge_base.json', 'r') as f:
        return json.load(f)

# Fonction d'inférence
def inference(facts, rules):
    recommendations = []
    for rule in rules:
        logging.debug(f"Vérification de la règle : {rule}")
        if all(fact in facts for fact in rule.get('if', [])):  # Vérifie que tous les faits sont présents
            logging.debug(f"Règle appliquée : {rule['then']}")
            # Example product details - adapt this to your real data
            product = {
                'name': rule.get('then')[0],  # Use the first recommendation as the product name
                'imageUrl': f'/static/img/{rule.get("then")[0].replace(" ", "").lower()}.jpg',  # Corrected image URL pattern
                'description': f"Le produit idéal pour vos cheveux {', '.join(facts)}."
            }
            recommendations.append(product)
        else:
            logging.debug(f"Règle non appliquée, faits manquants : {rule['if']}")
    
    return recommendations if recommendations else [{"name": "Aucune recommandation", "description": "Aucune recommandation trouvée.", "imageUrl": ""}]

# Route principale
@app.route('/')
def index():
    return render_template('test.html')

# Route pour soumettre des faits et obtenir une conclusion
@app.route('/inference', methods=['POST'])
def infer():
    data = request.get_json()
    facts = data.get('facts', [])
    logging.debug(f"Faits reçus: {facts}")  # Affiche les faits reçus

    knowledge_base = load_knowledge_base()
    rules = knowledge_base['rules']
    recommendations = inference(facts, rules)  # Call the single inference function
    logging.debug(f"Recommandation générée : {recommendations}")  # Affiche la recommandation générée

    return jsonify({'result': recommendations})


if __name__ == '__main__':
    app.run(debug=True)

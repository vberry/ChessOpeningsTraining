from flask import Flask, request, redirect, url_for, render_template_string
import os
from moteur import Moteur
app = Flask(__name__)
books_folder = '../openings'
M=Moteur(books_folder)
@app.route("/", methods=["GET", "POST"])
def index():
    books = M.get_book_list()
   
    if request.method == "POST":
        selected_book = request.form.get("choix_ouverture")
        selected_color = request.form.get("choix_couleur")
        if selected_book and selected_color:
            chemin_complet = os.path.join(books_folder, selected_book)
            if not os.path.isfile(chemin_complet):
                return f"Fichier {chemin_complet} non trouvé.", 404
            M.open_book(chemin_complet)
            return redirect(url_for('view_file', filename=selected_book, color=selected_color))
 
    html = '''
        <h2>Choisir un fichier d'ouverture et une couleur</h2>
        {% if books %}
        <form method="post">
            <h3>Choix du fichier :</h3>
            {% for b in books %}
                <input type="radio" name="choix_ouverture" value="{{ b }}" required> {{ b }}<br>
            {% endfor %}
 
            <h3>Choix de la couleur :</h3>
            <input type="radio" name="choix_couleur" value="blanc" required> Blanc<br>
            <input type="radio" name="choix_couleur" value="noir" required> Noir<br><br>
 
            <button type="submit">Valider</button>
        </form>
        {% else %}
            <p>Aucun fichier .sqlite trouvé dans le dossier.</p>
        {% endif %}
    '''
    return render_template_string(html, books=books)
 
@app.route("/<filename>/<color>",methods=["GET", "POST"])
def view_file(filename, color):
    if request.method == "POST":
        x = request.form.get("coup")
        coup = request.form.get("coup")
        if M.jouer_coup(coup)==False:
            print("coup pas legal")
        else:
            print("2e coup")
            M.jouer_coup()
        print(x)        
 
   
    M.board_string()
    #M.close_book()
    html = '''
        <h3>Fichier sélectionné : {{ filename }}</h3>
        <h3>Couleur choisie : {{ color }}</h3>
        <a href="{{ url_for('index') }}">← Retour</a>
        <pre> {{txt}} </pre>
        <br>    
        Choisir un coup :
        <form method="post">
        <input name="coup"/>
        <button type="submit">Valider</button>
        </form>
 
 
    '''
    return render_template_string(html, filename=filename, color=color, txt=M.display())
 
if __name__ == "__main__":
    app.run(debug=True)
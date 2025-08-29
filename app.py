from flask import Flask, render_template, request, redirect, url_for
from collections import Counter

app = Flask(__name__)

# ----- Define your quiz here -----
# Note: we give each question an "id" so the template doesn't need loop.parent.
questions_list = [
    {'id': 1, 'text': 'Il tuo pasto ideale è…', 'Options': [
        {"text": "Un'insalata gourmet, con verdura di stagione e aceto balsamico", "category": "A"},
        {"text": "Qualsiasi cosa, purché sia in porzioni abbondanti", "category": "B"},
        {"text": "Pasta, riso, pizza: tutto quello che è cucina mediterranea", "category": "C"},
        {"text": "Non ho paura di sperimentare!", "category": "D"}]},
    {'id': 2, 'text': 'Se dovessi scegliere come trascorrere una serata:', 'Options': [
        {"text": "A casa, in compagnia di un libro e una tazza di tè", "category": "A"},
        {"text": "Una pizzata con gli amici e tante chiacchiere", "category": "B"},
        {"text": "Una tranquilla passeggiata in riva al mare o al lago", "category": "C"},
        {"text": "Perché non sdraiarsi sul tetto a guardare le stelle?", "category": "D"}]},
    {'id': 3, 'text': 'La località in cui non ti stanchi mai di andare:', 'Options': [
        {"text": "Al lago, tra montagne, cielo e acqua", "category": "A"},
        {"text": "In montagna, con aria frizzante e clima fresco", "category": "B"},
        {"text": "In una città d'arte, dove c'è sempre qualcosa da imparare", "category": "C"},
        {"text": "Al mare, per farmi cullare dal suono delle onde", "category": "D"}]},
    {'id': 4, 'text': 'Meglio lavorare:', 'Options': [
        {"text": "In solitudine, per concentrarsi meglio", "category": "A"},
        {"text": "In gruppo, così da darsi una mano a vicenda", "category": "B"},
        {"text": "Per conto mio, ma accanto a persone a cui posso chiedere aiuto se serve", "category": "C"},
        {"text": "Lavorare? In che senso?", "category": "D"}]},
    {'id': 5, 'text': 'Un luogo che ho sempre desiderato visitare:', 'Options': [
        {"text": "Giappone", "category": "A"},
        {"text": "Nuova Zelanda", "category": "B"},
        {"text": "Stati Uniti", "category": "C"},
        {"text": "Thailandia", "category": "D"}]},
    {'id': 6, 'text': 'Scegli il tipo di musica che più ti è congeniale:', 'Options': [
        {"text": "Classica", "category": "A"},
        {"text": "Folk", "category": "B"},
        {"text": "Rock", "category": "C"},
        {"text": "Tutto, purché lo possa cantare ad alta voce", "category": "D"}]},
    {'id': 7, 'text': 'Se dovessi scegliere un colore…', 'Options': [
        {"text": "Verde", "category": "A"},
        {"text": "Beige", "category": "B"},
        {"text": "Viola", "category": "C"},
        {"text": "Rosa", "category": "D"}]},
    {'id': 8, 'text': 'Meglio viaggiare…', 'Options': [
        {"text": "A piedi o in bicicletta", "category": "A"},
        {"text": "In auto", "category": "B"},
        {"text": "In treno", "category": "C"},
        {"text": "In aereo", "category": "D"}]},
    {'id': 9, 'text': 'Quale saga fantasy sceglieresti?', 'Options': [
        {"text": "Le Cronache di Narnia", "category": "A"},
        {"text": "Il Signore degli Anelli", "category": "B"},
        {"text": "Il Trono di Spade", "category": "C"},
        {"text": "Cronache del mondo emerso", "category": "D"}]},
    {'id': 10, 'text': 'Se dovessi scegliere uno stile architettonico…', 'Options': [
        {"text": "Gotico, con guglie e archi a sesto acuto", "category": "A"},
        {"text": "Lineare e pulito, come lo stile classico", "category": "B"},
        {"text": "Barocco, scintillante e ricco di decorazioni", "category": "C"},
        {"text": "Un po' folle e sperimentale, come il modernismo", "category": "D"}]}
]

# Map winning category -> profile text
profiles = {
    "A": "Elfo. Sei un'anima antica! Ami la compagnia ma anche stare per conto tuo, in compagnia di un buon libro o del tuo pezzo musicale preferito. Come gli Elfi, ti piace imparare cose nuove e non hai paura di esplorare, anche in modalità solitaria.",
    "B": "Nano. Sei una personalità amorevole… ma anche testarda! Ti piace stare in compagnia e dai il meglio di te in gruppo. Come il popolo dei Nani, non ti tiri indietro di fronte a una difficoltà e non neghi mai aiuto a nessuno.",
    "C": "Uomo. Non c'è dubbio, appartieni alla Stirpe degli Uomini. Sei una persona aperta e attenta alle esigenze degli altri, ma anche affezionata alle tue abitudini, e non ti dispiace ogni tanto concederti del tempo per te.",
    "D": "Fata. Con il tuo carattere empatico, allegro e forse un po' pazzo, sei sicuramente un Abitante del Popolo Fatato. Forse non brilli per organizzazione, ma i tuoi amici sanno che possono sempre contare su di te e sul tuo buon cuore.",
}

@app.route("/")
def index():
    return render_template("index.html")
        #redirect(url_for("run_quiz")))

@app.route("/quiz", methods=["GET"])
def run_quiz():
    # Render all questions; form will POST only categories (A/B/C/D)
    return render_template("quiz.html", questions_list=questions_list)

@app.route("/submit", methods=["POST"])
def submit():
    # request.form looks like {"q1": "A", "q2": "C", ...}
    answers = request.form.to_dict()

    if not answers:
        return redirect(url_for("run_quiz"))

    # Count categories
    counts = Counter(answers.values())  # e.g. Counter({'A': 2, 'B': 1})

    # Resolve winner (majority). If tie, break by A > B > C > D (change if you prefer).
    order = ["A", "B", "C", "D"]
    max_count = max(counts.get(k, 0) for k in order)
    tied = [k for k in order if counts.get(k, 0) == max_count]
    winning_category = tied[0]  # deterministic tie-break

    result_text = profiles.get(winning_category, "Risultato non disponibile")

    # Normalize counts dict to always have all keys
    counts_all = {k: counts.get(k, 0) for k in order}

    return render_template(
        "result.html",
        result=result_text,
        counts=counts_all,
        winner=winning_category,
    )

if __name__ == "__main__":
    app.run(debug=True)

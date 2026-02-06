# assistant_vocal.py
# Assistant Vocal pour Seniors - MVP Gratuit et Stable (version finale)

from base_generiques import GENERIC_TO_PRINCEPS_RAW
from base_generiques import PRINCEPS_TO_GENERICS

import speech_recognition as sr
import json
from datetime import datetime, date
import os
import unicodedata


# -----------------------------
# NORMALISATION DES NOMS
# -----------------------------
def normaliser_nom(nom: str) -> str:
    nom = nom.lower()
    nom = "".join(
        c for c in unicodedata.normalize("NFD", nom)
        if unicodedata.category(c) != "Mn"
    )
    nom = nom.replace(",", " ")
    nom = nom.replace("/", " ")
    nom = " ".join(nom.split())
    return nom


# -----------------------------
# CORRECTION DES ERREURS GOOGLE SPEECH
# -----------------------------
def corriger_reconnaissance(texte: str) -> str:
    corrections = {
        "cyril": "loceryl",
        "siril": "loceryl",
        "ceril": "loceryl",
        "seril": "loceryl",
        "océril": "loceryl",
        "o cyril": "loceryl",
        "eau cyril": "loceryl",
        "eau siril": "loceryl",
        "eau ceril": "loceryl",
        "eau seril": "loceryl",
        "l'eau cyril": "loceryl",
        "l'eau siril": "loceryl",
        "l'eau ceril": "loceryl",
        "l'eau seril": "loceryl",
        "sériel": "loceryl",
        "série 5": "loceryl 5",
        "série": "loceryl",
    }

    t = texte.lower()
    for mauvais, bon in corrections.items():
        if mauvais in t:
            t = t.replace(mauvais, bon)
    return t


# -----------------------------
# EXTRACTION DU NOM DU MÉDICAMENT
# -----------------------------
def extraire_nom_medicament(question: str) -> str:
    q = question.lower()

    parasites = [
        "c'est quoi", "quel est", "quelle est",
        "le princeps de", "la princeps de",
        "le générique de", "la générique de",
        "generique de", "générique de",
        "princeps de", "original de",
        "est un générique de",
        "est le générique de",
        "est un princeps de",
        "est le princeps de",
        "de", "du", "des", "la", "le", "les",
        "ce médicament", "ce medicament"
    ]
    for p in parasites:
        q = q.replace(p, " ")

    q = " ".join(q.split())
    q = corriger_reconnaissance(q)

    return q.strip()


# -----------------------------
# PHONÉTIQUE
# -----------------------------
def metaphone_fr(mot: str) -> str:
    mot = normaliser_nom(mot)

    remplacements = {
        "ph": "f",
        "th": "t",
        "ch": "sh",
        "sch": "sh",
        "ck": "k",
        "qu": "k",
        "q": "k",
        "c": "k",
        "ç": "s",
        "ss": "s",
        "s": "s",
        "z": "s",
        "x": "ks",
        "gu": "g",
        "gn": "n",
        "ill": "y",
        "y": "i",
        "j": "j",
        "ge": "j",
        "gi": "j",
        "gy": "j",
    }

    for a, b in remplacements.items():
        mot = mot.replace(a, b)

    if len(mot) > 1:
        mot = mot[0] + "".join([c for c in mot[1:] if c not in "aeiouy"])

    return mot


def distance_phonetique(a: str, b: str) -> int:
    a, b = metaphone_fr(a), metaphone_fr(b)
    return sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))


def recherche_phonetique(mot: str, dictionnaire):
    meilleur = None
    meilleure_distance = 999

    for cle in dictionnaire:
        d = distance_phonetique(mot, cle)
        if d < meilleure_distance:
            meilleure_distance = d
            meilleur = cle

    if meilleure_distance <= 6:
        return meilleur

    return None


# -----------------------------
# RECHERCHE DANS LE DICTIONNAIRE
# -----------------------------
def trouver_princeps(nom_medicament: str) -> str:
    nom_normalise = normaliser_nom(nom_medicament)

    if nom_normalise in GENERIC_TO_PRINCEPS_RAW:
        return GENERIC_TO_PRINCEPS_RAW[nom_normalise]

    for generique in GENERIC_TO_PRINCEPS_RAW:
        if generique.startswith(nom_normalise):
            return GENERIC_TO_PRINCEPS_RAW[generique]

    for generique in GENERIC_TO_PRINCEPS_RAW:
        if nom_normalise in generique:
            return GENERIC_TO_PRINCEPS_RAW[generique]

    return None


# -----------------------------
# RECHERCHE INVERSE
# -----------------------------
def trouver_generiques(princeps: str):
    nom = normaliser_nom(princeps)

    for p, generiques in PRINCEPS_TO_GENERICS.items():
        if nom == normaliser_nom(p):
            return generiques

    phon = recherche_phonetique(nom, PRINCEPS_TO_GENERICS)
    if phon:
        return PRINCEPS_TO_GENERICS[phon]

    return None


# -----------------------------
# MINI BASE D'INFOS MÉDICAMENTS (EXPLICATION SIMPLE)
# -----------------------------
MED_INFO = {
    "doliprane": "Doliprane contient du paracétamol. Il est utilisé pour la douleur et la fièvre. Pour toute question médicale, demandez à votre médecin.",
    "paracetamol": "Le paracétamol est un antidouleur et antipyrétique. Pour toute question médicale, demandez à votre médecin.",
    "ramipril": "Ramipril est un médicament pour la tension artérielle. Pour toute question médicale, demandez à votre médecin.",
}


# -----------------------------
# CLASSE PRINCIPALE
# -----------------------------
class AssistantVocal:

    def __init__(self):
        print("Initialisation de l'assistant vocal...")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Mode lent (pour l'instant symbolique, utile si un jour on change de TTS)
        self.slow_mode = False

        self.load_data()

        print("✔ Assistant prêt\n")


    # -----------------------------
    # CHARGEMENT DES DONNÉES
    # -----------------------------
    def load_data(self):

        self.pilulier = {
            "lundi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "mardi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "mercredi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "jeudi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "vendredi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "samedi": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]},
            "dimanche": {"matin": ["Doliprane 500 mg"], "midi": [], "soir": ["Ramipril 5 mg"]}
        }

        self.historique_file = "historique.json"
        if os.path.exists(self.historique_file):
            with open(self.historique_file, "r") as f:
                self.historique = json.load(f)
        else:
            self.historique = []


    # -----------------------------
    # SAUVEGARDE HISTORIQUE
    # -----------------------------
    def sauvegarder_historique(self):
        with open(self.historique_file, "w") as f:
            json.dump(self.historique, f, indent=2)


    # -----------------------------
    # GESTION DU MODE LENT
    # -----------------------------
    def activer_mode_lent(self, actif: bool = True):
        self.slow_mode = actif


    # -----------------------------
    # ÉCOUTE MICRO
    # -----------------------------
    def ecouter(self):
        with self.microphone as source:
            print("À l'écoute...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                texte = self.recognizer.recognize_google(audio, language="fr-FR")
                print(f"Vous : {texte}")

                texte = corriger_reconnaissance(texte.lower())

                # Détection d'hésitation simple
                if "euh" in texte or "heu" in texte or len(texte.split()) <= 1:
                    print("Hésitation détectée.")
                    self.parler("Prenez votre temps, puis dites seulement le nom du médicament.")
                    return ""

                return texte

            except sr.WaitTimeoutError:
                print("Je n'ai rien entendu.")
                return ""

            except sr.UnknownValueError:
                print("Je n'ai pas compris.")
                return ""

            except Exception as e:
                print(f"Erreur audio : {e}")
                return ""


    # -----------------------------
    # SYNTHÈSE VOCALE (version macOS ultra stable)
    # -----------------------------
    def parler(self, texte):
        print(f"Assistant : {texte}\n")

        import subprocess

        try:
            subprocess.run(["say", "-v", "Amelie", texte])
        except Exception as e:
            print(f"Erreur TTS macOS : {e}")


    # -----------------------------
    # SÉCURITÉ MÉDICALE
    # -----------------------------
    def detecter_demande_medicale(self, question):
        mots = [
            "prendre", "dose", "dosage", "combien", "dois-je", "puis-je",
            "douleur", "fièvre", "symptôme", "malade", "arrêter", "continuer",
            "augmenter", "diminuer"
        ]
        return any(m in question for m in mots)

    def phrase_securite(self):
        return (
            "Je ne donne pas de conseils médicaux. "
            "En cas de doute ou de douleur, contactez votre médecin ou le 15."
        )

    def phrase_securite_medicaments(self):
        return (
            "Je ne donne pas de conseils médicaux. "
            "Je me base uniquement sur votre base de médicaments. "
            "Pour toute question médicale, demandez à votre médecin ou votre pharmacien."
        )


    # -----------------------------
    # PILULIER
    # -----------------------------
    def preparer_pilulier(self, jour):
        if jour not in self.pilulier:
            return f"Je n'ai pas d'information pour {jour}."

        reponse = f"Préparation du pilulier pour {jour}. "
        data = self.pilulier[jour]

        for moment in ["matin", "midi", "soir"]:
            medicaments = data.get(moment, [])
            if medicaments:
                liste = ", ".join(medicaments)
                reponse += f"{jour.capitalize()} {moment} : placez {liste}. "
            else:
                reponse += f"{jour.capitalize()} {moment} : rien à prendre. "

        return reponse


    # -----------------------------
    # CONFIRMATION PRISE
    # -----------------------------
    def confirmer_prise(self):
        self.historique.append({
            "date": datetime.now().isoformat(),
            "action": "prise_confirmee"
        })
        self.sauvegarder_historique()
        return "Parfait, c'est noté ! Bonne journée."


    # -----------------------------
    # LECTURE HISTORIQUE PRISES
    # -----------------------------
    def resume_prises(self, jour_cible: date):
        jour_str = jour_cible.isoformat()
        prises = [h for h in self.historique if h.get("action") == "prise_confirmee" and h.get("date", "").startswith(jour_str)]

        if not prises:
            return "Je n'ai aucune prise enregistrée pour ce jour."

        nb = len(prises)
        if jour_cible == date.today():
            return f"Pour aujourd'hui, j'ai enregistré {nb} prise(s) de médicaments."
        else:
            return f"Pour ce jour-là, j'ai enregistré {nb} prise(s) de médicaments."


    # -----------------------------
    # CONFIRMATION ORALE DU MÉDICAMENT
    # -----------------------------
    def confirmer_medicament(self, nom_medicament):
        self.parler(f"Vous avez dit : {nom_medicament}. C’est bien cela ?")

        reponse = self.ecouter().lower().strip()

        if not reponse:
            self.parler("Je n'ai pas compris. Pouvez-vous répondre par oui ou non ?")
            return self.confirmer_medicament(nom_medicament)

        if reponse in ["oui", "ouais", "c'est ça", "exact", "oui c'est ça"]:
            return True

        if reponse in ["non", "non non", "pas du tout"]:
            return False

        self.parler("Pouvez-vous répondre par oui ou non ?")
        return self.confirmer_medicament(nom_medicament)


    # -----------------------------
    # RÉPÉTER LE MÉDICAMENT
    # -----------------------------
    def repeter_medicament(self, nom_medicament):
        self.parler(f"Je répète : {nom_medicament}.")


    # -----------------------------
    # TRAITEMENT DES QUESTIONS
    # -----------------------------
    def traiter(self, question):

        # Mode lent / normal (symbolique pour l'instant)
        if "parle lentement" in question:
            self.activer_mode_lent(True)
            return "D'accord, je vais parler plus lentement."

        if "parle normalement" in question or "parle plus vite" in question:
            self.activer_mode_lent(False)
            return "Très bien, je reparlerai normalement."

        # Sécurité médicale
        if self.detecter_demande_medicale(question):
            return self.phrase_securite()

        # -----------------------------
        # GESTION DU PILULIER PAR LA VOIX
        # -----------------------------
        if "prendre" in question or "dois" in question or "doit" in question:

            # Détection du jour demandé
            jours = ["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
            jour_demande = None

            for j in jours:
                if j in question:
                    jour_demande = j
                    break

            # Gestion de "aujourd'hui"
            if "aujourd" in question:
                idx = datetime.today().weekday()
                jour_demande = jours[idx]

            # Gestion de "demain"
            if "demain" in question:
                idx = (datetime.today().weekday() + 1) % 7
                jour_demande = jours[idx]

            # Si aucun jour n'est trouvé → on prend aujourd'hui
            if not jour_demande:
                idx = datetime.today().weekday()
                jour_demande = jours[idx]

            # Détection du moment (matin / midi / soir)
            moment = None
            if "matin" in question:
                moment = "matin"
            elif "midi" in question:
                moment = "midi"
            elif "soir" in question or "ce soir" in question:
                moment = "soir"

            # Gestion de "maintenant"
            if "maintenant" in question:
                h = datetime.now().hour
                if h < 12:
                    moment = "matin"
                elif h < 18:
                    moment = "midi"
                else:
                    moment = "soir"

            # Réponse selon moment
            if moment:
                medicaments = self.pilulier[jour_demande][moment]
                if medicaments:
                    liste = ", ".join(medicaments)
                    return f"Pour {jour_demande} {moment}, vous devez prendre : {liste}."
                else:
                    return f"Pour {jour_demande} {moment}, vous n'avez rien à prendre."

            # Réponse complète (matin + midi + soir)
            data = self.pilulier[jour_demande]
            reponse = f"Pour {jour_demande}, voici votre traitement : "

            for m in ["matin","midi","soir"]:
                meds = data[m]
                if meds:
                    reponse += f"{m.capitalize()} : {', '.join(meds)}. "
                else:
                    reponse += f"{m.capitalize()} : rien. "

            return reponse

        # -----------------------------
        # HISTORIQUE : "QU'EST-CE QUE J'AI DÉJÀ PRIS ?"
        # -----------------------------
        if "déjà pris" in question or "deja pris" in question or "pris aujourd'hui" in question or "pris aujourd hui" in question:
            return self.resume_prises(date.today())

        if "pris hier" in question or "pris hier ?" in question:
            from datetime import timedelta
            return self.resume_prises(date.today() - timedelta(days=1))

        # Pilulier (ancienne entrée générique)
        if "pilulier" in question:
            jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
            for j in jours:
                if j in question:
                    return self.preparer_pilulier(j)
            return "Pour quel jour souhaitez-vous préparer le pilulier ?"

        # -----------------------------
        # GÉNÉRIQUE / MÉDICAMENT ORIGINAL (version senior-friendly)
        # -----------------------------
        if "générique" in question or "generique" in question or "médicament" in question or "medicament" in question or "original" in question or "vrai médicament" in question or "médicament de base" in question:
            nom = extraire_nom_medicament(question)

            # 1) Si la question contient "générique de" → on cherche les copies
            if "générique de" in question or "generique de" in question:
                liste = trouver_generiques(nom)
                if liste:
                    generiques = ", ".join(liste)
                    return f"Les génériques de {nom} sont : {generiques}. {self.phrase_securite_medicaments()}"
                else:
                    return f"{nom} est le médicament original ou n'a pas de génériques. {self.phrase_securite_medicaments()}"

            # 2) Sinon : le senior dit juste "générique" → on cherche le princeps
            resultat = trouver_princeps(nom)
            if resultat:
                if self.confirmer_medicament(resultat):
                    self.repeter_medicament(resultat)
                    return f"{nom} est un générique de {resultat}. {self.phrase_securite_medicaments()}"
                else:
                    return "D'accord, pouvez-vous répéter le nom du médicament ?"

            # 3) Rien trouvé
            return f"Je n'ai pas trouvé ce médicament dans ma base. {self.phrase_securite_medicaments()}"

        # -----------------------------
        # EXPLICATION SIMPLE D'UN MÉDICAMENT
        # -----------------------------
        if "c'est quoi ce médicament" in question or "c est quoi ce medicament" in question or "à quoi ça sert" in question or "a quoi ca sert" in question:
            nom = extraire_nom_medicament(question)
            nom_norm = normaliser_nom(nom)
            info = None

            for k, v in MED_INFO.items():
                if k in nom_norm:
                    info = v
                    break

            if info:
                return info
            else:
                return "Je ne peux pas expliquer ce médicament précisément. Pour toute question médicale, demandez à votre médecin ou votre pharmacien."

        # Confirmation prise (simple)
        if "j'ai pris" in question or "jai pris" in question or "pris" in question and "déjà" not in question:
            return self.confirmer_prise()

        # Salutations
        if "bonjour" in question or "salut" in question:
            return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

        if "comment" in question and "va" in question:
            return "Je vais bien, merci ! Et vous, comment vous sentez-vous ?"

        # Reformulation automatique
        return "Je n'ai pas bien compris. Pouvez-vous reformuler en disant seulement le nom du médicament ?"


    # -----------------------------
    # BOUCLE PRINCIPALE
    # -----------------------------
    def demarrer(self):
        self.parler("Bonjour ! Je suis votre assistant vocal. Comment puis-je vous aider ?")

        while True:
            question = self.ecouter()
            if not question:
                continue

            if "stop" in question or "au revoir" in question or "termine" in question:
                self.parler("Au revoir ! Prenez soin de vous.")
                break

            reponse = self.traiter(question)
            self.parler(reponse)


# -----------------------------
# LANCEMENT
# -----------------------------
if __name__ == "__main__":
    try:
        assistant = AssistantVocal()
        assistant.demarrer()
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")
    except Exception as e:
        print(f"Erreur : {e}")

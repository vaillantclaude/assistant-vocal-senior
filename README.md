<p align="center">
  <img src="banner.png" width="100%" />
</p>

# Assistant Vocal Senior — MVP

Un assistant vocal simple, fiable et sécurisé pour accompagner les seniors dans la gestion de leurs médicaments.

---

## 📑 Sommaire

- [Présentation générale](#présentation-générale)
- [Objectifs du projet](#objectifs-du-projet)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Architecture technique](#architecture-technique)
- [Design senior-friendly](#design-senior-friendly)
- [Sécurité & confidentialité](#sécurité--confidentialité)
- [Cas d’usage](#cas-dusage)
- [Points forts](#points-forts)
- [Évolutions possibles](#évolutions-possibles)
- [Conclusion](#conclusion)

---

## Présentation générale

L’Assistant Vocal Senior est un outil conçu pour aider les personnes âgées dans la gestion quotidienne de leurs médicaments.

Il simplifie la prise de médicaments, réduit les oublis et offre un soutien vocal accessible, sans écran ni manipulation complexe.

Ce MVP fonctionne hors ligne, utilise la voix native de macOS pour une stabilité parfaite et comprend le langage naturel des seniors, y compris leurs hésitations et formulations approximatives.

---

## Objectifs du projet

- Faciliter la gestion du traitement  
- Réduire les risques d’oubli ou de double prise  
- Offrir un accompagnement vocal quotidien  
- Rendre l’information médicale accessible  
- Proposer une solution low‑tech, robuste et inclusive  

---

## Fonctionnalités principales

### 1. Synthèse vocale fluide (macOS)

- Voix Amélie (native Apple)  
- Lecture claire et naturelle  
- Fonctionne hors ligne  
- Adaptée à l’audition des seniors  

### 2. Reconnaissance vocale adaptée aux seniors

- Tolérance aux hésitations  
- Correction automatique des erreurs  
- Compréhension du langage naturel  
- Reformulation automatique  
- Confirmation orale systématique  

### 3. Gestion complète du pilulier par la voix

Le senior peut demander :

- « Qu’est‑ce que je dois prendre aujourd’hui ? »  
- « Ce soir ? »  
- « Demain matin ? »  
- « Maintenant ? »  
- « Lundi ? »

Le système comprend :

- les jours  
- les moments (matin / midi / soir)  
- “aujourd’hui”, “demain”, “maintenant”  
- l’heure actuelle  

### 4. Gestion des génériques & médicaments originaux

Le système :

- détecte le princeps  
- détecte les génériques  
- confirme oralement  
- répète si besoin  

### 5. Historique des prises

Le senior peut demander :

- « Qu’est‑ce que j’ai déjà pris aujourd’hui ? »  
- « Et hier ? »

Le système :

- enregistre chaque prise  
- lit l’historique  
- répond clairement  

### 6. Explication simple d’un médicament

Exemples :

- « C’est quoi ce médicament Doliprane ? »  
- « À quoi ça sert Ramipril ? »

Le système fournit :

- une explication simple  
- une phrase de sécurité médicale obligatoire  

### 7. Sécurité médicale intégrée

Pour toute demande sensible :

- “combien”, “dose”, “puis‑je”, “douleur”, “fièvre”, etc.

Réponse automatique :

> « Je ne donne pas de conseils médicaux. Pour toute question, contactez votre médecin ou le 15. »

---

## Architecture technique

| Composant | Description |
|----------|-------------|
| Langage | Python 3 |
| Reconnaissance vocale | Google Speech API |
| Synthèse vocale | Moteur natif macOS (`say`) |
| Dictionnaire médicaments | Génériques ↔ Princeps |
| Base d’explications | Mini‑base interne |
| Historique | Fichier JSON local |
| Mode hors ligne | Oui (sauf reconnaissance vocale) |

---

## Design senior-friendly

- Zéro manipulation  
- Zéro écran  
- Phrases courtes  
- Tolérance aux erreurs  
- Confirmation orale  
- Répétition automatique  
- Aucune surcharge cognitive  

---

## Sécurité & confidentialité

- Fonctionne hors ligne (sauf reconnaissance vocale)  
- Aucun stockage externe  
- Historique local uniquement  
- Aucune donnée médicale sensible stockée  
- Messages de sécurité systématiques  

---

## Cas d’usage

### Exemple 1  
« Je ne me souviens plus si j’ai pris mon médicament. »  
→ Lecture de l’historique

### Exemple 2  
« Qu’est‑ce que je dois prendre ce soir ? »  
→ Lecture du pilulier

### Exemple 3  
« C’est quoi le générique de Doliprane ? »  
→ Liste des génériques

### Exemple 4  
« C’est quoi ce médicament Ramipril ? »  
→ Explication simple + sécurité  

---

## Points forts

- Ultra simple  
- Ultra stable  
- Adapté aux seniors  
- Fonctionne hors ligne  
- Extensible  
- Code propre et structuré  
- Impact social fort  

---

## Évolutions possibles

- Wake‑word (“Assistant ?”)  
- Rappels programmés  
- Interface tablette simplifiée  
- Pilulier connecté  
- Module urgence  
- Lecture des ordonnances  
- Mode conversation continue  

---

## Conclusion

Ce MVP démontre :

- une compréhension fine des besoins des seniors,  
- une maîtrise technique solide,  
- une approche centrée utilisateur,  
- un potentiel réel pour un produit d’accompagnement quotidien.

**Un assistant vocal utile, simple et humain.**

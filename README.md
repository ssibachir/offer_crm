# README - Tâches à faire

Ce document liste les tâches à réaliser pour améliorer l’application **Job Hunter CRM** selon les derniers retours et besoins.

---

## ✅ Checklist des tâches à faire

- [ ] **Dans la Inbox, remplacer le bouton \"Refus\" par \"Supprimer\"**
    - Le bouton doit supprimer définitivement l’offre de la base (Airtable).
    - Ajouter une confirmation avant suppression.

- [ ] **Faire en sorte que le nombre de fichiers filtrés change dynamiquement avec le score sélectionné**
    - Lorsque l’utilisateur ajuste le slider de score minimum dans la Inbox, le compteur doit afficher le nombre de jobs actuellement affichés (après filtre).
    - Exemple :  
      `5 jobs affichés` si le filtre score >= 8 affiche 5 jobs.

---

## 📋 Détail des tâches

### 1. Remplacer \"Refus\" par \"Supprimer\" dans la Inbox

- **Objectif :**  
  Permettre à l’utilisateur de supprimer une offre de la base directement depuis la file d’attente (Inbox).
- **À faire :**
    - Modifier le bouton d’action dans la colonne d’actions de la Inbox.
    - Remplacer le texte et l’icône par \"🗑 Supprimer\".
    - Ajouter une boîte de dialogue de confirmation (ex : \"Êtes-vous sûr de vouloir supprimer cette offre ?\").
    - Appeler la fonction `delete_job(table, job_id)` ou équivalent pour supprimer l’enregistrement dans Airtable.
    - Rafraîchir la page après suppression.

### 2. Compteur dynamique du nombre de jobs filtrés par score

- **Objectif :**  
  Afficher en temps réel le nombre de jobs visibles selon le filtre de score appliqué.
- **À faire :**
    - Après application du filtre (slider score minimum), calculer la longueur du DataFrame filtré.
    - Afficher le nombre de jobs filtrés juste au-dessus ou en-dessous de la liste.
    - Exemple d’affichage :  
      `7 jobs affichés` ou `Aucun job à ce score` si la liste est vide.

---

## 📝 Exemple d’UI attendue

### Inbox

```
┌─────────────────────────────┬─────────────┬─────────────┐
│ Poste / Entreprise          │ Score       │ Actions     │
├─────────────────────────────┼─────────────┼─────────────┤
│ Data Scientist - ABC Corp   │ 9/10        │ 🗑 Supprimer │
│ ...                         │ ...         │ ...         │
└─────────────────────────────┴─────────────┴─────────────┘

5 jobs affichés (score ≥ 8)
```

---

## 📦 Pour contribuer

- Forkez le repo, créez une branche `feature/inbox-delete` ou `feature/inbox-filter-count`.
- Faites vos modifications, testez localement.
- Ouvrez une Pull Request avec une description claire.

---

## 🚀 Historique des demandes

- [x] Correction du filtre High Priority sur le Dashboard (score ≥ 8 **et** statut = \"À Analyser\")
- [ ] [En cours] Amélioration de la Inbox (suppression, compteur dynamique)

---

**Merci de cocher les cases au fur et à mesure de l’avancement !**
# Tutoriel Django – Application Polls

Application web développée avec Django permettant la gestion de sondages (création de questions, choix, votes), avec authentification utilisateur et affichage de statistiques.

---

## 1. Présentation du projet

Ce projet est une application web basée sur le framework Django.
Elle permet :

* L’affichage d’une liste de sondages
* La consultation du détail d’un sondage
* Le vote pour un choix
* L’affichage des résultats
* L’accès à une page de statistiques
* La gestion des utilisateurs (connexion / déconnexion)
* L’administration via l’interface Django Admin

---

## 2. Architecture du projet

Structure principale :

```
mysite/                Configuration principale Django
polls/                 Application principale (gestion des sondages)
templates/             Template global (base.html)
polls/templates/       Templates spécifiques à l’application
polls/static/          Fichiers statiques (CSS, images)
doc/                   Documentation interne
```

### Projet Django

```
mysite/
    settings.py
    urls.py
    asgi.py
    wsgi.py
```

### Application Polls

```
polls/
    models.py
    views.py
    forms.py
    urls.py
    admin.py
    templates/
        polls/
        auth/
    static/
```

---

## 3. Modèles de données

Les principaux modèles définis dans `polls/models.py` sont :

### Question

* question_text : texte de la question
* pub_date : date de publication

### Choice

* choice_text : texte du choix
* votes : nombre de votes
* relation ForeignKey vers Question

---

## 4. Fonctionnalités principales

### 4.1 Affichage des sondages

* Liste des questions publiées
* Accès au détail d’un sondage

### 4.2 Vote

* Sélection d’un choix
* Incrémentation du nombre de votes
* Affichage des résultats

### 4.3 Authentification

* Formulaire de connexion
* Gestion des sessions via django.contrib.auth
* Redirection après connexion via paramètre `next`

### 4.4 Page statistiques

* Visualisation des résultats
* Analyse des fréquences de votes

---

## 5. Interface utilisateur

L’interface repose sur :

* Bootstrap 5 via django-bootstrap5
* Un template de base (`base.html`)
* Une barre de navigation avec gestion des utilisateurs


---

Voici la **version adaptée de la section Installation**, basée sur ton `requirements.txt` réel.

---

## 6. Installation

### 6.1 Prérequis

* Python 3.11 ou supérieur recommandé
* pip
* Environnement virtuel conseillé

Vérification de la version Python :

```
python --version
```

---

### 6.2 Clonage du projet

```
git clone <repository_url>
cd <repository>
```

---

### 6.3 Création et activation d’un environnement virtuel

Sous Linux / macOS :

```
python -m venv venv
source venv/bin/activate
```

Sous Windows :

```
python -m venv venv
venv\Scripts\activate
```

---

### 6.4 Installation des dépendances

Le projet utilise les dépendances suivantes :

* Django 5.2.11
* django-bootstrap5
* django-debug-toolbar
* asgiref
* sqlparse
* tzdata
* django-stubs (pour le typage statique)

Installation via :

```
pip install -r requirements.txt
```



### 6.5 Lancement du serveur de développement

```
python manage.py runserver
```

Application accessible à l’adresse :

```
http://127.0.0.1:8000/
```

Interface d’administration :

```
http://127.0.0.1:8000/admin/
```

---

### 6.6 Mode développement (Debug Toolbar)

Le projet inclut `django-debug-toolbar`.

Pour l’utiliser :

1. Vérifier que `DEBUG = True` dans `settings.py`
2. Vérifier que `django-debug-toolbar` est ajouté dans `INSTALLED_APPS`
3. Accéder au site en local

La barre d’outils s’affichera automatiquement dans les pages.


## 7. Tests

Les tests unitaires sont situés dans :

```
polls/tests.py
```

Exécution :

```
python manage.py test
```

---

## 8. Technologies utilisées

* Python 3
* Django
* Bootstrap 5
* SQLite (base de données par défaut)



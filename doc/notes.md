2.2.1 exercice d'administration

1. il suffit d'ajouter admin.site.register(Choice) a admin.py
2. L'interface est facile d'utilisation, il suffit de cliquer sur ajouter dans la section polls et ajouter 5 questions et leurs choix respectifs
3. voici les réponses:
	1. non
	2. non
	3. non
	4. non
4.  n/a
5. ça ne marche pas, un utilisateur, un utilisateur qui n'a ni le "statut équipe" ni le "statut super-utilisateur" ne peut se connecter
6. le mot de passe a été changé
7. il suffit de décocher la cas à cocher "actif" lorsque l'on modifie un utilisateur dans l'administration, dans la section "authentification et autorisation"

2.2.2 exercice shell

2.2.2.1 Préambule

lancer le shell : python manage.py shell


2.2.2.2 Questions

1. 

Commande bash:
```bash
  for question in Question.objects.all():
  print(question.question_text)			
  print(question.pub_date)
```
Résultat:
```
What's up?
2026-02-23 12:14:20.764925+00:00
En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?
2025-12-15 23:00:00+00:00
En base de données relationnelle, quelle contrainte garantit l’unicité d’une ligne ?
2025-11-12 11:00:00+00:00
En Java, quel type est le plus adapté pour représenter un montant d’argent ?
2026-02-10 12:47:35+00:00
Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?
2026-02-17 05:00:00+00:00
Dans une API REST, quelle méthode HTTP est généralement utilisée pour créer une ressource ?
2026-02-17 12:50:42+00:00

````

2.

Commande bash:
```bash
Question.objects.filter(pub_date__month=12)
```
Résultat:
```
<QuerySet [<Question: En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?>]>
```

3.

Commande bash:
```bash
 q = Question.objects.get(id=2)
 print(q.question_text)
 print(q.pub_date)
 Choice.objects.filter(question=q)
```

Résultat:
```
En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?
2025-12-15 23:00:00+00:0
<QuerySet [<Choice: L’héritage>, <Choice: L’encapsulation>, <Choice: Le polymorphisme>]>
```

4.

Commande bash:
```bash
qlist = Question.objects.all()
for q in qlist:
    print(q.question_text)
    print(q.pub_date)
    print(Choice.objects.filter(question=q))

```


```
What's up?
2026-02-23 12:14:20.764925+00:00
<QuerySet [<Choice: Not much>, <Choice: The sky>]>
En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?
2025-12-15 23:00:00+00:00
<QuerySet [<Choice: L’héritage>, <Choice: L’encapsulation>, <Choice: Le polymorphisme>]>
En base de données relationnelle, quelle contrainte garantit l’unicité d’une ligne ?
2025-11-12 11:00:00+00:00
<QuerySet [<Choice: FOREIGN KEY>, <Choice: INDEX>, <Choice: PRIMARY KEY>]>
En Java, quel type est le plus adapté pour représenter un montant d’argent ?
2026-02-10 12:47:35+00:00
<QuerySet [<Choice: double>, <Choice: float>, <Choice: BigDecimal>]>
Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?
2026-02-17 05:00:00+00:00
<QuerySet [<Choice: Gérer les règles métier>, <Choice: Gérer l’accès aux données>, <Choice: Gérer l’interface utilisateur>]>
Dans une API REST, quelle méthode HTTP est généralement utilisée pour créer une ressource ?
2026-02-17 12:50:42+00:00
<QuerySet [<Choice: GET>, <Choice: POST>, <Choice: DELETE>]>

```

5.

Commande bash

```bash

qlist = Question.objects.all()
for q in qlist:
    Choice.objects.filter(question=q).count()
    

```

Résultat:

```
2
3
3
3
3
3
```

6.


Commande bash



```bash

from django.db.models import Sum
qlist = Question.objects.annotate(total_votes=Sum('choice__votes')).order_by('total_votes')
for q in qlist:
   print(f"votes {q.total_votes or 0} | question: {q.question_text}")
   
   
```

Résultat:
```
votes 5 | question: What's up?
votes 9 | question: En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?
votes 10 | question: Quelle est l'utilité d'un framework web ?
votes 11 | question: En base de données relationnelle, quelle contrainte garantit l’unicité d’une ligne ?
votes 15 | question: En Java, quel type est le plus adapté pour représenter un montant d’argent ?
votes 17 | question: Dans une API REST, quelle méthode HTTP est généralement utilisée pour créer une ressource ?
votes 18 | question: Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?

```
7.

Commande bash

```bash
qlist = Question.objects.all().order_by('-pub_date')
for q in qlist:
    print(q.question_text)
```

Résultat:

```
What's up?
Dans une API REST, quelle méthode HTTP est généralement utilisée pour créer une ressource ?
Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?
En Java, quel type est le plus adapté pour représenter un montant d’argent ?
En programmation orientée objet, quel principe permet de masquer les détails d’implémentation ?
En base de données relationnelle, quelle contrainte garantit l’unicité d’une ligne ?

```


8.

Commande bash:

```bash

Question.objects.filter(choice__choice_text__contains="Gérer").distinct()

```

Résultat:


```
<QuerySet [<Question: Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?>]>
```
9.

Commande bash:

```bash
from django.utils import timezone
q = Question(question_text="Quelle est l'utilité d'un framework web ?", pub_date=timezone.now())
q.save()

```


10.


Commande bash:

```bash
q = Question.objects.get(pk=7)
q.choice_set.create(choice_text="Faciliter le développement d’applications web en fournissant une structure et des outils prêts à l’emploi.", votes=0)
q.choice_set.create(choice_text="Créer automatiquement une base de données sans configuration.", votes=0)
q.choice_set.create(choice_text="Remplacer complètement le langage de programmation utilisé.", votes=0)
```

Résultat:

```
<Choice: Faciliter le développement d’applications web en fournissant une structure et des outils prêts à l’emploi.>
<Choice: Créer automatiquement une base de données sans configuration.>
<Choice: Remplacer complètement le langage de programmation utilisé.>
```

11.

Commande bash:

```bash

Question.objects.filter(pub_date__year=2026)
```

Résultat:

```
<QuerySet [<Question: What's up?>, 
<Question: En Java, quel type est le plus adapté pour représenter un montant d’argent ?>, 
<Question: Quel est le rôle principal d’une couche DAO dans une architecture multi-couches ?>, 
<Question: Dans une API REST, quelle méthode HTTP est généralement utilisée pour créer une ressource ?>, 
<Question: Quelle est l'utilité d'un framework web ?>]>
```


12.  

Commande bash:

```bash

from django.contrib.auth.models import User
  for user in User.objects.all():
    print(user.username)
    
```

Résultat:

```
campistronr
uilisateurTest

```


2.2.3 Exercice d'écriture de méthodes du modèle 

1. la méthode age() renvoit : 

```
1 day, 0:02:16.621566
70 days, 13:16:37.386794
104 days, 1:16:37.386937
13 days, 23:29:02.387104
7 days, 7:16:37.387269
6 days, 23:25:55.387434
2:54:24.511703
```

3.2 Exercice sur les parties 3 et 4

1. Dans le template Il faut ajouter : 
    ```
   - {{ question.pub_date}}
   ```
   
2. il faut créer dans les templates all.html basé sur le template par défaut de index, puis ajouter la route et ajouter la fonction all dans views.py
3. il faut modifier models pour obtenir un pourcentage de votes pour chaque question, dans les vues utiliser get_choices
et afficher le tout dans le template

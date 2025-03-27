# INFO834 - TP 1 

## Introduction

Dans le cadre de ce TP, il a fallu réaliser site permettant l'achat et la ventes d'articles (DVD, livres, etc.). Le site doit utiliser une base de données MySQL pour les informations sur les utilisateurs et Redis, un système de gestion de base de données NoSQL, pour les informations sur les articles et sur les achats. Pour ma part, j'ai mis en place tout ce qui concerne les achats mais je n'ai pas fait la partie "vente" (je ne l'avais pas vu😂).
Le lien avec Redis se fait grâce à un script Python qui permet d'exécuter des requêtes et le site est développé en PHP (avec un peu d'aide de l'IA).

## Structure du site 

Le site est divisé en plusieurs parties :

- La page d'accueil : qui pourrait afficher des informations utiles et où l'utilisateur peut se connecter (il n'y a pas de page d'inscription).
- La page de connexion : qui permet à l'utilisateur de se connecter avec son nom d'utilisateur et son mot de passe.
- La page des services : qui affiche tous les articles disponibles à la vente. Il est possible d'acheter un article en cliquant sur le bouton "Acheter".
- La page de statistiques : qui affiche plusieurs statistiques sur les connexions et sur les achats des utilisateurs (elle est accessible <u>en bas</u> de la page des services)

## Utilisation de Redis

Redis est ici utilisé pour stocker les objets et quelques informations sur les utilisateurs (nombre de connexions et achats). Les différents usages de Redis sont les suivants :

- Un compteur de connexions : chaque fois qu'un utilisateur se connecte, un compteur est incrémenté dans Redis. Cela permet de savoir combien de fois un utilisateur s'est connecté et empecher la connexion si le nombre de connexions dépasse 10 en dix minutes. Pour cela, j'ai utilisé la commande `INCR connexion:<user_id>` de Redis qui permet d'incrémenter une valeur dans Redis. J'ai également utilisé la commande `EXPIRE` pour faire expirer la clé après 600 secondes.
- Gestion des achats : chaque achat effectué par un utilisateur est enregistré dans Redis en incrémentant une clé spéficique à l'utilisateur et à l'objet acheté (`INCR achat:<user_id>:<objet_id>`). Cela permet de suivre le nombre d'achat de chaque utilisateur et de chaque objet (pour les statistiques).
- Stockage des objets : Les objets disponibles à la vente sont stockés dans un hash Redis, où chaque clé est l'id de l'objet et la valeur une chaine JSON contenant les détails de l'objet (nom, description, prix) avec la commande `HSET objets 1 '{"nom": "<nom_objet>", "description": "<description_objet>", "prix": <prix_objet>}'`. Cela permet de stocker des objets complexes dans Redis et de les récupérer facilement avec la commande `HGET objets 1` qui renvoie le JSON contenant les détails de l'objet.


## Interface en Python pour Redis

J'ai développé une interface en Python pour Redis qui permet d'exécuter des requêtes sur la base de données Redis. Cette interface ensuite est utilisée par le site PHP.

Cette interface permet d'exécuter des fonctions assez simples avec des commandes shell pour être utilisées par la commande `shell_exec` de PHP. Le format de la commande est `python <nom_script.py> <commande> <paramètres éventuels>` et le script renvoie un JSON contenant le résultat de la commande. Voici quelques exemples de commandes :

- `-count-connections <user_id>` : renvoie le nombre de connexions de l'utilisateur
- `new-connection <user_id>` : incrémente le compteur de connexions de l'utilisateur
- `-add-objet <id_objet> <nom> <description> <prix>` : ajoute un objet à la base de données Redis
- `-get-objet <id_objet>` : renvoie les détails de l'objet
- `-get-all-objets` : renvoie tous les objets disponibles à la vente
- `-buy-objet <user_id> <id_objet>` : incrémente le compteur d'achat de l'utilisateur et de l'objet
- `-inventaire <user_id>` : renvoie l'inventaire de l'utilisateur (tous les objets achetés)
- `-add-exemples` : ajoute des objets d'exemple à la base de données Redis (vous devrez le faire manuellement dans une invite de commande pour les tests (sinon le site est vide))

## Statistiques 

Les statistiques peuvent être consultées via le lien en bas de la page des services. La page affiche trois informations :

- La liste des derniers utilisateurs connectés (10 derniers)
- Le nombre d'achats effectués par chaque utilisateur (10 premiers)
- L'inventaire de l'utilisateur connecté (tous les objets achetés et leur nombre)

Ces statistiques sont créées par le script Python à partir de requêtes Redis, PHP n'a qu'à exécuter le script, décoder le JSON et afficher les résultats.

## Mise en place

Pour mettre en place le site, il faut d'abord lancer le serveur Redis et le serveur PHP sur votre machine. Ensuite, il faut peupler la base de données (en utilisant le fichier `db.sql` si vous voulez) et ajouter des objets d'exemple à la base de données Redis (en utilisant la commande `python redis.py -add-exemples` dans une invite de commande). Ensuite, il suffit d'accéder au site via un navigateur web et de se connecter avec des identifiants utilisateur que vous avez créés dans la base de données MySQL (avec les données de `db.sql` vous pouvez vous connecter avec `migmig11@yahoo.fr` et `mig` comme mot de passe par exemple).

## Conclusion

Dans l'ensemble, ce TP a été une bonne introduction à l'utilisation de Redis et à son intégration dans un site PHP. Il a été une bonne occasion de découvrir les bases de données noSQL et de s'en servir pour un petit projet concret. Cependant je dois avouer que je préfère le SQL pour l'instant 😅.

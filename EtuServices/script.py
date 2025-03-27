import redis
import sys
import json
import mysql.connector

r = redis.Redis(host='localhost', port=6379)

# Connexion à la base de données MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

def ping():
    return {"ping": "pong"}

def count_connections(user_id):
    count = r.get(f"connexions:{user_id}")
    if count is None:
        return '{"count": 0}'
    return '{"count" : ' + count.decode() + '}'

def new_connection(user_id):
    r.incr(f"connexions:{user_id}")
    r.expire(f"connexions:{user_id}", 600)
    r.incr(f"total_connexions:{user_id}")

def get_objets():
    objets = r.hgetall('objets')
    return {id.decode(): json.loads(objet) for id, objet in objets.items()}

def add_objet(id, nom, description, prix):
    objet = {"nom": nom, "description": description, "prix": prix}
    r.hset('objets', id, json.dumps(objet))

def add_exemples():
    objets = [
        {"id": "1", "nom": "Livre", "description": "Un livre intéressant", "prix": 15},
        {"id": "2", "nom": "Vélo", "description": "Un vélo en bon état", "prix": 150},
        {"id": "3", "nom": "Ordinateur", "description": "Un ordinateur portable", "prix": 500},
        {"id": "4", "nom": "Chaise", "description": "Une chaise confortable", "prix": 30},
        {"id": "5", "nom": "Table", "description": "Une table en bois", "prix": 70},
    ]
    for objet in objets:
        add_objet(objet["id"], objet["nom"], objet["description"], objet["prix"])

def buy_objet(user_id, objet_id):
    r.incr(f"achat:{user_id}:{objet_id}")

def get_nom_objet(objet_id):
    objet = r.hget('objets', objet_id)
    if objet is None:
        print(f"Erreur : L'objet avec l'ID {objet_id} n'existe pas.")
        return None
    try:
        return json.loads(objet)["nom"]
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON pour l'objet ID {objet_id} : {e}")
        return None

def get_nom_utilisateur(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT nom, prenom FROM utilisateurs WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return f"{user['prenom']} {user['nom']}"
    return f"Utilisateur {user_id}"

def list_achats(user_id):
    achats = r.keys(f"achat:{user_id}:*")
    objets = {}
    for achat in achats:
        objet_id = achat.decode().split(":")[-1]
        nom_objet = get_nom_objet(objet_id)
        if nom_objet:
            objets[nom_objet] = int(r.get(achat).decode())
    return objets

def top_users_connexions():
    users = r.keys("total_connexions:*")
    top_users = {}
    for user in users:
        user_id = user.decode().split(":")[-1]
        count = int(r.get(user).decode())
        top_users[get_nom_utilisateur(user_id)] = count
    return dict(sorted(top_users.items(), key=lambda item: item[1], reverse=True)[:10])

def objets_plus_achetes():
    objets = r.hgetall('objets')
    achats = {}
    for objet_id, objet in objets.items():
        nom_objet = json.loads(objet)["nom"]
        total_achats = sum(int(r.get(f"achat:{user_id}:{objet_id.decode()}").decode() or 0) for user_id in r.keys("achat:*"))
        achats[nom_objet] = total_achats
        print(f"Objet: {nom_objet}, Total achats: {total_achats}")  # Debug print
    return dict(sorted(achats.items(), key=lambda item: item[1], reverse=True)[:10])


def utilisateurs_plus_acheteurs():
    users = r.keys("achat:*")
    achats = {}
    for user in users:
        user_id = user.decode().split(":")[1]
        if user_id not in achats:
            achats[user_id] = 0
        achats[user_id] += int(r.get(user).decode())
    return {get_nom_utilisateur(user_id): count for user_id, count in sorted(achats.items(), key=lambda item: item[1], reverse=True)[:10]}

def inventaire_utilisateur(user_id):
    achats = r.keys(f"achat:{user_id}:*")
    inventaire = {}
    for achat in achats:
        objet_id = achat.decode().split(":")[-1]
        nom_objet = get_nom_objet(objet_id)
        if nom_objet:
            inventaire[nom_objet] = int(r.get(achat).decode())
    return inventaire

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('beep beep')
        sys.exit(1)

    elif sys.argv[1] == '-ping':
        print(ping())
        sys.exit(0)

    elif sys.argv[1] == '-new':
        new_connection(sys.argv[2])
        sys.exit(0)

    elif sys.argv[1] == '-count':
        print(count_connections(sys.argv[2]))
        sys.exit(0)

    elif sys.argv[1] == '-get-objets':
        print(json.dumps(get_objets()))
        sys.exit(0)

    elif sys.argv[1] == '-add-objet':
        id = sys.argv[2]
        nom = sys.argv[3]
        description = sys.argv[4]
        prix = sys.argv[5]
        add_objet(id, nom, description, prix)
        sys.exit(0)

    elif sys.argv[1] == '-add-exemples':
        add_exemples()
        sys.exit(0)

    elif sys.argv[1] == '-buy-objet':
        buy_objet(sys.argv[2], sys.argv[3])
        sys.exit(0)

    elif sys.argv[1] == '-list-achats':
        print(json.dumps(list_achats(sys.argv[2])))
        sys.exit(0)

    elif sys.argv[1] == '-top-users':
        print(json.dumps(top_users_connexions()))
        sys.exit(0)

    elif sys.argv[1] == '-objets-plus-achetes':
        print(json.dumps(objets_plus_achetes()))
        sys.exit(0)

    elif sys.argv[1] == '-utilisateurs-plus-acheteurs':
        print(json.dumps(utilisateurs_plus_acheteurs()))
        sys.exit(0)

    elif sys.argv[1] == '-inventaire':
        print(json.dumps(inventaire_utilisateur(sys.argv[2])))
        sys.exit(0)

    else:
        print('beep beep')
        sys.exit(1)

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Achat/Vente d'Objets</title>
    <style>
        .objet {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>Nozama</h1>
    <p>Voici les objets disponibles à la vente :</p>

    <?php
    session_start();

    // Appeler le script Python pour récupérer les objets
    $output = shell_exec('python script.py -get-objets 2>&1');
    $objets = json_decode($output, true);

    if (!empty($objets)) {
        foreach ($objets as $id => $objet) {
            echo "<div class='objet'>";
            echo "<h2>" . htmlspecialchars($objet["nom"]) . "</h2>";
            echo "<p>" . htmlspecialchars($objet["description"]) . "</p>";
            echo "<p>Prix : " . htmlspecialchars($objet["prix"]) . " €</p>";
            echo "<button onclick='acheter(" . htmlspecialchars($id) . ")'>Acheter</button>";
            echo "</div>";
        }
    } else {
        echo "Aucun objet disponible.";
    }
    ?>

    <a href="accueil.php">Retour à l'accueil</a>
    <a href="statistiques.php">Voir les statistiques</a>

    <script>
        function acheter(id) {
            fetch('buy_objet.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'objet_id=' + id
            })
            .then(response => response.text())
            .then(data => {
                alert("Objet acheté avec succès !");
            })
            .catch(error => {
                console.error('Erreur :', error);
            });
        }
    </script>
</body>
</html>

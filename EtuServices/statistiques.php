<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Statistiques</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Statistiques</h1>

    <?php
    session_start();

    // Fonction pour obtenir les statistiques depuis Redis via le script Python
    function get_stats($command) {
        $output = shell_exec("python script.py $command 2>&1");
        $data = json_decode($output, true);
        return $data ? $data : [];
    }

    echo "<h2>Derniers utilisateurs connectés</h2>";
    echo "<table><tr><th>Utilisateur</th><th>Nombre de connexions</th></tr>";
    $derniers_utilisateurs = get_stats('-top-users');
    foreach ($derniers_utilisateurs as $user => $count) {
        echo "<tr><td>$user</td><td>$count</td></tr>";
    }
    echo "</table>";

    echo "<h2>Utilisateurs qui ont le plus acheté</h2>";
    echo "<table><tr><th>Utilisateur</th><th>Nombre d'achats</th></tr>";
    $utilisateurs_plus_acheteurs = get_stats('-utilisateurs-plus-acheteurs');
    foreach ($utilisateurs_plus_acheteurs as $user => $count) {
        echo "<tr><td>$user</td><td>$count</td></tr>";
    }
    echo "</table>";

    // Inventaire de l'utilisateur connecté
    $user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : 1;
    echo "<h2>Votre inventaire</h2>";
    echo "<table><tr><th>Objet</th><th>Quantité</th></tr>";
    $inventaire = get_stats("-inventaire $user_id");
    foreach ($inventaire as $objet => $count) {
        echo "<tr><td>$objet</td><td>$count</td></tr>";
    }
    echo "</table>";
    ?>

    <a href="services.php">Retour aux objets</a>
</body>
</html>

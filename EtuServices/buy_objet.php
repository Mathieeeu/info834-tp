<?php
session_start();

if (isset($_SESSION['user_id']) && isset($_POST['objet_id'])) {
    $user_id = $_SESSION['user_id'];
    $objet_id = $_POST['objet_id'];

    // Appeler le script Python pour enregistrer l'achat
    shell_exec("python script.py -buy-objet $user_id $objet_id 2>&1");
}
?>

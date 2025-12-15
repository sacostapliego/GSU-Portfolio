<?php
function remove_all($str, $char) {
    $result = "";

    for ($i = 0; $i < strlen($str); $i++) {
        if ($str[$i] != $char) {
            $result .= $str[$i];
        }
    }

    return $result;
}

// Example call
echo remove_all("Summer is here!", 'e');
?>

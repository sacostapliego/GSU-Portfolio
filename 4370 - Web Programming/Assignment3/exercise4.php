<?php
function word_count($str) {
    $count = 0;
    $inWord = false;

    for ($i = 0; $i < strlen($str); $i++) {
        $char = $str[$i];

        if ($char != ' ' && !$inWord) {
            $inWord = true;
            $count++;
        } elseif ($char == ' ') {
            $inWord = false;
        }
    }

    return $count;
}

// Example call
echo word_count("hello, how are you?");
?>

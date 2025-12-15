<?php
function countWords($str) {
    $str = strtolower($str);
    $words = preg_split('/\s+/', trim($str)); // split by spaces
    $counts = array();

    foreach ($words as $word) {
        if ($word != "") {
            if (isset($counts[$word])) {
                $counts[$word]++;
            } else {
                $counts[$word] = 1;
            }
        }
    }

    print_r($counts);
}

// Example call
countWords("This is a test. This is only a test.");
?>

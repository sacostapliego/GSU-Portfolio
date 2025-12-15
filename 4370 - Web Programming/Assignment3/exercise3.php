<?php
function triangle($size) {
    for ($i = 1; $i <= $size; $i++) {
        for ($space = $size - $i; $space > 0; $space--) {
            echo "&nbsp;"; // HTML space
        }
        for ($star = 1; $star <= $i; $star++) {
            echo "*";
        }
        echo "<br>";
    }
}

// Example call
triangle(5);
?>

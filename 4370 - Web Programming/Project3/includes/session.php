<?php
// Session management
session_start();
if (!isset($_SESSION['session_id'])) {
    $_SESSION['session_id'] = uniqid('sess_', true);
}

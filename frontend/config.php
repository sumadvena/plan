<?php
// config.php - Konfiguracja połączenia z bazą danych

// Konfiguracja bazy danych
define('DB_HOST', 'localhost');
define('DB_NAME', 'plan_lekcji');
define('DB_USER', 'plan');
define('DB_PASS', 'lekcji');
define('DB_CHARSET', 'utf8mb4');

// Funkcja połączenia z bazą danych
function getDatabaseConnection() {
    try {
        $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
        $pdo = new PDO($dsn, DB_USER, DB_PASS);
        
        // Ustawienia PDO
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        $pdo->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
        
        return $pdo;
    } catch(PDOException $e) {
        error_log("Błąd połączenia z bazą danych: " . $e->getMessage());
        throw new Exception("Nie można nawiązać połączenia z bazą danych");
    }
}

// Ustawienia CORS dla API
function setCorsHeaders() {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization');
    header('Content-Type: application/json; charset=utf-8');
    
    // Obsługa preflight requests
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit();
    }
}

// Funkcja do bezpiecznego pobierania parametrów
function getParam($name, $default = null, $type = 'string') {
    $value = $_GET[$name] ?? $_POST[$name] ?? $default;
    
    if ($value === null) {
        return $default;
    }
    
    switch ($type) {
        case 'int':
            return filter_var($value, FILTER_VALIDATE_INT) !== false ? (int)$value : $default;
        case 'email':
            return filter_var($value, FILTER_VALIDATE_EMAIL) ?: $default;
        case 'string':
        default:
            return is_string($value) ? trim($value) : $default;
    }
}

// Funkcja do wysyłania odpowiedzi JSON
function sendJsonResponse($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

// Funkcja do wysyłania błędu
function sendError($message, $status = 400) {
    sendJsonResponse(['error' => $message], $status);
}

// Logowanie błędów
function logError($message, $context = []) {
    $logMessage = date('Y-m-d H:i:s') . " - " . $message;
    if (!empty($context)) {
        $logMessage .= " - Context: " . json_encode($context);
    }
    error_log($logMessage);
}
?>
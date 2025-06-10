<?php
require_once 'config.php';

setCorsHeaders();

// Pobieranie parametrów
$action = getParam('action', '');
$szkola = getParam('szkola', '');
$grupa = getParam('grupa', ''); // zmieniona nazwa z 'klasa'
$nauczyciel = getParam('nauczyciel', '');

try {
    $pdo = getDatabaseConnection();
    
    switch($action) {
        case 'schools':
            getSchools($pdo);
            break;
        case 'groups': // zmieniona nazwa z 'classes'
            getGroups($pdo, $szkola);
            break;
        case 'teachers':
            getTeachers($pdo, $szkola);
            break;
        case 'schedule':
            getSchedule($pdo, $szkola, $grupa, $nauczyciel);
            break;
        default:
            sendError('Nieprawidłowa akcja', 400);
    }
} catch(Exception $e) {
    logError('API Error: ' . $e->getMessage());
    sendError('Błąd serwera: ' . $e->getMessage(), 500);
}

function getSchools($pdo) {
    try {
        $stmt = $pdo->query("SELECT id, name AS nazwa FROM schools ORDER BY name");
        $schools = $stmt->fetchAll();
        sendJsonResponse($schools);
    } catch(PDOException $e) {
        logError('Error fetching schools: ' . $e->getMessage());
        sendError('Błąd pobierania szkół');
    }
}

function getGroups($pdo, $szkola_id = '') {
    try {
        $sql = "SELECT g.id, g.name AS nazwa, g.id_school AS szkola_id 
                FROM groups g";
        
        $params = [];
        if ($szkola_id) {
            $sql .= " WHERE g.id_school = :szkola_id";
            $params[':szkola_id'] = $szkola_id;
        }
        
        $sql .= " ORDER BY g.name";
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        
        $groups = $stmt->fetchAll();
        sendJsonResponse($groups);
    } catch(PDOException $e) {
        logError('Error fetching groups: ' . $e->getMessage());
        sendError('Błąd pobierania grup');
    }
}

function getTeachers($pdo, $szkola_id = '') {
    try {
        $sql = "SELECT t.id, t.name AS imie, t.surname AS nazwisko, t.id_school
                FROM teachers t";
        
        $params = [];
        if ($szkola_id) {
            $sql .= " WHERE t.id_school = :szkola_id";
            $params[':szkola_id'] = $szkola_id;
        }
        
        $sql .= " ORDER BY t.surname, t.name";
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        
        $teachers = $stmt->fetchAll();
        sendJsonResponse($teachers);
    } catch(PDOException $e) {
        logError('Error fetching teachers: ' . $e->getMessage());
        sendError('Błąd pobierania nauczycieli');
    }
}

function getSchedule($pdo, $szkola_id = '', $grupa_id = '', $nauczyciel_id = '') {
    try {
        // Ta tabela jest bardzo skomplikowana - na razie zwróć pustą odpowiedź
        // Będziemy musieli dodać przykładowe dane do tabeli schedule
        
        $sql = "SELECT 
                    s.name as szkola_nazwa,
                    g.name as grupa_nazwa,
                    sch.timeframe,
                    c.name as przedmiot,
                    CONCAT(t.name, ' ', t.surname) as nauczyciel,
                    cl.location as sala
                FROM schedule sch
                JOIN schools s ON sch.id_school = s.id
                JOIN assigned_sets aset ON sch.id_assigned_set = aset.id
                JOIN groups g ON aset.id_group = g.id
                JOIN teachers t ON aset.id_teacher = t.id
                JOIN courses c ON aset.id_course = c.id
                JOIN classrooms cl ON sch.id_classroom = cl.id
                WHERE 1=1";
        
        $params = [];
        
        if ($szkola_id) {
            $sql .= " AND s.id = :szkola_id";
            $params[':szkola_id'] = $szkola_id;
        }
        
        if ($grupa_id) {
            $sql .= " AND g.id = :grupa_id";
            $params[':grupa_id'] = $grupa_id;
        }
        
        if ($nauczyciel_id) {
            $sql .= " AND t.id = :nauczyciel_id";
            $params[':nauczyciel_id'] = $nauczyciel_id;
        }
        
        $sql .= " ORDER BY s.name, g.name, sch.timeframe";
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute($params);
        
        $schedule = $stmt->fetchAll();
        
        // Formatowanie danych - na razie zwróć pustą strukturę
        $formatted = [];
        
        sendJsonResponse($formatted);
    } catch(PDOException $e) {
        logError('Error fetching schedule: ' . $e->getMessage());
        sendError('Błąd pobierania planu');
    }
}
?>
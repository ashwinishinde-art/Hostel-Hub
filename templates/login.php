<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Methods: POST");

include_once '../config/database.php';

$database = new Database();
$db = $database->getConnection();

$data = json_decode(file_get_contents("php://input"));

if(!empty($data->username) && !empty($data->password)) {
    
    $query = "SELECT id, username, password FROM admins WHERE username = :username LIMIT 0,1";
    $stmt = $db->prepare($query);
    $stmt->bindParam(':username', $data->username);
    $stmt->execute();
    
    if($stmt->rowCount() > 0) {
        $row = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if(password_verify($data->password, $row['password'])) {
            
            // Native Lightweight JWT Payload Implementation
            $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
            
            $payload = json_encode([
                'iss' => 'portal_hostel_server',
                'iat' => time(),
                'exp' => time() + (3600 * 4), // Valid for 4 hours
                'userId' => $row['id'],
                'username' => $row['username']
            ]);
            
            // Encode Base64Url
            $base64UrlHeader = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($header));
            $base64UrlPayload = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($payload));
            
            // Cryptographic Signing Key
            $secret = "SUPER_SECRET_HOSTEL_KEY_2026";
            $signature = hash_hmac('sha256', $base64UrlHeader . "." . $base64UrlPayload, $secret, true);
            $base64UrlSignature = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($signature));
            
            $jwt = $base64UrlHeader . "." . $base64UrlPayload . "." . $base64UrlSignature;
            
            http_response_code(200);
            echo json_encode([
                "status" => "success",
                "message" => "Access authenticated successfully.",
                "token" => $jwt
            ]);
        } else {
            http_response_code(401);
            echo json_encode(["status" => "error", "message" => "Invalid security password reference."]);
        }
    } else {
        http_response_code(404);
        echo json_encode(["status" => "error", "message" => "Administrative username identity not registered."]);
    }
} else {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Incomplete input parameters passed."]);
}
?>
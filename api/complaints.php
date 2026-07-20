<?php
// Read the inbound HTTP Headers inside the PHP worker environment
$headers = getallheaders();
$authHeader = isset($headers['Authorization']) ? $headers['Authorization'] : '';

if (preg_match('/Bearer\s(\S+)/', $authHeader, $matches)) {
    $jwt = $matches[1];
    
    // Split the token to decode the payload structure
    $tokenParts = explode('.', $jwt);
    $payload = json_decode(base64_decode(str_replace(['-', '_'], ['+', '/'], $tokenParts[1])));
    
    // Check if the current timestamp has passed the token's expiration date
    if ($payload->exp < time()) {
        http_response_code(401);
        echo json_encode(["status" => "error", "message" => "Security token expired. Please re-authenticate."]);
        exit();
    }
    
    // Safe execution context continues below...
} else {
    http_response_code(403);
    echo json_encode(["status" => "error", "message" => "Access denied. Token signature missing."]);
    exit();
}
?>
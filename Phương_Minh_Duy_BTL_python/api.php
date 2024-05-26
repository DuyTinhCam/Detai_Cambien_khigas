<?php
header('Content-Type: application/json');

// Kết nối server
$server = "127.0.0.1,1433";
$database = "Gia_JPY";
$username = "sa";
$password = "123";

try {
    $conn = new PDO("sqlsrv:Server=$server;Database=$database", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    echo json_encode(array("error" => "Connection DB failed: " . $e->getMessage()));
    exit();
}

// Method GET
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // Kiểm tra tham số đầu vào
    if(isset($_GET["action"])) {
        // Lấy tham số action
        $action = $_GET["action"];
        if($action == "get_all") {
            // Truy vấn lấy 15 dòng ngẫu nhiên từ bảng JPY_VND
            $stmt = $conn->query("SELECT TOP 15 * FROM JPY_VND ORDER BY NEWID()");

            // Xử lý kết quả
            $array_kq = [];
            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $array_kq[] = $row; // Thêm dòng hiện tại vào mảng
            }
            $json_result = json_encode($array_kq);
            echo $json_result;
        } elseif($action == "get_latest") {
            // Truy vấn lấy tỷ giá mới nhất từ bảng JPY_VND
            $stmt = $conn->query("SELECT TOP 1 * FROM JPY_VND ORDER BY rate DESC");

            // Xử lý kết quả
            $array_kq = [];
            while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
                $array_kq[] = $row; // Thêm dòng hiện tại vào mảng
            }
            $json_result = json_encode($array_kq);
            echo $json_result;
        } else {
            echo json_encode(array("error" => "Invalid action parameter"));
        }
    } else {
        echo json_encode(array("error" => "Missing action parameter"));
    }
} else {
    echo json_encode(array("error" => "Invalid request method"));
}
?>

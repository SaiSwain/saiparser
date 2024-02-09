<?php
// Retrieve the JSON data sent from the Python script
$input_data = json_decode(file_get_contents('php://input'), true);

// Check if the required keys are present in the JSON data
if (
    isset($input_data['email'], $input_data['row_newfile'], $input_data['row_oldfile'], $input_data['row_dublicate'])
) {
    // Extract relevant data
    $email = $input_data['email'];
    $row_newfile = $input_data['row_newfile'];
    $row_oldfile = $input_data['row_oldfile'];
    $row_dublicate = $input_data['row_dublicate'];

    // Database connection parameters
    $host = 'localhost';
    $user = 'root';
    $password = '';
    $database = 'truetalent';

    // Create a new connection
    $conn = new mysqli($host, $user, $password, $database);

    // Check the connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Check if the email already exists in the database
    $query = "SELECT * FROM parser WHERE Email = '$email'";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        // Email already exists, update the count_oldfile
        $row = $result->fetch_assoc();
        echo json_encode(['status' => 'existing', 'row_oldfile' => ++$row_oldfile]);
    } else {
        // Email does not exist, insert a new record and update the count_newfile
        $insert_query = "INSERT INTO parser (Email) VALUES ('$email')";
        if ($conn->query($insert_query) === TRUE) {
            echo json_encode(['status' => 'new', 'row_newfile' => ++$row_newfile]);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Error inserting record']);
        }
    }

    // Close the connection
    $conn->close();
} else {
    echo json_encode(['status' => 'error', 'message' => 'Invalid JSON data']);
}
?>


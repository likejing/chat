<?php
// require_once "log.php";
require  'Medoo.php';

use Medoo\Medoo;

//接收队列数据
function newDB()
{
    $database = new Medoo([
        // required
        'database_type' => 'mysql',
        'database_name' => 'chat',
        'server' => 'localhost',
        'username' => '',
        'password' => '@123456',

        // [optional]
        'charset' => 'utf8',
        'port' => 3306,

        // // [optional] Table prefix
        'prefix' => 'im_',

        // // [optional] Enable logging (Logging is disabled by default for better performance)
        // 'logging' => true,

        // // [optional] MySQL socket (shouldn't be used with server and port)
        // 'socket' => '/tmp/mysql.sock',

        // // [optional] driver_option for connection, read more from http://www.php.net/manual/en/pdo.setattribute.php
        // 'option' => [
        //     PDO::ATTR_CASE => PDO::CASE_NATURAL
        // ],

        // // [optional] Medoo will execute those commands after connected to the database for initialization
        // 'command' => [
        //     'SET SQL_MODE=ANSI_QUOTES'
        // ]
    ]);
    return $database;
};

//接收队列数据
function newminiblgDB()
{
    $database = new Medoo([
        // required
        'database_type' => 'mysql',
        'database_name' => 'mini_blg',
        'server' => 'localhost',
        'username' => '',
        'password' => '',

        // [optional]
        'charset' => 'utf8',
        'port' => 3306,

        // // [optional] Table prefix
        // 'prefix' => 'im_',

        // // [optional] Enable logging (Logging is disabled by default for better performance)
        // 'logging' => true,

        // // [optional] MySQL socket (shouldn't be used with server and port)
        // 'socket' => '/tmp/mysql.sock',

        // // [optional] driver_option for connection, read more from http://www.php.net/manual/en/pdo.setattribute.php
        // 'option' => [
        //     PDO::ATTR_CASE => PDO::CASE_NATURAL
        // ],

        // // [optional] Medoo will execute those commands after connected to the database for initialization
        // 'command' => [
        //     'SET SQL_MODE=ANSI_QUOTES'
        // ]
    ]);
    return $database;
};

//连接数据库
function connect2db(){
    $servername = "localhost";
    $username = "";
    $password = "";
    $dbname = "chat";
     
    // 创建连接
    $conn = new mysqli($servername, $username, $password, $dbname);
    // 检测连接
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
    return $conn; 
};
//查询所有---------查
function get_data_from_table($table_name){
    $conn=connect2db();
     
    $sql = "SELECT * FROM ".$table_name;
    $result = $conn->query($sql);
    
    $table_array=array();

    if ($result->num_rows > 0) {
        // 输出数据
        while($row = $result->fetch_assoc()) {
            $table_array[]=$row;
        }
        return $table_array;
    } else {
        return false;
    }
    $conn->close();
};


function get_id($nickname){
    $conn=connect2db();
     
    $sql = "SELECT id FROM im_users where nickname = '".$nickname."' ;";
    // echo $sql;
    $result = $conn->query($sql);
    
    $table_array=array();

    if ($result->num_rows > 0) {
        // 输出数据
        while($row = $result->fetch_assoc()) {
            $table_array[]=$row;
        }
        return $table_array;
    } else {
        return false;
    }
    $conn->close();
};

function get_unread($user_id){
    $conn=connect2db();
     
    $sql = "SELECT related_from,mobile,content,user_id,msg_type,receiver_id,im_talk_records.id,im_talk_records.created_at FROM im_users,im_talk_records where im_talk_records.is_read = 0 and im_talk_records.receiver_id=im_users.id and im_talk_records.created_at > DATE_SUB(now(), INTERVAL 7 DAY) and  im_talk_records.user_id = ".$user_id." ;";
    // echo $sql;
    $result = $conn->query($sql);
    
    $table_array=array();

    if ($result->num_rows > 0) {
        // 输出数据
        while($row = $result->fetch_assoc()) {
            $table_array[]=$row;
        }
        return $table_array;
    } else {
        return false;
    }
    $conn->close();
};
function get_task_line($device_flag){
    $conn=connect2db();
     
    $sql = "SELECT * FROM task_line where status = 1 and device_flag = '".$device_flag."' ORDER BY  rand() LIMIT 1 ;";
    $result = $conn->query($sql);
    
    $table_array=array();

    if ($result->num_rows > 0) {
        // 输出数据
        while($row = $result->fetch_assoc()) {
            $table_array[]=$row;
        }
        return $table_array[0];
    } else {
        return false;
    }
    $conn->close();
};

//+++++++++++++++增++++++++++++
//addLine
function addLine($roomUrl,$userUrl,$openTimestamp,$aweMoney)
{
    $conn = connect2db();

    // 预处理及绑定
    $stmt = $conn->prepare("INSERT INTO line (room_url,user_url,open_timestamp,awe_money) VALUES (?,?,?,?);");
    $stmt->bind_param("ssii", $roomUrl,$userUrl,$openTimestamp,$aweMoney);

    //读取参数并执行
    $stmt->execute();
    $insertId=mysqli_insert_id($conn);

    $stmt->close();
    $conn->close();

    return $insertId;
};
//addRoom
function addRoom($roomUrl,$roomKeywords,$roomViewer,$theme,$roomLike,$ranks,$aweMoney)
{
    $conn = connect2db();

    // 预处理及绑定
    $stmt = $conn->prepare("INSERT INTO rooms (room_url,room_keyword,room_viewer,theme,room_like,ranks,awe_money) VALUES (?,?,?,?,?,?,?);");
    $stmt->bind_param("ssisisi", $roomUrl,$roomKeywords,$roomViewer,$theme,$roomLike,$ranks,$aweMoney);

    //读取参数并执行
    $stmt->execute();
    $insertId=mysqli_insert_id($conn);
    if($insertId==0){
        Log::INFO(mysqli_error($conn));
    };

    $stmt->close();
    $conn->close();

    return $insertId;
};

//改
function update_task($order_id){

    $conn=connect2db();


    // 预处理及绑定
    $stmt = $conn->prepare("UPDATE task_line SET  status = 2 where  order_id = ? ;");
    $stmt->bind_param("i" , $order_id);

    //读取参数并执行
    $stmt->execute();

    $stmt->close();

    $conn->close();

    return true;
};
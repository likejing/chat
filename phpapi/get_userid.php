<?php
require "sql.php";
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$chat_id = isset($_POST['chat_id']) ? (int)htmlspecialchars($_POST['chat_id'])  : 1;
// $id = isset($_POST['id']) ? (int)htmlspecialchars($_POST['id']) : 0;
if($chat_id== ""){
    $json_arr["code"]=500;
    $json_arr["msg"] = "缺少必要数据";
    echo json_encode($json_arr);
    return;
};
$database = newDB();
$userid = $database->select("users",["mobile","related_from"] ,[
    "id" => $chat_id,
]);
if($userid){
    $json_arr["code"]=200;
    $json_arr["userid"]=$userid[0]["mobile"];
    $json_arr["related_from"]=$userid[0]["related_from"];
    $json_arr["msg"] = "获取成功";
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"]=500;
    $json_arr["msg"] = "账号未注册";
    echo json_encode($json_arr);
    return;
};
// $database->select("users", ["id"], [
//     "nickname" => $nickname,
// ]);

// print_r($output);

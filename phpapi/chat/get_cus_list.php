<?php
require  'sql.php';
// require "sql.php";
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$user_id = isset($_GET['user_id']) ? (int)htmlspecialchars($_GET['user_id'])  : 0;
if ($user_id == 0) {
    $json_arr["code"] = 500;
    $json_arr["msg"] = "缺少必要数据";
    echo json_encode($json_arr);
    return;
};
$database = newDB();
$cus_list=$database->select("users",["id","mobile"],[
    "related_from"=>$user_id,
]);
if ($cus_list) {
    $json_arr["code"] = 200;
    $json_arr["cus_count"] = count($cus_list);
    $json_arr["cus_list"] = $cus_list;
    $json_arr["msg"] = "获取成功";
    echo json_encode($json_arr);
    return;
} else {
    $json_arr["code"] = 200;
    $json_arr["cus_count"] = 0;
    $json_arr["msg"] = "该账号无客户";
    echo json_encode($json_arr);
    return;
};
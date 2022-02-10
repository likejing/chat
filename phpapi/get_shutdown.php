<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$database = newDB();
$device_list=$database->select(
    "device_status",
    ["device_name","ip"],
    [
        "update_timestamp[<]" => date("Y-m-d H:i:s",strtotime("-600 seconds")),
    ]
);
if($device_list){
    $json_arr["code"] = 200;
    $json_arr["device_list"] = $device_list;
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"] = 201;
    $json_arr["msg"] = "暂无宕机设备";
    echo json_encode($json_arr);
    return;
};

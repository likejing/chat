<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$database = newDB();
$customer_info_list=$database->select(
    "send_task_list",
    ["remark","corp_max_send","person_max_send","corp_today_send","send_template"],
    [
        "remark[!]" =>"" ,
    ]
);
if($customer_info_list){
    $json_arr["code"] = 200;
    $json_arr["customer_info_list"] = $customer_info_list;
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"] = 201;
    $json_arr["msg"] = "暂无发送任务信息";
    echo json_encode($json_arr);
    return;
};

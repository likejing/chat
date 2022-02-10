<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$corpShortName = isset($_GET['corpShortName']) ? htmlspecialchars($_GET['corpShortName']) : "";  //sender_id  就是新通过好友申请的客户的id
if ($corpShortName == "") {
    $json_arr["code"] = 500;
    $json_arr["msg"] = "缺少corpShortName";
    echo json_encode($json_arr);
    return;
};
$database = newminiblgDB();
$secrets=$database->select(
    "corp_list",
    ["back_corp_id","corp_secret","contact_secret"],
    [
        "corp_short_name" => $corpShortName,
        "LIMIT" => 1,
    ]
);
if($secrets){
    // print_r($output);
    $json_arr["code"] = 200;
    $json_arr["secrets"] = $secrets[0];
    $json_arr["msg"] = "获取secret列表成功";
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"] = 500;
    $json_arr["msg"] = "账号列表为空";
    echo json_encode($json_arr);
    return;
};

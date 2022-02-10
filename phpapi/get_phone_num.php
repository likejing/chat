<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$nickname = isset($_POST['nickname']) ? htmlspecialchars($_POST['nickname'])  : "";
// $id = isset($_POST['id']) ? (int)htmlspecialchars($_POST['id']) : 0;
if($nickname== ""){
    $json_arr["code"]=500;
    $json_arr["msg"] = "缺少必要数据";
    echo json_encode($json_arr);
    return;
};
$database = newDB();
$phone_nums = $database->select("users",["mobile"] ,[
    "nickname" => $nickname,
]);
if($phone_nums){
    $json_arr["code"]=200;
    $json_arr["mobile"]=$phone_nums[0]["mobile"];
    $json_arr["msg"] = "账号已注册";
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"]=200;
    $json_arr["msg"] = "账号未注册";
    echo json_encode($json_arr);
    return;
};
// $database->select("users", ["id"], [
//     "nickname" => $nickname,
// ]);

// print_r($output);
$json_arr["code"]=200;
$json_arr["msg"] = "账号未注册";
echo json_encode($json_arr);

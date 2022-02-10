<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$phone_num = isset($_POST['phone_num']) ? htmlspecialchars($_POST['phone_num']) : "";  //sender_id  就是新通过好友申请的客户的id
$chat_id = isset($_POST['chat_id']) ? (int)htmlspecialchars($_POST['chat_id']) : 0;
if ($chat_id == 0 || $phone_num == "") {
    $json_arr["code"] = 500;
    $json_arr["msg"] = "缺少必要数据";
    echo json_encode($json_arr);
    return;
};
$database = newDB();
$user_id=$database->select(
    "users",
    ["id"],
    [
        "mobile" => $phone_num,
    ]
);
if($user_id){
    $user_id=$user_id[0]["id"];
    // $delete_friend = $database->delete("users_friends",[
    //     "AND" => [
    //         "user_id" => $chat_id,
    //         "friend_id" => $user_id
    //     ]
    // ]);
    $delete_friend = $database->delete("users_friends",[
        "AND" => [
            "user_id" => $user_id,
            "friend_id" => $chat_id
        ]
    ]);
}else{
    $json_arr["code"] = 500;
    $json_arr["msg"] = "好友账号不存在";
    echo json_encode($json_arr);
    return;
};

// print_r($output);
$json_arr["code"] = 200;
$json_arr["msg"] = "删除好友成功";
echo json_encode($json_arr);
return;

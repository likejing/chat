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
    $is_friend = $database->select("users_friends", ["id"],[
        "user_id" => $user_id,
        "friend_id" => $chat_id,
    ]);
    if (!$is_friend) {
        $add_friend = $database->insert("users_friends", [
            "user_id" => $user_id,
        "friend_id" => $chat_id,
            "status" => 1,
        ]);
        $add_friend = $database->insert("users_friends", [
            "user_id" =>  $chat_id,
        "friend_id" =>$user_id,
            "status" => 1,
        ]);
    };
    //把对应客户的id查出来了，通过userid从corp_customer_list里，把头像和电话搞出来
    if(strpos($phone_num,'_') !== false){ 
        $new_userid= substr($phone_num, 0 , 16);
    }else{
        $new_userid= $phone_num;
    };
    $miniblg=newminiblgDB();
    $mini_data=$miniblg->select(
        "corp_customer_list",
        ["imei","avatar","phone_num","sex","customer_tag","customer_name","update_time","nick_name"],
        [
            "user_id" => $new_userid,
        ]
    );
    if($mini_data){
        $database->update(
            "users",
            [
                "avatar" => $mini_data[0]["avatar"],
                "gender" => $mini_data[0]["sex"],
                "nickname" => $mini_data[0]["phone_num"]."-".$mini_data[0]["nick_name"],
                "motto" => "用户名：".$mini_data[0]["customer_name"].",用户标签：".$mini_data[0]["customer_tag"].",添加时间：".$mini_data[0]["update_time"],
                "email" => "添加自".$mini_data[0]["imei"],
            ],
            [
                "mobile"=> $phone_num,
            ]
        );
    };
}else{
    $json_arr["code"] = 500;
    $json_arr["msg"] = "账号不存在";
    echo json_encode($json_arr);
    return;
};

// print_r($output);
$json_arr["code"] = 200;
$json_arr["msg"] = "添加好友成功";
echo json_encode($json_arr);
return;

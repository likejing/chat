<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$user_id = isset($_GET['user_id']) ? (int)htmlspecialchars($_GET['user_id'])  : 0;
$device_name = isset($_GET['device_name']) ? htmlspecialchars($_GET['device_name'])  : "";
$user_name = isset($_GET['user_name']) ? htmlspecialchars($_GET['user_name'])  : "";
$ip = isset($_GET['ip']) ? htmlspecialchars($_GET['ip'])  : "未知ip";
$user_sum = isset($_GET['user_sum']) ? (int)htmlspecialchars($_GET['user_sum'])  : 0;
// $id = isset($_POST['id']) ? (int)htmlspecialchars($_POST['id']) : 0;
if ($user_id == 0) {
    $json_arr["code"] = 500;
    $json_arr["msg"] = "缺少必要数据";
    echo json_encode($json_arr);
    return;
};
$database = newDB();
$add_user=0;
// $ip = $_SERVER["REMOTE_ADDR"];
if($device_name!=""){
    $select_device=$database->select("device_status",["id","max_user_sum"],[
        "ip"=>$device_name."--".$ip,
    ]);
    if($select_device){
        if($user_sum<$select_device[0]["max_user_sum"]){
            $blg_db=newminiblgDB();
            $add_user_status=$blg_db->select("user_auth",["add_user_status"],[
                "user_name"=>$username,
            ]);
            if($add_user_status && $add_user_status[0]["add_user_status"]=="正在上号"){
                $add_user=1;
            };
        };
        $update_device=$database->update("device_status",[
            "ask_flag"=>rand(0,99),
            "user_sum"=>$user_sum,
            "user_name"=>$user_name,
        ],[
            "ip"=>$device_name."--".$ip,
        ]);
    }else{
        if($user_sum<20){
            $blg_db=newminiblgDB();
            $add_user_status=$blg_db->select("user_auth",["add_user_status"],[
                "user_name"=>$username,
            ]);
            if($add_user_status && $add_user_status[0]["add_user_status"]=="正在上号"){
                $add_user=1;
            };
        };
        $insert_device=$database->insert("device_status",[
            "ask_flag"=>rand(0,99),
            "user_sum"=>$user_sum,
            "user_name"=>$user_name,
            "ip"=>$device_name."--".$ip,
        ]);
    };
};
$unread_data = get_unread($user_id);
if ($unread_data) {
    for($i=0;$i<count($unread_data);$i++){
        if($unread_data[$i]["msg_type"]==2){
            $save_dir=$database->select("talk_records_file",["save_dir"] ,[
                "record_id" => $unread_data[$i]["id"],
            ]);
            if($save_dir){
                $unread_data[$i]["save_dir"]=$save_dir[0]["save_dir"];
            }else{
                $unread_data[$i]["save_dir"]="";
            };
        }else{
            $unread_data[$i]["save_dir"]="";
        };
    };
    $json_arr["code"] = 200;
    $json_arr["data"] = $unread_data;
    $json_arr["add_user"] = $add_user;
    $json_arr["msg"] = "获取成功";
    echo json_encode($json_arr);
    return;
} else {
    $json_arr["code"] = 200;
    $json_arr["add_user"] = $add_user;
    $json_arr["msg"] = "账号无未读消息";
    echo json_encode($json_arr);
    return;
};

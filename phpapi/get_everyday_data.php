<?php
require  'sql.php';
header('Content-Type:application/json');
header('Access-Control-Allow-Origin:*'); // *代表允许任何网址请求
header('Access-Control-Allow-Methods:POST,GET,OPTIONS,DELETE'); // 允许请求的类型
// header('Access-Control-Allow-Credentials: true'); // 设置是否允许发送 cookies
header('Access-Control-Allow-Headers: Content-Type,Content-Length,Accept-Encoding,X-Requested-with, Origin'); // 设置允许自定义请求头的字段
$database = newDB();
$userlist=$database->select(
    "user_auth",
    [ "user_name","remark"],
    [
        "remark[!]" =>"" ,
    ]
);
$send_task_list=$database->select(
    "send_task_list",
    [ "user_name","person_max_send","corp_today_send","send_template","start_time","second_time","third_time"],
    [
        "user_name" =>array_column($userlist, 'user_name'),
    ]
);
$send_data=$database->query("SELECT user_name,count(case WHEN `status` =1 then 1 end) as 未发送,count(case WHEN `status` =2 then 1 end) as 发送完成,count(case WHEN `status` =3 then 1 end) as 发送频繁 FROM `user_imei` GROUP BY user_name")->fetchAll();
$todaytime=date('Y-m-d H:i:s',strtotime(date("Y-m-d"),time()));//今天零点
$add_data=$database->query("SELECT user_name,count(case WHEN `customer_status` ='已添加' then 1 end) as 已添加 FROM `corp_customer_list` WHERE update_time>'".$todaytime."' GROUP BY user_name")->fetchAll();
for($i=0;$i<count($userlist);$i++){
    for($j=0;$j<count($send_task_list);$j++){
        if($send_task_list[$j]["user_name"]==$userlist[$i]["user_name"]){
            $userlist[$i]=array_merge($userlist[$i],$send_task_list[$j]);
            break;
        };
    };
    for($k=0;$k<count($send_data);$k++){
        if($send_data[$k]["user_name"]==$userlist[$i]["user_name"]){
            $userlist[$i]=array_merge($userlist[$i],$send_data[$k]);
            break;
        };
    }
    for($l=0;$l<count($add_data);$l++){
        if($add_data[$l]["user_name"]==$userlist[$i]["user_name"]){
            $userlist[$i]=array_merge($userlist[$i],$add_data[$l]);
            break;
        }; 
    }
}

if($userlist){
    $json_arr["code"] = 200;
    $json_arr["today_data"] = $userlist;
    echo json_encode($json_arr);
    return;
}else{
    $json_arr["code"] = 201;
    $json_arr["msg"] = "暂无今日发送信息";
    echo json_encode($json_arr);
    return;
};

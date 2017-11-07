<?php
#header("Content-type: text/html; charset=utf-8");
/******************获取access_token******************/
function get_access_token($appid,$appsecret)    //获取access_token的函数
{
    $url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$appid&secret=$appsecret";  //获取access-token的借口
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $output = curl_exec($ch);
    if(curl_errno($ch))
    {
        echo 'Errno'.curl_error($ch);
    }
    curl_close($ch);
    $jsoninfo = json_decode($output, true);
    
    return $jsoninfo["access_token"];
}


/*************聊天机器人接口**************/

function robot($keyword,$object,$options)
{
    $weObj=new Wechat($options);
    $fromusername = $weObj->getRevFrom();
    $userid = substr($fromusername ,15);
    $userid = urlencode($userid);
    $content = urlencode($keyword);
    $url="http://www.tuling123.com/openapi/api?key=b8bb8bf591af8b522652fc2aa1e4a03a&info=$content&userid=$userid"; 
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($ch, CURLOPT_POST, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $output = curl_exec($ch);
    if(curl_errno($ch))
    {
        echo 'Errno'.curl_error($ch);
    }
    curl_close($ch);
    $jsoninfo = json_decode($output, true);
    $code = $jsoninfo["code"];
    $time = time();
    switch($code)
    {
        case "100000":
            $contentStr = $jsoninfo["text"];
        $resultStr = $weObj->text($contentStr);
        break;
        case "200000":
            $contentStr = $jsoninfo["text"];
            $url = $contentStr.$jsoninfo["url"];
            $newsdata=array("0"=>array("Title"=>"","Description"=>$contentStr,"PicUrl"=>"","Url"=>$url));
            $resultStr = $weObj->news($newsdata);
        break;
        case "302000":
               $title1 = $jsoninfo["list"][0]["article"];
               $url1 = $jsoninfo["list"][0]["detailurl"];
               $description1 = $jsoninfo["list"][0]["source"];
               $title2 = $jsoninfo["list"][2]["article"];
               $url2 = $jsoninfo["list"][2]["detailurl"];
               $description2 = $jsoninfo["list"][2]["source"];
               $title3 = $jsoninfo["list"][1]["article"];
               $url3 = $jsoninfo["list"][1]["detailurl"];
               $description3 = $jsoninfo["list"][1]["source"];
               $picurl = $jsoninfo["list"][0]["icon"];
               $newsdata=array("0"=>array("Title"=>$title1,"Description"=>$description1,"PicUrl"=>$picurl,"Url"=>$url1),
                            "1"=>array("Title"=>$title2,"Description"=>$description2,"PicUrl"=>$picurl,"Url"=>$url2),
                            "3"=>array("Title"=>$title3,"Description"=>$description3,"PicUrl"=>$picurl,"Url"=>$url3));
            $resultStr = $weObj->news($newsdata);
            break;
    }
    return $resultStr;

}
/******************************/

/******************记录用户输入和openid********************/

function record($keyword, $fromusername)
{
    $time = date('Y-m-d H:m:s');
    $link = mysql_connect('127.0.0.1', 'root', 'cgd1011');
    mysql_select_db("wechat");
    $search = "INSERT INTO record(openid, text, time)
            VALUES('$fromusername','$keyword','$time')";
    mysql_query("set names 'utf8'");
    mysql_query($search, $link);
    mysql_close();
}
/******************记录用户输入和openid********************/

/*******************Linux命令查询函数*********************/

function linux_comman($keyword,$object,$options){
    $weObj=new Wechat($options);
    $url="http://linux.51yip.com/search/$keyword";
    //$result=file_get_contents($url);
    $time=time();
    $title="Linux命令之：$keyword";
    $description="好好看,好好学\n这个命令呢是这样的";
    $newsdata=array("0"=>array("Title"=>$title,"Description"=>$description,"PicUrl"=>"","Url"=>$url));
    $resultStr = $weObj->news($newsdata);
    return $resultStr;
}
/*******************Linux命令查询函数*********************/

/*********************百度云资源查询函数*****************/

function bdsearch($keyword,$object,$options){
    $weObj=new Wechat($options);
    $contentStr=shell_exec("python movice.py $keyword");
    $time=time();
    $resultStr = $weObj->text($contentStr);
    return $resultStr;
}

/*********************百度云资源查询函数*****************/

/******************Linux命令查询函数***********************/
function robot1($content)
{
    $key = urlencode($content);
    $url="http://api.qingyunke.com/api.php?key=free&appid=0&msg=$key"; 
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, FALSE);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, FALSE);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    $output = curl_exec($ch);
    if(curl_errno($ch))
    {
        echo 'Errno'.curl_error($ch);
    }
    curl_close($ch);
    $jsoninfo = json_decode($output, true);
    $result=$jsoninfo["content"];
    return $result;
}
?>


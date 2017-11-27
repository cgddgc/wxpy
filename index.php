<?php
#include 'config.php';//要调用的函数
#include 'cloud_music.php';
include 'wechat.class.php';
#define("TOKEN", "zzzero"); 
date_default_timezone_set("Etc/GMT-8");

class mywechat extends Wechat{
    #public $weObj=new Wechat($options);
    public function __construct($options)
    {
        $this->token = isset($options['token'])?$options['token']:'';
        #$this->encodingAesKey = isset($options['encodingaeskey'])?$options['encodingaeskey']:'';
        #$this->appid = isset($options['appid'])?$options['appid']:'';
        #$this->appsecret = isset($options['appsecret'])?$options['appsecret']:'';
        #$this->debug = isset($options['debug'])?$options['debug']:false;
        #$this->logcallback = isset($options['logcallback'])?$options['logcallback']:false;
        $this->weObj = new Wechat($options);
        #$this->music=new music();
    }

    public function responseMsg($type){        
                $keyword = $this->weObj->getRevContent();
                $fromusername = $this->weObj->getRevFrom();
                switch($type) {
                    case Wechat::MSGTYPE_TEXT:
                            $this->record($keyword, $fromusername);
                            $result=$this->respon($keyword);
                            file_put_contents("index.html", $result,FILE_APPEND);
                            $this->weObj->reply($result);
                            exit;
                            break;
                    case Wechat::MSGTYPE_VOICE:
                            $keyword = $this->weObj->getRevContent();
                            $keyword = str_replace("!", "", $keyword);
                            $this->record($keyword, $fromusername);
                            $this->weObj->reply($this->respon($keyword));
                    case Wechat::MSGTYPE_EVENT:
                            $this->weObj->reply($this->receiveEvent());
                            break;
                    case Wechat::MSGTYPE_IMAGE:
                            break;
                    default:
                            $this->weObj->text("help info")->reply();
                }

        }
        /**********************消息处理函数***********************/
    public function respon($keyword){
                #$this->weObj=new Wechat($options);
                $temp=substr($keyword,0,1);
                switch($temp){
                    case ".":
                        $keyword=str_replace(".","",$keyword);
                        $resultStr=$this->linux_comman($keyword);
                        #error_log($resultStr);//,3,"/var/log/php/error.log");
                    break;
                    case "/":
                        $keyword=str_replace("/","",$keyword);
                        $resultStr=$this->bdsearch("$keyword");
                        #var_dump($resultStr);
                    break;
                    default:
                        $key=strstr($keyword, "点歌");
                        if($key<>""){
                            $resultStr=$this->getmusic($keyword);
                        }
                        else
                        {  
                            $resultStr = $this->robot($keyword);
                        }
                    break;
                    }
                return $resultStr;
            }
        /**********************消息处理函数*************************/



        /**********************事件处理函数*************************/
    public function receiveEvent(){
            #$this->weObj=new Wechat($options);
            $contentStr= "";
            $even = $this->weObj->getRevEvent();
            $event = $even['event'];
                if($event == "CLICK")
                {
                    $event=$even['key'];
                }
              switch ($event){
                case "subscribe":
                    $contentStr ="谢谢关注，发送文字或语音消息可以和我聊天哦发送'.'+Linux命令可查询该命令详细介绍发送'/'+关键字可以查询相关百度云资源,发送点歌+歌名可以点歌，后面加\"*\"+歌手名可以指定歌手";                
                          break;
                case "aaa":
                         $contentStr = "更多功能正在开发哦，敬请期待！";
                          break;
                }
                $resultStr = $this->weObj->text($contentStr);
                return $resultStr;
            }
        /**********************事件处理函数*************************/  


            
        /**********************点歌系统函数*************************/    
    public function getmusic($keyword)    //
                {   
                    $muobj=new music();
                    #$this->weObj=new Wechat($options);
                    $key = str_replace("点歌","", $keyword);
                    $art="";
                    if(strstr($key,"*")<>"")
                    {
                    $a=strpos($key,"*");
                    $word=substr($key,0,$a);
                    $art=str_replace("*","",strstr($key,"*"));
                    $key=$word;
                     }
                    $musicurl="";
                    $musicurl=$muobj->get_musicUrl($key,10,$art);
                    $artist=$muobj->get_artist($key,10,$art);
               if($musicurl == "")       //没有找到音乐资源
               { 
                $contentStr = "啊哦，没找到这首歌，听歌请输入\"点歌\"+歌名,想要指定歌手可以在后面加\"\"+歌手名字，如\"点歌告白气球*周二珂\"";
                $resultStr = $this->weObj->text($contentStr);
               }
               else
               {
                    $resultStr = $this->weObj->music($artist."-".$key,$musicurl,$musicurl);
               }
                     return $resultStr;
         
                }  
            /**********************点歌系统函数*************************/ 


                /*************聊天机器人接口**************/

    public function robot($keyword)
    {
        #$this->weObj=new Wechat($options);
        $fromusername = $this->weObj->getRevFrom();
        $userid = $fromusername;//substr($fromusername ,15);
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
                $resultStr = $this->weObj->text($contentStr);
            break;
            case "200000":
                $contentStr = $jsoninfo["text"];
                $url = $contentStr.$jsoninfo["url"];
                $newsdata=array("0"=>array("Title"=>"","Description"=>$contentStr,"PicUrl"=>"","Url"=>$url));
                $resultStr = $this->weObj->news($newsdata);
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
                $resultStr = $this->weObj->news($newsdata);
                break;
            default:
                $resultStr=$this->weObj->text($jsoninfo["text"]);
                break;
        }
        return $resultStr;

    }
    /******************************/

    /******************记录用户输入和openid********************/

    public function record($keyword, $fromusername)
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

    public function linux_comman($keyword){
        #$this->weObj=new Wechat($options);
        $url="http://linux.51yip.com/search/$keyword";
        $title="Linux命令之：$keyword";
        $description="好好看,好好学\n这个命令呢是这样的";
        $newsdata=array("0"=>array("Title"=>$title,"Description"=>$description,"PicUrl"=>"","Url"=>$url));
        $resultStr = $this->weObj->news($newsdata);
        return $resultStr;
    }
    /*******************Linux命令查询函数*********************/

    /*********************百度云资源查询函数*****************/

    public function bdsearch($keyword){
        #$this->weObj=new Wechat($options);
        $contentStr=shell_exec("python movice.py $keyword");
        #error_log($contentStr);
        $resultStr = $this->weObj->text($contentStr);
        return $resultStr;
    }

    /*********************百度云资源查询函数*****************/
}

class music{
    #public function __construct($options){
    #    $this->weObj=new Wechat($options);
    #}
    public function curl_get($url)
    {
        $refer = "http://music.163.com/";
        $header[] = "Cookie: " . "appver=1.5.0.75771;";
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
        curl_setopt($ch, CURLOPT_REFERER, $refer);
        $output = curl_exec($ch);
        curl_close($ch);
        return $output;
    }

    public function music_search($word, $type)
    {
        $url = "http://music.163.com/api/search/pc";
        $post_data = array(
            's' => $word,
            'offset' => '0',
            'limit' => '20',
            'type' => $type,
        );
        $referrer = "http://music.163.com/";
        $URL_Info = parse_url($url);
        $values = [];
        $result = '';
        $request = '';
        foreach ($post_data as $key => $value) {
            $values[] = "$key=" . urlencode($value);
        }
        $data_string = implode("&", $values);
        if (!isset($URL_Info["port"])) {
            $URL_Info["port"] = 80;
        }
        $request .= "POST " . $URL_Info["path"] . " HTTP/1.1\n";
        $request .= "Host: " . $URL_Info["host"] . "\n";
        $request .= "Referer: $referrer\n";
        $request .= "Content-type: application/x-www-form-urlencoded\n";
        $request .= "Content-length: " . strlen($data_string) . "\n";
        $request .= "Connection: close\n";
        $request .= "Cookie: " . "appver=1.5.0.75771;\n";
        $request .= "\n";
        $request .= $data_string . "\n";
        $fp = fsockopen($URL_Info["host"], $URL_Info["port"]);
        fputs($fp, $request);
        $i = 1;
        while (!feof($fp)) {
            if ($i >= 15) {
                $result .= fgets($fp);
            } else {
                fgets($fp);
                $i++;
            }
        }
        fclose($fp);
        return $result;
    }

    public function get_music_info($music_id)
    {
        $url = "http://music.163.com/api/song/detail/?id=" . $music_id . "&ids=%5B" . $music_id . "%5D";
        return $this->curl_get($url);
    }

    public function get_artist_album($artist_id, $limit)
    {
        $url = "http://music.163.com/api/artist/albums/" . $artist_id . "?limit=" . $limit;
        return $this->curl_get($url);
    }

    public function get_album_info($album_id)
    {
        $url = "http://music.163.com/api/album/" . $album_id;
        return $this->curl_get($url);
    }

    public function get_playlist_info($playlist_id)
    {
        $url = "http://music.163.com/api/playlist/detail?id=" . $playlist_id;
        return $this->curl_get($url);
    }

    public function get_music_lyric($music_id)
    {
        $url = "http://music.163.com/api/song/lyric?os=pc&id=" . $music_id . "&lv=-1&kv=-1&tv=-1";
        return $this->curl_get($url);
    }

    public function get_mv_info()
    {
        $url = "http://music.163.com/api/mv/detail?id=319104&type=mp4";
        return $this->curl_get($url);
    }

    public function get_search($word,$limit){
        $url = "http://music.163.com/api/search/get/web?csrf_token=";
        $curl = curl_init();
        $post_data = 'hlpretag=&hlposttag=&s='. $word . '&type=1&offset=0&total=true&limit=' . $limit;
        curl_setopt($curl, CURLOPT_URL,$url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER,1);

        $header =array(
            'Host: music.163.com',
            'Origin: http://music.163.com',
            'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
            'Content-Type: application/x-www-form-urlencoded',
            'Referer: http://music.163.com/search/',
        );

        curl_setopt($curl, CURLOPT_HTTPHEADER, $header);

        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
        $src = curl_exec($curl);
        curl_close($curl);
        return $src;
    }

    public function get_musicid($word,$limit,$art){
        $src=$this->get_search($word,$limit);
        $arr=json_decode($src,true);
        $music_id=$arr['result']['songs'][0]['id'];
        if($art==""){
            return $music_id;
        }
        else{
        for($i=0;$i<$limit;$i++)
        {
            $artist=$arr['result']['songs'][$i]['artists'][0]['name'];
            if(strcasecmp($artist,$art)==0)
            {
                $music_id=$arr['result']['songs'][$i]['id'];
                //var_dump($arr['result']['songs'][$i]['artists'][0]['name']);
                break;
                exit;
            }
            else $music_id="";
        }
        }
        return $music_id;
    }
    public function get_musicUrl($word,$limit,$art){
        $musicUrl="null";
        $music_id=$this->get_musicid($word,$limit,$art);
        $music_info=$this->get_music_info($music_id);
        $music_info=json_decode($music_info,true);
        #var_dump($music_info['songs'][0]);
        #echo $music_info;
        $musicUrl=$music_info['songs'][0]['mp3Url'];
        return $musicUrl;
    }
    public function get_artist($word,$limit,$art){
        $src=$this->get_search($word,$limit);
        $arr=json_decode($src,true);
        if($art==""){
            $artist=$arr['result']['songs'][0]['artists'][0]['name'];
        }
        else $artist=$art;
        //echo $src1;
        return $artist;
    }
}

$options = array('token'=>'jnugxd');
$we = new mywechat($options);
#$wechat=new Wechat($options);
$we->weObj->valid();//明文或兼容模式可以在接口验证通过后注释此句，但加密模式一定不能注释，否则会验证失败
$type = $we->weObj->getRev()->getRevType();
$we->responseMsg($type);

/*
$test =new mywechat($options);
$a=$test->respon(".python");
var_dump($a);
echo date('Y-m-d H:m:s');
*/
?>

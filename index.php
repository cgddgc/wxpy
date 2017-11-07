<?php
include 'config.php';//要调用的函数
include 'cloud_music.php';
include 'wechat.class.php';

$options = array(
        'token'=>'cgddgc', //填写你设定的key
        'encodingaeskey'=>'gxdzero1011' //填写加密用的EncodingAESKey，如接口为明文模式可忽略
    );
$weObj = new Wechat($options);
$weObj->valid();//明文或兼容模式可以在接口验证通过后注释此句，但加密模式一定不能注释，否则会验证失败
$type = $weObj->getRev()->getRevType();
#$rep=new Wechat;
responseMsg($type,$options);

#class Wechat_my extends Wechat {
    function responseMsg($type,$options){
                $weObj=new Wechat($options);
                $postObj=$weObj->getRev();
                $keyword = trim($weObj->getRevContent());
                $fromusername = $weObj->getRevFrom();
                switch($type) {
                    case Wechat::MSGTYPE_TEXT:
                            record($keyword, $fromusername);
                            $weObj->reply(respon($postObj,$keyword,$options));
                            exit;
                            break;
                    case Wechat::MSGTYPE_VOICE:
                            $keyword = $weObj->getRevContent();
                            $keyword = str_replace("！", "", $keyword);
                            record($keyword, $fromusername);
                            $weObj->reply(respon($postObj,$keyword,$options));
                    case Wechat::MSGTYPE_EVENT:
                            $weObj->reply(receiveEvent($postObj,$options));
                            break;
                    case Wechat::MSGTYPE_IMAGE:
                            break;
                    default:
                            $weObj->text("help info")->reply();
                }

        }
        /**********************消息处理函数***********************/
    function respon($object, $keyword,$options){
		$weObj=new Wechat($options);
                $funcFlag = 0;
                $temp=substr($keyword,0,1);
                switch($temp){
                    case ".":
                        $keyword=str_replace(".","",$keyword);
                        $resultStr=linux_comman($keyword,$object,$options);
                    break;
                    case "/":
                        $keyword=str_replace("/","",$keyword);
                        $resultStr=bdsearch($keyword,$object,$options);
                    break;
                    default:
                        $key=strstr($keyword, "点歌");
                        $keyword = $keyword;
                        if($key<>""){
                            $resultStr=getmusic($object, $keyword,$options);
                        }
                        else
                        {  
                            /* $temp = robot($keyword,$object);
                            $contentStr = implode("",array($temp[1],$temp[2]));
                            $resultStr=$this->constructText($object, $contentStr, $funcFlag);
                            /*$contentStr = robot1($keyword); //机器人1号
                            $textTpl = "<xml>                                    
                                        <ToUserName><![CDATA[%s]]></ToUserName>
                                        <FromUserName><![CDATA[%s]]></FromUserName>
                                        <CreateTime>%s</CreateTime>
                                        <MsgType><![CDATA[text]]></MsgType>
                                        <Content><![CDATA[%s]]></Content>
                                        <FuncFlag>%d</FuncFlag>
                                        </xml>"; 
                            $resultStr = sprintf($textTpl, $object->FromUserName, $object->ToUserName, time(), $contentStr, 0);*/
                            $resultStr = robot($keyword, $object,$options);
                        }
                    break;
                    }
                return $resultStr;
            }
        /**********************消息处理函数*************************/



        /**********************事件处理函数*************************/
    function receiveEvent($object,$options){
		$weObj=new Wechat($options);
              $contentStr= "";
              $event = $weObj->getRevEvent()['event'];
                if($event == "CLICK")
                {
                    $event=$weObj->getRevEvent()['key'];
                }
              switch ($event){
                case "subscribe":
                    $contentStr ="谢谢关注，发送文字或语音消息可以和我聊天哦发送'.'+Linux命令可查询该命令详细介绍发送'/'+关键字可以查询相关百度云资源,发送点歌+歌名可以点歌，后面加\"*\"+歌手名可以指定歌手";                
                          break;
                case "aaa":
                         $contentStr = "更多功能正在开发哦，敬请期待！";
                          break;
                }
                $resultStr = $weObj->text($contentStr);
                return $resultStr;
            }
        /**********************事件处理函数*************************/  


            
        /**********************点歌系统函数*************************/    
    function getmusic($postObj, $keyword,$options)    //
                {       
                    $key = str_replace("点歌","", $keyword);
                    $art="";
                    if(strstr($key,"*")<>"")
                    {
                    $a=strpos($key,"*");
                    $word=substr($key,0,$a);
                    $art=str_replace("*","",strstr($key,"*"));
                    $key=$word;
                     }
                    //$keywordc= urlencode($key);
                    $musicurl="";
                    $musicurl=get_musicUrl($key,10,$art);
                    $artist=get_artist($key,10,$art);
                   /* $musicapi = "http://box.zhangmen.baidu.com/x?op=12&count=1&title={$keywordc}\$\$"; 
                    $simstr=file_get_contents($musicapi);
                    $musicobj=simplexml_load_string($simstr);
                    $i=0;
                    $musicurl="none";
                    foreach($musicobj->url as $itemobj)
                    {
                        $encode = $itemobj->encode;
                        $decode = $itemobj->decode;  
                        $removedecode = end(explode('&', $decode));
                        if($removedecode<>"")
                        {
                            $removedecode="&".$removedecode;   
                        }
                        $decode = str_replace($removedecode,"", $decode);
                        $musicurl= str_replace(end(explode('/', $encode)) ,$decode,$encode);
                        break;
                    }*/
               if($musicurl == "")       //没有找到音乐资源
               { 
                $contentStr = "啊哦，没找到这首歌，听歌请输入\"点歌\"+歌名,想要指定歌手可以在后面加\"\"+歌手名字，如\"点歌告白气球*周二珂\"";
                $resultStr = $weObj->text($contentStr);
               }
               else
               {
                    $resultStr = $weObj->music($artist."-".$key,$musicurl,$musicurl);
               }
                     return $resultStr;
         
                }  
            /**********************点歌系统函数*************************/ 
#}
?>

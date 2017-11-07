<?php
function record($keyword, $fromusername)
{
    $time = date('Y-m-d H:m:s');
    $link = mysql_connect('localhost', 'root', 'cgddgc');
    mysql_select_db("wechat");
    $search = "INSERT INTO record(openid, text, time)
			VALUES('$fromusername','$keyword','$time')";
    mysql_query("set names 'utf8'");
    mysql_query($search, $link);
    mysql_close();
}
?>

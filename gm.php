<?php
include 'cloud_music.php';
$gets = $_GET;
$song = trim($gets['song']);
$art = trim($gets['singer']);
$m_url=get_musicUrl($song,10,$singer);	
$artist=get_artist($song,10,$singer);
$data=["url"=>$m_url,"artist"=>$artist];
echo json_encode($data);
?>

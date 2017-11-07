<?php
	function curl_get($url)
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

	function music_search($word, $type)
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

	function get_music_info($music_id)
	{
		$url = "http://music.163.com/api/song/detail/?id=" . $music_id . "&ids=%5B" . $music_id . "%5D";
		return curl_get($url);
	}

	function get_artist_album($artist_id, $limit)
	{
		$url = "http://music.163.com/api/artist/albums/" . $artist_id . "?limit=" . $limit;
		return curl_get($url);
	}

	function get_album_info($album_id)
	{
		$url = "http://music.163.com/api/album/" . $album_id;
		return curl_get($url);
	}

	function get_playlist_info($playlist_id)
	{
		$url = "http://music.163.com/api/playlist/detail?id=" . $playlist_id;
		return curl_get($url);
	}

	function get_music_lyric($music_id)
	{
		$url = "http://music.163.com/api/song/lyric?os=pc&id=" . $music_id . "&lv=-1&kv=-1&tv=-1";
		return curl_get($url);
	}

	function get_mv_info()
	{
		$url = "http://music.163.com/api/mv/detail?id=319104&type=mp4";
		return curl_get($url);
	}

	function get_search($word,$limit){
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
	#echo music_search("Moon Without The Stars", "1");
	#get_music_info("28949444");
	#echo get_artist_album("166009", "5");
	#echo get_album_info("3021064");
	#echo get_playlist_info("22320356");
	#echo get_music_lyric("29567020");
	#echo get_mv_info();
	#echo get_search("pdd洪荒之力",1);
	#echo get_musicid("pdd洪荒之力",1);
	//$output=get_search("普通diso",1);
	function get_musicid($word,$limit,$art){
		$src=get_search($word,$limit);
		$arr=json_decode($src,true);
		$music_id=$arr['result']['songs'][0]['id'];
		if($art==""){
			return $music_id;
		}
		else{
		for($i=0;$i<$limit;$i++)
		{
			$artist=$arr['result']['songs'][$i]['artists'][0]['name'];
			if(strcasecmp($artist,$art)==0){
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
	function get_musicUrl($word,$limit,$art){
		$musicUrl="null";
		$music_id=get_musicid($word,$limit,$art);
		$music_info=get_music_info($music_id);
		$music_info=json_decode($music_info,true);
		#var_dump($music_info['songs'][0]);
		#echo $music_info;
		$musicUrl=$music_info['songs'][0]['mp3Url'];
		return $musicUrl;
	}
	function get_artist($word,$limit,$art){
		$src=get_search($word,$limit);
		$arr=json_decode($src,true);
		if($art==""){
			$artist=$arr['result']['songs'][0]['artists'][0]['name'];
		}
		else $artist=$art;
		//echo $src1;
		return $artist;
	}

//$reg='\"songs\":\[\{\"id\":(.*?)\"name\"';
//preg_match($reg,$output,$matches);
#echo get_music_info("440353010");
//$output=$output[code];
//echo $output=get_musicUrl("我可以",1);
//$output=json_decode(get_search("玲珑",1),true);
//var_dump($output);
//echo $output['result']['songs'][0]['id'];
//echo $output=get_music_in('5250096');
?>

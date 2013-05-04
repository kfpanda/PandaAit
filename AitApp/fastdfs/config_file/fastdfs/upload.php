<?php

echo "{";
foreach( $_REQUEST as $key => $value ){
	$value = str_replace("/www/upload/capture_images", "", $value);
	echo $key.":'".$value."',";
}
echo "status:'success'}";

?>

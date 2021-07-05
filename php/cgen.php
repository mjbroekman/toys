<html>
  <head>
    <title>A basic dice rolling page</title>
    <link rel="stylesheet" type="text/css"
          href="http://broekman.us/~maarten/css/embedded_style.css">
    <link rel="stylesheet" type="text/css"
          href="http://broekman.us/~maarten/css/standalone_style.css">
  </head>
  <body>
    <?php
      $char_attrs=array('name','class','Str','Dex','Con','Int','Wis','Cha');
      $stat_names=array('Str','Dex','Con','Int','Wis','Cha');

      function start_form() {
        echo "<form action=\"cgen.php\" method=POST>\n";
      }

      function end_form() {
        echo "  <input type=submit name=submit value=\"Keep\">\n";
	echo "</form>\n";
      }

      function roll_em_1($debug) {
        srand();
	$tmp = 0;
	$rolls = array();
	for($j = 0; $j < 4; $j++) {
	  $rolls[$j] = rand(1,6);
	}
	rsort($rolls);
	$tmp = $rolls[0] + $rolls[1] + $rolls[2];
	if ( $debug == "on" ) {
	  echo "Roll = ".$tmp." =~ (".$rolls[0]."+".$rolls[1]."+".$rolls[2].". Discarded ".$rolls[3].")<br>\n";
	}
	return $tmp;
      }

      function display_name($name) {
        if ( $name == "" ) {
          echo "Name: <input type=text name=char_name><br>\n";
        } else {
          echo "Name: ".$name."<br>\n";
          echo "<input type=hidden name=char_name value=".$name.">\n";
        }
      }

      function print_stat($stats,$stat) {
        echo $stat." =&gt; ".$stats[$stat]."<br>\n";
	echo "<input type=hidden name=".$stat." value=".$stats[$stat].">\n";
      }

      function display_stats($vars) {
	global $stat_names;
	foreach ($stat_names as $stat) {
          print_stat($vars,$stat);
	}
      }

      $debug="";
      $meth1="";
      $meth2="";
      $meth3="";

      if ( $HTTP_POST_VARS['debug'] == "on" ) {
         $debug="CHECKED";
      }
      if ( $HTTP_POST_VARS['meth'] == "" ) {
         $meth1="CHECKED";   $meth2="";    $meth3="";
      }
      if ( $HTTP_POST_VARS['meth'] == 1 ) {
         $meth1="CHECKED";   $meth2="";    $meth3="";
      }
      if ( $HTTP_POST_VARS['meth'] == 2 ) {
         $meth1="";   $meth2="CHECKED";    $meth3="";
      }
      if ( $HTTP_POST_VARS['meth'] == 3 ) {
         $meth1="";   $meth2="";    $meth3="CHECKED";
      }

      if (( $HTTP_POST_VARS['submit'] == "ReRoll" ) OR
          ( $HTTP_POST_VARS['submit'] == "" )) {
            start_form();
            display_name($HTTP_POST_VARS['char_name']);
            $stats = array();
            if ( $HTTP_POST_VARS['meth'] == 1 ) {
                $stats['Str'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Dex'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Con'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Int'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Wis'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Cha'] = roll_em_1($HTTP_POST_VARS['debug']);
	    }
            if ( $HTTP_POST_VARS['meth'] == 2 ) {
                $stats['Str'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Dex'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Con'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Int'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Wis'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Cha'] = roll_em_1($HTTP_POST_VARS['debug']);
	    }
            if ( $HTTP_POST_VARS['meth'] == 3 ) {
                $stats['Str'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Dex'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Con'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Int'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Wis'] = roll_em_1($HTTP_POST_VARS['debug']);
                $stats['Cha'] = roll_em_1($HTTP_POST_VARS['debug']);
	    }
            display_stats($stats);
        ?>
            <p></p>
            Debug: <input type=checkbox name=debug <?echo $debug ?> ><br>
            Method 1: <input type=radio name="meth" value="1" <?echo $meth1 ?> > 4d6 drop lowest<br>
            Method 2: <input type=radio name="meth" value="2" <?echo $meth2 ?> > <br>
            Method 3: <input type=radio name="meth" value="3" <?echo $meth3 ?> > <br>
            <input type=submit name=submit value="ReRoll">
        <?
           end_form();
      } else {
        start_form();
        display_name($HTTP_POST_VARS['char_name']);
        display_stats($HTTP_POST_VARS);
        end_form();
      }
     ?>
  </body>
</html>


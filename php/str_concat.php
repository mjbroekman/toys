<?php
$foo = "abcdef0123456789";
$bar = "ghijklmnopqrstuvwxyz";
echo(strlen($foo)."\n");
echo(strlen($bar)."\n");
$total = strlen($bar) + strlen($foo);
$idx = 0;
while(strlen($foo) < $total) {
    echo($idx . " = " . $foo[$idx] . "\n");
    $foo .= $bar[$idx];
    $idx++; 
}
echo($foo . "\n");

#!/usr/local/bin/perl
# stop.cgi
# Stop the plex daemon

require './plex-lib.pl';
&ReadParse();
&error_setup($text{'stop_err'});
$err = &stop_plex();
&error($err) if ($err);
&webmin_log("stop");
&redirect("");

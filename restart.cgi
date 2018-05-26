#!/usr/local/bin/perl
# restart.cgi
# Restart the plex daemon

require './plex-lib.pl';
&ReadParse();
&error_setup($text{'restart_err'});
$err = &restart_plex();
&error($err) if ($err);
&webmin_log("restart");
&redirect("");

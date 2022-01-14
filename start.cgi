#!/usr/local/bin/perl
# start.cgi
# Start the plex daemon

require './plexmediaserver-lib.pl';
&ReadParse();
&error_setup($text{'start_err'});
$err = &start_plex();
&error($err) if ($err);
&webmin_log("start");
&redirect("");

#!/usr/local/bin/perl
# plex-lib.pl
# Common functions for the Plex daemon

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();

# get_plex_version()
sub get_plex_version
{
$getversion = "$config{'version_cmd'}";
$version = `$getversion`;
}

# get_plex_stats()
sub get_plex_stats
{
$getplexstat = "$config{'status_cmd'}";
$plexstatus = `$getplexstat`;
}

# get_dlna_stats()
sub get_dlna_stats
{
$getdlnastat = "$config{'status_dlna'}";
$dlnastatus = `$getdlnastat`;
}

# get_plex_config()
# Returns a reference to an array of Plex config file options.
sub get_plex_config
{
local @rv = ( { 'dummy' => 1,
		'indent' => 0,
		'file' => $config{'plex_config'},
		'line' => -1,
		'eline' => -1 } );
local $lnum = 0;
open(CONF, $config{'plex_config'});
while(<CONF>) {
	s/\r|\n//g;
	s/^\s*#.*$//g;
	local ($name, @values) = split(/\s+/, $_);
	if ($name) {
		local $dir = { 'name' => $name,
					'values' => \@values,
					'file' => $config{'plex_config'},
					'line' => $lnum };
		push(@rv, $dir);
		}
	$lnum++;
	}
close(CONF);
return \@rv;
}

# find_value(name, &config)
sub find_value
{
foreach $c (@{$_[1]}) {
	if (lc($c->{'name'}) eq lc($_[0])) {
		return wantarray ? @{$c->{'values'}} : $c->{'values'}->[0];
		}
	}
return wantarray ? ( ) : undef;
}

# restart_plex()
# Re-starts the Plex server, and returns an error message on failure or
# undef on success.
sub restart_plex
{
if ($config{'restart_cmd'}) {
	local $out = `$config{'restart_cmd'} 2>&1 </dev/null`;
	return "<pre>$out</pre>" if ($?);
	}
else {
	local $pid = &get_plex_pid();
	$pid || return $text{'apply_epid'};
	&kill_logged('HUP', $pid);
	}
return undef;
}

# stop_plex()
# Kills the Plex server, and returns an error message on failure or
# undef on success.
sub stop_plex
{
if ($config{'stop_cmd'}) {
	local $out = `$config{'stop_cmd'} 2>&1 </dev/null`;
	return "<pre>$out</pre>" if ($?);
	}
else {
	local $pid = &get_plex_pid();
	$pid || return $text{'apply_epid'};
	&kill_logged('TERM', $pid);
	}
return undef;
}

# start_plex()
# Attempts to start the Plex server, returning undef on success or an error
# message on failure.
sub start_plex
{
# Remove PID file if invalid.
if (-f $config{'pid_file'} && !&check_pid_file($config{'pid_file'})) {
	&unlink_file($config{'pid_file'});
	}
if ($config{'start_cmd'}) {
	$out = &backquote_logged("$config{'start_cmd'} 2>&1 </dev/null");
	if ($?) { return "<pre>$out</pre>"; }
	}
else {
	$out = &backquote_logged("$config{'plex_path'} 2>&1 </dev/null");
	if ($?) { return "<pre>$out</pre>"; }
	}
return undef;
}

# get_pid_file()
# Returns the Plex server PID file.
sub get_pid_file
{
local $conf = &get_plex_config();
local $pidfile = &find_value("pidfile", $conf);
$pidfile ||= $config{'pid_file'};
return $pidfile;
}

# get_plex_pid()
# Returns the PID of the running Plex process.
sub get_plex_pid
{
local $file = &get_pid_file();
if ($file) {
	return &check_pid_file($file);
	}
else {
	local ($rv) = &find_byname("plex");
	return $rv;
	}
}

1;

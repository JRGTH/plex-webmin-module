#!/usr/local/bin/perl
# plex-lib.pl
# Common functions for the Plex daemon

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();

# get_plex_version()
sub get_plex_version
{
my $getversion = "$config{'version_cmd'}";
my $version = `$getversion`;
}

# get_plex_stats()
sub get_plex_stats
{
my $getplexstat = 'pgrep "Plex Media"';
my $plexstatus = `$getplexstat`;
}

# get_dlna_stats()
sub get_dlna_stats
{
my $getdlnastat = 'pgrep "Plex DLNA"';
my $dlnastatus = `$getdlnastat`;
}

# get_tuner_stats()
sub get_tuner_stats
{
my $gettunerstat = 'pgrep "Plex Tuner"';
my $tunerstatus = `$gettunerstat`;
}

# get_stat_icons()
sub get_stat_icons
{
my $okicon = "/images/ok.gif";
}

# get_local_ipaddress()
sub get_local_ipaddress
{
my $ipaddress = &to_ipaddress(get_system_hostname());
}

# Kill Plex related processes.
sub kill_plex_procs
{
my $getplexprocs = 'pkill -U plex';
my $killplexprocs = `$getplexprocs`;
}

# restart_plex()
# Re-starts the Plex server, and returns an error message on failure or
# undef on success.
sub restart_plex
{
if ($config{'restart_cmd'}) {
	local $out = `$config{'restart_cmd'} 2>&1 </dev/null`;
	return "<pre>$out</pre>" if ($?);
	# Wait few secs for Plex services to populate.
	sleep (3);
	}
else {
	# Just kill plex related processes and start Plex.
	kill_plex_procs;
	if ($config{'start_cmd'}) {
	$out = &backquote_logged("$config{'start_cmd'} 2>&1 </dev/null");
	if ($?) { return "<pre>$out</pre>"; }
	# Wait few secs for Plex services to populate.
	sleep (3);
		}
	}
return undef;
}

# stop_plex()
# Always use stop command whenever possible, otherwise
# try to kill the Plex server, returns an error message on failure or
# undef on success.
sub stop_plex
{
if ($config{'stop_cmd'}) {
	local $out = `$config{'stop_cmd'} 2>&1 </dev/null`;
	return "<pre>$out</pre>" if ($?);
	}
else {
	# Just kill Plex related processes.
	kill_plex_procs;
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
	# Wait few secs for Plex services to populate.
	sleep (3);
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
$pidfile = $config{'pid_file'};
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
	local ($rv) = &find_byname("Plex Media");
	return $rv;
	}
}

1;

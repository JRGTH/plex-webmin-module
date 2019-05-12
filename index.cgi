#!/usr/local/bin/perl
# index.cgi
# Display Plex option categories

require './plex-lib.pl';

# Check if config file exists.
if (!-r $config{'plex_config'}) {
	&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1);
	print &text('index_econfig', "<tt>$config{'plex_config'}</tt>",
		"$gconfig{'webprefix'}/config.cgi?$module_name"),"<p>\n";
	&ui_print_footer("/", $text{"index"});
	exit;
	}

# Check if Plex exists.
if (!&has_command($config{'plex_path'})) {
	&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1);
	print &text('index_eplex', "<tt>$config{'plex_path'}</tt>",
		"$gconfig{'webprefix'}/config.cgi?$module_name"),"<p>\n";
	&ui_print_footer("/", $text{"index"});
	exit;
	}

# Get Plex version.
my $version = &get_plex_version();
if (!$config{'version_cmd'} == "blank") {
	# Display version.
	&write_file("$module_config_directory/version", {""},$version);
	&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1, 0,
		&help_search_link("plexmediaserver", "man", "doc", "google"), undef, undef,
		&text('index_version', "$text{'index_modver'} $version"));
	}
else {
	# Don't display version.
	&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1, 0,
		&help_search_link("plexmediaserver", "man", "doc", "google"), undef, undef,
		&text('index_version', ""));
}

# Get Plex status.
my $plexstatus = &get_plex_stats();

# Get DLNA status.
my $dlnastatus = &get_dlna_stats();

# Get Tuner status.
my $tunerstatus = &get_tuner_stats();

# Get status icons.
my $okicon = &get_stat_icons();

# Get local ip address.
my $ipaddress =  &get_local_ipaddress();

# Configure Plex ip address.
if (!$config{'plex_url'} == "blank") {
	# Set the user defined ip.
	$plexurl = "$config{'plex_url'}";
	}
else {
	# Set the system local ip.
	$plexurl = "http://$ipaddress:32400/web";
}

print &ui_columns_start([$text{'index_colitem'}, $text{'index_colinfo'}, $text{'index_colstat'}]);
# Display informative column if service is running.
if (!$plexstatus == "blank") {
	print &ui_columns_row(["<a href=$plexurl target=_blank>$text{'index_plexstat'}</a>",
	"<a href=/proc/edit_proc.cgi?$plexstatus>$text{'index_infopid'} $plexstatus</a>", "<img src=$okicon>",]);
	}
if (!$dlnastatus == "blank") {
	print &ui_columns_row(["<a href=$plexurl target=_blank>$text{'index_dlnastat'}</a>",
	"<a href=/proc/edit_proc.cgi?$dlnastatus>$text{'index_infopid'} $dlnastatus</a>", "<img src=$okicon>",]);
	}
if (!$tunerstatus == "blank") {
	print &ui_columns_row(["<a href=$plexurl target=_blank>$text{'index_tunerstat'}</a>",
	"<a href=/proc/edit_proc.cgi?$tunerstatus>$text{'index_infopid'} $tunerstatus</a>", "<img src=$okicon>",]);
	}
print &ui_columns_end();

# Check if plex is running.
$pid = &get_plex_pid();
print &ui_hr();
print &ui_buttons_start();
if ($pid) {
	# Running .. offer to restart and stop.
	print &ui_buttons_row("stop.cgi", $text{'index_stop'}, $text{'index_stopmsg'});
	print &ui_buttons_row("restart.cgi", $text{'index_restart'}, $text{'index_restartmsg'});
	}
else {
	# Not running .. offer to start.
	print &ui_buttons_row("start.cgi", $text{'index_start'}, $text{'index_startmsg'});
	}
print &ui_buttons_end();

&ui_print_footer("/", $text{"index"});

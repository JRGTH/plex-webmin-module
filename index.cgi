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
$version = &get_plex_version();
&write_file("$module_config_directory/version", {""},$version);
&ui_print_header(undef, $text{'index_title'}, "", "intro", 1, 1, 0,
	&help_search_link("plexmediaserver", "man", "doc", "google"), undef, undef,
	&text('index_version', "$text{'index_modver'} $version"));

# Get Plex status.
$plexstatus = &get_plex_stats();

# Get DLNA status.
$dlnastatus = &get_dlna_stats();

print ui_columns_start([$text{'index_colitem'}, $text{'index_colinfo'}]);
# Display columns if requested information is available.
if (!$version == "blank") {
print ui_columns_row([$text{'index_plexver'}, $version,]);
	}
if (!$plexstatus == "blank") {
print ui_columns_row([$text{'index_plexstat'}, "$text{'index_infopid'} $plexstatus",]);
	}
if (!$dlnastatus == "blank") {
print ui_columns_row([$text{'index_dlnastat'}, "$text{'index_infopid'} $dlnastatus",]);
	}

print ui_columns_end();

# Check if plex is running.
$pid = &get_plex_pid();
print &ui_hr();
print &ui_buttons_start();
if ($pid) {
	# Running .. offer to apply changes and stop.
	print &ui_buttons_row("stop.cgi",
				$text{'index_stop'}, $text{'index_stopmsg'});
	print &ui_buttons_row("restart.cgi",
				$text{'index_restart'}, $text{'index_restartmsg'});
	}
else {
	# Not running .. offer to start.
	print &ui_buttons_row("start.cgi", $text{'index_start'},
				$text{'index_startmsg'});
	}
print &ui_buttons_end();

&ui_print_footer("/", $text{"index"});

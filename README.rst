Overview
--------
*snort* is a plugin for *nose* that reports success and failure via the Growl notification system.
The main difference from the older *nosegrowl* project:

* It uses *growlnotify* instead of a linked version of the Growl library. The older approach seems to be acting up strangely under OS X Lion. Using *growlnotify* works much smoother.
* It indicates skipped tests with a different icon, and writes the number of skipped tests in the notification window.
* It uses non-proprietary icons
* It's explicitly BSD licensed
* As the older project seems not to be under active support or development, *snort* is, and is open for opinions and feature requests ;-)


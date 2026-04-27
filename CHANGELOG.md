## 1.0.7
* Reworked community server detection
	* Previously detection would be performed AFTER first chat prompt was sent, causing the first prompt in valve servers to be prefixed with the community server fingerprint.
* Display connection status to make potential script failures easier to identify

## 1.0.6
* Automatically assumes server is community server until `status` confirmation
	* On community servers with increased playerlimit, first lines of `status` output can fail to register, causing failure to switch to community server fingerprint.

## 1.0.5
* Improved server connection handling
	* Now sends a `status` packet on script launch and waits for response before processing anything else, to detect community server if script is launched midgame
	* Blocks messages from being sent while connecting to a server, resets chat prompt cooldown upon connection success. First prompt will now send immediately after connection

## 1.0.4
* Added new script commands: `community_on` and `community_off`. Used to manually force community server compatibility mode on/off if it doesn't update automatically
	* Use script commands by typing the command in console directly (to prompt the `unknown command "(command)"` message), or by typing `echo (command)`
* Fixed terminal playing a system ding whenever server RTD commands are printed to chat (because of `\x07` character)

## 1.0.3
* Automatically detect when client connects to a community server and changes fingerprint to avoid server filter
	* Previously some servers would filter messages due to invalid characters in fingerprint
* Print cool header on script launch

## 1.0.2
* added epic hacker letters in code header
* no functional changes

## 1.0.1
* Prompt for tf/cs mode if script is launched with no arguments
    * Previously, if script was launched with no arguments it would just crash.

## 1.0.0
* First stable version!!
* Added update check

**THIS VERSION REQUIRES A NEW DEPENDENCY:** `requests`
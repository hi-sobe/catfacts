## 1.1.4
* New command `set_cooldown x`
	* Sets chat message cooldown to `x` seconds
	* Default value of 1 second will work in most circumstances, but prolonged spam at that value will fully lock you out of chat. Higher values will reduce chat timeout, but will also result in more commands not getting responses.
	* Script commands that require arguments must be ran with `echo (command) (args)`

## 1.1.3
* Added Schrodinger's cat
* Shortened sleeps from 500ms to 100ms to improve respoenseoveniss
* Added new keyword for command trigger patterns: `#CONSTRING`
	* Commands triggered by `#CONSTRING` will run every time the client connects to a new server.
* Update prompt now shows changelog for latest version

## 1.1.2
* Little bit of refactoring
* All chat functions except timed prompt now handled externally through /custom* modules

## 1.1.1 beta
* Added framework for better terminal output
	* Script now prints last few sent messages to terminal
	* Subscripts should now print to terminal using `console_log()` function instead of `print()`, as the latter will bust up my nice pretty printing
* Chat messages sent with `cat_message()` are now rate-limited to alleviate chat timeout when players spam commands
* Fixed certain chat outputs not being sent with cat_message

## 1.1.0 beta
* Python commands
	* Documentation available in README.md in `python commands` section
* **THIS IS A BETA RELEASE!** New features may have bugs, or may not behave as expected. Please report issues to me if you find them!

## 1.0.9
* Fixed CS2 support
	* Previous community server detection updates broke `cs` launch option, works now
	* Launching the script mid-match in CS2 no longer works, because it misses the server connection trigger.
	* To activate the script when launching it midgame, type `#CS_CONNECT` in game console.
* Added spinner for the loading bar :D

## 1.0.8
* Added framework to print script info in non-debug mode without spamming terminal
* Currently only shows connection status and progress bar for next chat prompt

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
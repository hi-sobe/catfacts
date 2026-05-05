![GATITO IMAGE](gatito.jpg)

CURRENT VERSION: 1.1.4\
[CHANGELOG](CHANGELOG.md)\
If you use this software, please report issues, feedback, suggestions to me on [STEAM](https://steamcommunity.com/id/isthatsobe/) or [EMAIL](mailto:sobefromgithub@gmail.com) me at sobefromgithub@gmail.com

## Dependencies
This script requires the following python libraries:
- keyboard
- pynput
- tkinter
- pathlib
- pyKey
- requests

You can install them with `pip install (dependency)`

## Setup
Both TF2 and CS2 require the following launch options in steam for this script to function:\
``-usercon -condebug -conclearlog``. The script uses these to read console output and parse chat messages.

When running the script for the first time in either mode, you will be prompted to set the path to your game's `console.log`. This file is automatically created after launching the game once with these launch options.

### TF2 setup:
TF2 requires these lines in your `autoexec.cfg` to start the rcon server:
```
rcon_password "[your rcon password]"
ip 0.0.0.0
net_start
hostport 27015
```
**IMPORTANT:** Set your rcon password to something unique. If someone has your rcon password AND your ip, they can remotely execute tf2 console commands on your client.

### CS2 setup:
In CS2, the script writes console commands to a config file, and simulates an `f13` keypress to execute that config.\
During setup, that config will be automatically created after you set the path to CS2's `console.log`.\
By default, the config file is named `sobecatfacts.cfg`. Add the following line to your `autoexec.cfg`:
```
bind f13 "exec sobecatfacts"
``` 
**NOTE:** Because it uses keybinds to send messages in CS2, the script **WILL NOT SEND MESSAGES** if you are alt-tabbed, have chat or console open, or any other situation that prevents keybind inputs from being processed. I recommend binding another key to run `sobecatfacts.cfg` so that you can send the last queued message manually if it failed to send.

## Usage
Everything in this repository is ready to run as-is. If you want to add custom commands, see the **Custom commands** and **Custom pattern-match commands** sections.

The script can be run in rcon mode for TF2, or in keybind mode for CS2. When you run it you **MUST** specify which mode using launch options:
`python cat.py tf` or `python cat.py cs`

If you want to silence the automatic prompts in chat, run it with the `s` launch option: `python cat.py tf s`

## Commands
You can run certain script commands by running `echo [command]` in the game console, or by saying them in chat.\
**CURRENTLY THESE COMMANDS CAN BE TRIGGERED BY ANY CHAT MESSAGE, FROM ANY USER!!**\
I plan to change this soon.

Currently supported commands:

| Command  | Function |
| :------------- |:-------------|
| killcat      | Shuts down the script     |
| cat_on      | Turns on automatic chat prompt     |
| cat_off      | Turns off automatic chat prompt     |
| listplayerids | Prints a list of all connected players + steamids |
| script_enable | Enables script - script can be automatically disabled if two instances are running on the same server. Use this to turn it back on. |
| script_disable | Disables the script. |
| community_on  | Forces community server compatibility mode on, to prevent chat messages from being filtered for invalid characters |
| community_off | Forces community server compatibility mode off (will be turned back on after every `status` command if on a community server) |

## Simple commands
**Simple commands are defined in the `/custom` folder.**\
Simple commands trigger with a phrase in chat, and print a random phrase from a selection.\
You can add custom trigger phrases by adding a .txt file to the `/custom` folder. The filename defines the chat command, and the contents of the file define the list of messages to randomly select from.

For example, `lizard.txt` in the `/custom` folder contains two lines:
```
Lizards are not cats!
I don't know anything about lizards!
```
When a player in your match types `!lizard`, the script will randomly select one of those two messages to send in chat.

## Simple pattern-match commands
**Pattern-match commands are defined in the `/custom_pattern` folder.**\
Pattern-match commands use python regex to find phrases in console output, and are **NOT** restricted to messages in chat. These can be used to trigger messages on certain game events, or to recognize more complex patterns in chat messages.

Unlike simple commands, the filename is not used by the script at all. The command trigger is instead defined by the first line of the file, with all following lines representing entries in the list of possible messages.

For example, `test.txt` in the `/custom_pattern` folder contains these lines:
```
sobescooltestcommand\d
this should trigger whenever a string matching "sobescooltestcommand(number)" is printed to console!
second entry!
third entry!
```
The first line defines the "trigger" pattern: `sobescooltestcommand\d`.\
This matches the exact phrase `sobescooltestcommand`, followed by any number (represented by `\d`).\
It will trigger if any matching phrase - `sobescooltestcommand1`, `sobescooltestcommand7`, etc - appear anywhere in any message printed to the console.

### Pattern keywords
| Keyword | Use |
| :--- | :--- |
| #CMDSTRING | Prefix for messages sent in chat by any player - prevents chat commands from being triggered by non-chat console output |
| #CONSTRING | Triggers once when the client connects to a server |

## Python commands
**Python commands are defined in the `/custom_py` folder.**\
Python commands use the same pattern system as simple pattern-match commands, but they require two files - a text (`.txt`) file for the patterns, and a matching python script (`.py`) for the code to be executed when those commands are matched in console output. 

**FORMAT:**
	* Filenames for patterns and code must match. `(xyz).txt` will only associate to `(xyz).py`, and if `(xyz).py` does not exist, the command will not register.
	* Python script for a command MUST register function `PAT_CMD(arg)`, with argument `arg` being the pattern which triggered the command as a string.

**USE:**
Command scripts have access to the FULL global environment of the main script - they can call any function defined anywhere in the script.

*USEFUL FUNCTIONS:*
| Function | Use |
| :------------- |:-------------|
| cat_message | say message in chat |
| cat_command | execute console commands (separate with `;`) |

*USEFUL VARIABLES:*
| Variable | Use |
| :------------- |:-------------|
| playerids | Array: list of connected usernames and steamids |

**WARNINGS!!**\
Command scripts are called with the `exec()` function, which means there is NO sandboxing or security. Code run through this system can break the script, or even break your computer.\
*ONLY USE THIS TO RUN CODE THAT YOU TRUST!!*

Command scripts have full access to the global namespace, variables defined in command scripts can overwrite variables defined in the main script, potentially breaking it.
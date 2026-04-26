## Dependencies
This script requires the following python libraries:
- keyboard
- pynput
- tkinter
- pathlib
- pyKey

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
**NOTE:** Because it uses keybinds to send messages in CS2, the script **WILL NOT SEND MESSAGES** if you are alt-tabbed, have chat or console open, or any other situation that prevents keybind inputs from being processed. I recommend binding another key to run `sobecatfacts.cfg` so that you can send the last queued message manually if someone missed theirs.

## Usage
Everything in this repository is ready to run as-is.

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
| caton      | Turns on automatic chat prompt     |
| catoff      | Turns off automatic chat prompt     |
| listplayerids | Prints a list of all connected players + steamids |
| script_enable | Enables script - script can be automatically disabled if two instances are running on the same server. Use this to turn it back on. |
| script_disable | Disables the script. |

## Custom commands
This script currently only supports custom commands in the same format as the original !cat command - trigger with a phrase in chat, and print a random phrase from a selection.\
You can add custom trigger phrases by adding a .txt file to the `/custom` folder. The filename defines the chat command, and the contents of the file define the list of messages to randomly select from.

For example, `lizard.txt` in the `/custom` folder contains two lines:
```
Lizards are not cats!
I don't know anything about lizards!
```
When a player in your match types `!lizard`, the script will send one of those two messages in chat, randomly selected.

## Custom pattern-match commands
Pattern-match commands use python regex to find phrases in console output, and are **NOT** restricted to messages in chat.\
These can be used to trigger messages on certain game events, or to recognize more complex patterns in chat messages.

Unlike standard custom commands, the filename is not used by the script at all. \
The command trigger is instead defined by the first line of the file, with all following lines representing entries in the list of possible messages.

For example, `test.txt` in the `/custom_pattern` folder contains these lines:
```
sobescooltestcommand\d
this should trigger whenever a string matching "sobescooltestcommand(number)" is printed to console!
second entry!
third entry!
```
The first line defines the "trigger" pattern: `sobescooltestcommand\d`.\
This matches the exact phrase `sobescooltestcommand`, followed by any number. It will trigger if the phrase `sobescooltestcommand1`, `sobescooltestcommand7`, etc are printed to console.

**IMPORTANT**: This will not be restricted to chat messages, it will trigger if that phrase appears in ANY console output!\
If you want to restrict it to only chat messages, start the pattern with `:  .*` (TWO spaces)
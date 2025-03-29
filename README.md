MoveText
========

Select text and move it around using the keyboard, or setup a text "tunnel" to move code from one location to another.

Installation
------------

Using Package Control, install "MoveText" or clone this repo in your packages folder.

I recommended you add key bindings for the commands. I've included my preferred bindings below.
Copy them to your key bindings file (⌘⇧,).

Commands
--------

`move_text_left`: Moves the selected text one character to the left

`move_text_right`: Moves the selected text one character to the right

`move_text_up`: Moves the selected text one line up

`move_text_down`: Moves the selected text one line down

When moving text up and down, funny things happen when the destination line doesn't have enough preceding characters.  An attempt *is made* to keep the text on the same column, but the mechanism for this uses `sublime.View.command_history`, which doesn't update after every movement.  It updates in between "Undo" events, so if you move the text in the opposite direction, or if you pause long enough for an "undo" to register, the text will move correctly.  It looks like this:

    1. one*dragme*  1. one          1. one       1. one
    2. two          2. two*dragme*  2. two       2. two
    3.              3.              3. *dragme*  3.
    4. four         4. four         4. four      4. *dragme*four

But if you move the text *up* first, it will move correctly:

    1. one          1. one*dragme*  1. one          1. one       1. one
    2. two*dragme*  2. two          2. two*dragme*  2. two       2. two
    3.              3.              3.              3. *dragme*  3.
    4. four         4. four         4. four         4. four      4. fou*dragme*r

Key Bindings
------------

Copy these to your user key bindings file.

<!-- keybindings start -->
    { "keys": ["super+ctrl+left"], "command": "move_text_left" },
    { "keys": ["super+ctrl+right"], "command": "move_text_right" },
    { "keys": ["super+ctrl+up"], "command": "move_text_up" },
    { "keys": ["super+ctrl+down"], "command": "move_text_down" },
<!-- keybindings stop -->

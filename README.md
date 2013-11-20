MoveText
========

Select text and move it around using the keyboard, or setup a text "tunnel" to move code from one location to another.

Installation
------------

1. Using Package Control, install "MoveText"

Or:

1. Open the Sublime Text Packages folder
    - OS X: ~/Library/Application Support/Sublime Text 3/Packages/
    - Windows: %APPDATA%/Sublime Text 3/Packages/
    - Linux: ~/.Sublime Text 3/Packages/ or ~/.config/sublime-text-3/Packages

2. clone this repo
3. Install keymaps for the commands (see Example.sublime-keymap for my preferred keys)

### Sublime Text 2

1. Open the Sublime Text 2 Packages folder
2. clone this repo, but use the `st2` branch

       git clone -b st2 git@github.com:colinta/SublimeMoveText

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

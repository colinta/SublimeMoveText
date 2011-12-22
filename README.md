MoveText plugin for Sublime Text 2
==================================

Installation
------------

1. Open the Sublime Text 2 Packages folder

    - OS X: ~/Library/Application Support/Sublime Text 2/Packages/
    - Windows: %APPDATA%/Sublime Text 2/Packages/
    - Linux: ~/.Sublime Text 2/Packages/

2. clone this repo

Commands
--------

`move_text_left`: Moves the selected text one character to the left
`move_text_right`: Moves the selected text one character to the right
`move_text_up`: Moves the selected text one line up
`move_text_down`: Moves the selected text one line down

When moving text up and down, funny things happen when the destination line doesn't
have enough preceding characters.  It looks like this:

    1. one*dragme*  1. one          1. one       1. one
    2. two          2. two*dragme*  2. two       2. two
    3.              3.              3. *dragme*  3.
    4. four         4. four         4. four      4. *dragme*four`


Once the text gets forced to the 0<sup>th</sup> column, it stays there.  I would like to add a mechanism that saves the initial column, but I'm not sure how it would be reset.

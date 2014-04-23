Introduction:
    This plugin is fairly simple, and is meant to be used to format text to a
    fixed width while still maintaining clean formatting in places (often web
    forms or emails) that will not preserve it. The plugin copies whatever text
    is in the current document and will copy a formatted version below it. The
    formatted version will split lines when they exceed the defined maximum
    allowed columns and will ensure the newly created line preserves the
    indentation.

Example:
    A trivial example of what this plugin does follows below. Consider the
    following piece of text:
    
    <example>
    *This is some example text that will exemplify the effect of this plugin.*
    
    *Look at this list:*
        *1. blah blah blah blah blah blah blah blah blah blah*
        
        *2. hello world!*
    </example>
    
    If the plugin is run and a small column width is provided as a parameter,
    the output may be:
    
    <output>
    *This is some example text that will exemplify*
    *the effect of this plugin.*
    
    *Look at this list:*
        *1. blah blah blah blah blah blah blah blah*
        *blah blah*
        
        *2. hello world!*
    </output>

There are a few files of interest:
    1. formatter.py: This is the actual plugin, which does all the text
    manipulation
    2. Default (*).sublime-keymap: These are key map files, which control the
    shortcut to run the plugin

Installation:
    1. Move the "FixedWidthFormatter" folder the Sublime "Packages" directory.
    For example:
        (OSX)
        /Users/{$USERNAME}/Library/Application Support/Sublime Text 2/Packages

        (WINDOWS)
        C:\Documents and Settings\{$USERNAME}\Application Data\Sublime
        Text\Packages\User

    2. Modify the existing .sublime-keymap files to include an entry that
    matches one of the .sublime-keymap files packaged with this plugin


Usage Notes:
    Write a document like you normally would. For each line written (e.g., a
    line ending with the whitespace character '\n') make sure that the
    indentation you want is being used (e.g, 1 space, a tab, a combination of
    those, or more) and do not worry about manually breaking lines to keep the
    formatting preserved. The plugin will do that for you. Then run the plugin
    using whatever keybinding you choose.

    By default the text will be formatted to be at most 80 columns wide.
    However, this is customizable if you launch the plugin with arguments. To
    my knowledge, you can do this in two ways:
        1. Through the Sublime Text 2 console (ctrl + `) like so:
            view.run_command("fixed_width",{"numCols":<some integer>})

        2. Through a keybinding. This can be done by adding an "args" parameter
        like so:
            [
                {
                    "keys": ["command+shift+f"],
                    "command": "fixed_width",
                    "args": {"numCols": "60"}
                }
            ]


Enjoy!
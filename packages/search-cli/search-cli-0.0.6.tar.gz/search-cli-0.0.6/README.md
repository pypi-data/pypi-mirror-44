# Search CLI

<!---[![Build Status](https://travis-ci.com/blester125/search_cli.svg?branch=master)](https://travis-ci.com/blester125/search_cli)--->

Small tools to interface with search engine form the command line that has tight integration with the linux X clipboard.

For python 3 installs:

`sudo apt install surfraw surfraw-extra xclip python3-tk`

For python 2

`sudo apt install surfraw surfraw-extra xclip python-tk`

install with `pip install .` or `pip install search-cli`

Programs:

 * `search` or `sr`: Search from the command line with a backoff to search for what ever is on your clipboard if you don't type anything
 * `search_highlighted`: Search for the highlighted span.
 * `search_gui`: Create a text input box and search for entered text with `<Enter>`
 * `search_gui_highlighted`: Same as above but seeded with the currently highlighted text.

`search_highlighted`, `search_gui`, and `search_gui_highlighted` are ideal for keybinding.

When the search bar loses focus (you click away) it will automatically close. If you don't like this behavior you can set `SR_CLOSE_LOSS_FOCUS` to `no` to stop it.

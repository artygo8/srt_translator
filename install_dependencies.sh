#!/bin/bash

GRN_PRINTF = printf "\033[32m%s\e[m\n"

for lib in 'chime' 'selenium' 'pyperclip'; do
    python3 -c "import $lib" && ${GRN_PRINTF} "$lib installed" || python3 -m pip install $lib
done

brew install geckodriver
brew install firefox

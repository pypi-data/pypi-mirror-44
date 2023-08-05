# rcrepl - A remote control for REPLs

This is a python script that wraps some REPL's and compilers and enables controlling them via commands sent to a network socket.
This is meant to provide a rapid compile/feed back loop in supported text editors.

Right now supported REPLs/compilers are 

1. Haskell GHCI 
2. ELM compiler

The supported editors are

1. VIM (>= 8.0)
2. Neovim

## Installing

```
pip3 install rcrepl
```

## Using with GHCI + VIM

1 . Set custom ghci prompt

Typically this is done from the `.ghci` file in your home folder. So add the following line to it.

```
:set prompt RCGHCIPROMPT>>>
```
2 . Add the following VimL functions to your .vimrc. These can be customized and decides what happens on the editor when there 
is a build success, warnings, errors or an activity in REPL.

```
function! RCREPLIndicateError()
  hi StatusLine ctermfg=black guibg=black ctermbg=red guifg=#fc4242
endfunction

function! RCREPLIndicateWarnings()
  hi StatusLine ctermfg=black guibg=black ctermbg=yellow guifg=#84ff56
endfunction

function! RCREPLIndicateSuccess()
  hi StatusLine ctermfg=black guibg=black ctermbg=green guifg=#087e3b
endfunction

function! RCREPLIndicateActivity()
  hi StatusLine ctermfg=black guibg=black ctermbg=brown guifg=orange
endfunction
```

3 . Set vim to send a reload command to port 1880 on save of a .hs file

```
function! Ghci(command)
  let ch = ch_open('localhost:1880', {'mode':'raw'})
  ch_evalraw(ch, a:command)
endfunction

function! ReloadGHCI()
  call Ghci(":reload")
endfunction

autocmd BufWritePost *.hs call ReloadGHCI()
```

4 . Start Vim with a explicitly set servername as follows

```
vim --servername VIMMASTER 
```

5 . Go to your project root and run

```
export RCREPL_PORT=1880 && export VIM_SERVERNAME=VIMMASTER && export RCGHCI_PROMPT='RCGHCIPROMPT>>>' && rcghci vim
```

This starts a `stack ghci` process and you will be able to see it's output at the terminal. If you have arguments that should be passed to `stack ghci` command, pass them after the command, for example...

```
export RCREPL_PORT=1880 && export VIM_SERVERNAME=VIMMASTER && export RCGHCI_PROMPT='RCGHCIPROMPT>>>' && rcghci vim --ghci-options "+RTS -M3G -RTS"
```

Now if you open a haskell source file
in the editor, you will see the GHCI reloading on file save. If the file you are editing is part of the project, then the status line will switch colors when there is a command being run, if there are errors, warning or if it was successful.

If there are errors, the vim's error list will be populated with them. You can open this error list window using the ":cope" command. Once in the error list window, you will be able to jump to error locations by pressing enter when the cursor is on the first line of the error.


## Using with GHCI + Neovim

The procedure is mostly the same, with the following difference in step 3 to 5.

3 . Set neovim to send a reload command to port 1880 on save of a .hs file

```
function! Ghci(command)
  let ch = sockconnect("tcp", "127.0.0.1:1880")
  call chansend(ch, a:command)
endfunction

function! ReloadGHCI()
  call Ghci(":reload")
endfunction

autocmd BufWritePost *.hs call ReloadGHCI()
```

4 . Start Neovim with explicitly set listen address

```
neovim --listen /tmp/nvimmaster
```

5 . Go to your project root and run

```
export RCREPL_PORT=1880 && export NVIM_LISTEN_ADDRESS=/tmp/nvimmaster && export RCGHCI_PROMPT='RCGHCIPROMPT>>>' && rcghci nvim
```
If you have arguments that should be passed to `stack ghci` command, pass them after the command, for example...

```
export RCREPL_PORT=1880 && export NVIM_LISTEN_ADDRESS=/tmp/nvimmaster && export RCGHCI_PROMPT='RCGHCIPROMPT>>>' && rcghci nvim --ghci-options "+RTS -M3G -RTS"
```

Also, if you are running this from a terminal inside of Neovim, then the NVIM_LISTEN_ADDRESS seems to be already defined. So it should be possible
for you to skip the `export NVIM_LISTEN_ADDRESS=/tmp/nvimmaster`. In that case, you can also skip the `--listen` argument while starting neovim.


## Using with ELM

The elm component does not wrap an REPL, but just the `make` command. So it just run the `elm make` command, and sends the errors back to the editor.

```
export RCREPL_PORT=1890 && rcelm vim src/Main.elm --output ../Analytics.js
```

```
export RCREPL_PORT=1890 && rcelm nvim src/Main.elm --output ../Analytics.js
```

### For elm 0.18

```
export RCREPL_PORT=1890 && rcelm18 vim src/Main.elm --output ../Analytics.js
```

```
export RCREPL_PORT=1890 && rcelm18 nvim src/Main.elm --output ../Analytics.js
```
The `--report` flag is passed to the binary, so apart from that, you can pass any additional flag by just including them after the command.


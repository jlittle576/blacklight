#!/bin/sh
cd /C/Users/JoesDesktop/Dropbox/code/projects/blacklight
git init
git add '.'
git commit -m "first commit"
git remote add origin git@github.com:jlittle576/blacklight.git
git push -u origin master
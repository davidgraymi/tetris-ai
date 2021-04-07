#!/bin/zsh

read -p "Enter commit message: " message

printf "\e[33m\nPushing to tetris-ai repository...\e[39m\n\n"
git add .
git commit -m "$message"
git push

printf "\e[32m\nSuccessfully deployed!\e[39m"
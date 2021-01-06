#!/bin/bash
# Clean up personal data before pushing to GitHub
# Colors
red="\e[0;91m"
blue="\e[0;94m"
expand_bg="\e[K"
blue_bg="\e[0;104m${expand_bg}"
red_bg="\e[0;101m${expand_bg}"
green_bg="\e[0;102m${expand_bg}"
green="\e[0;92m"
white="\e[0;97m"
bold="\e[1m"
uline="\e[4m"
reset="\e[0m"
#####

declare -a removeArray
removeArray=( [0]=Rechnungen [1]=__pycache__ [2]=*.csv)
for f in "${removeArray[@]}"; do
  echo -e "${red}Removing files or folders: $f${reset}"
  rm -rf $f
done
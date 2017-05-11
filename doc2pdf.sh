#!/usr/bin/env bash

if ! type soffice > /dev/null; then
    echo "command soffice is not exist, you can install it by the following command:"
    case "$(uname -s)" in
       Darwin)
         echo '- brew cask install libreoffice'
         ;;
       Linux)
         echo 'Linux'
         ;;

       CYGWIN*|MINGW32*|MSYS*)
         echo 'MS Windows'
         ;;
       *)
         echo 'other OS'
         ;;
    esac
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "No arguments provided"
    exit 1
fi

if [ ! -f $1 ]; then
    echo $1 "File not found!"
else
   soffice --headless --convert-to pdf $1 --outdir $2
fi

exit 0
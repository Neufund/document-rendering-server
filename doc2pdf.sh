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

for FILE1 in "$@"
do
    if [ ! -f $FILE1 ]; then
        echo $FILE1 "File not found!"
    else
       soffice --headless --convert-to pdf $FILE1 --outdir converted
    fi
done
exit 0
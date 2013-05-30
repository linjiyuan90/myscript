#!/bin/bash
# convert a unknown encoding file to UTF8.
# This script support recursively convert.
# Usage:
#  ./convert2utf8.sh dir_a file_a dir_b

# Note:
# Encoding detected by file may not be correct, and lead to
# bad convert!
# Alternative is open the file with vim, "set fileencoding"
# you will get the encoding!

echoerr() {
  echo $* >&2
  # or
  # echo $* >/dev/stderr
  # echoerr xxx 2>log
}

to=tmp

convert() {
    for x in "$@"
    do
        if [ -d "$x" ];then
            IFS=$'\n'   # noted
            convert `ls -d "$x"/*`
            continue
        fi
        # try different encoding --!
        ok=0
        for encoding in gbk gb18030 euc-cn `file "$x" --mime-encoding -b`
        do
            # echo -e converting "$x" ... 
            iconv -f $encoding -t utf-8 "$x" >$to
            if [ $? -eq 0 ]; then
                mv $to "$x"
                # echo done
                ok=1
                break
            fi
        done
        if [ $ok -eq 0 ]; then
            echoerr Can\'t convert: "$x", encoding: $encoding
        fi
    done
}

convert "$@"
rm $to

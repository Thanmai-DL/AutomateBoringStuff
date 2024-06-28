#!/bin/bash
info=()
while IFS= read -r line; do info+=("$line"); done < info.txt

if [ ${#info[@]} -eq 6 ];then
	position=${info[4]}
	company=${info[5]}
else
	position=${info[3]}
	company=${info[4]}
fi

first=$(echo "${info[0]}" | awk '{print toupper(substr($0, 1, 1)) substr($0, 2)}')
subject="Request for Interview: Applying for $position at $company!"

sed -e "s/\[Name\]/$first/g" -e "s/\[Position\]/$position/g" -e "s/\[Company\]/$company/g" template.html > message.html

if [ ${#info[@]} -eq 6 ];then
	python3.12 compose.py ${info[0]} ${info[1]} ${info[2]} ${info[3]} "$subject"
elif [ ${#info[@]} -eq 5 ];then
	python3.12 compose.py ${info[0]} ${info[1]} ${info[2]} "$subject"
else
	echo "Invalid enties in info.txt"
fi
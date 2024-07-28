#!/bin/bash

# Function to generate message.html for the body and subject for the email
message() {
    sed -e "s/\[Name\]/$1/g" -e "s/\[Position\]/$2/g" -e "s/\[Company\]/$3/g" template.html > message.html
    echo "Request for Interview: Applying for $2 at $3!"
}

info=()
# Read info.txt
while IFS= read -r line; do info+=("$line"); done < info.txt
# Capitalize the first letter of firstname
first=$(echo "${info[0]}" | awk '{print toupper(substr($0, 1, 1)) substr($0, 2)}')

case ${#info[@]} in
    6)
        subject=$(message "$first" "${info[4]}" "${info[5]}")
        python3.12 compose.py "${info[0]}" "${info[1]}" "${info[2]}" "${info[3]}" "$subject"
        ;;
    5)
        subject=$(message "$first" "${info[3]}" "${info[4]}")
        python3.12 compose.py "${info[0]}" "${info[1]}" "${info[2]}" "$subject"
        ;;
    4)
        subject=$(message "$first" "${info[2]}" "${info[3]}")
        python3.12 compose.py "${info[1]}" "$subject"
        ;;
    *)
        echo "Invalid entries in info.txt"
        ;;
esac
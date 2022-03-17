#!/usr/bin/bash

# This script is used for automating the process of updating patch numbers.
# Specifically, it updates the version number in setup.cfg (Line 3) and setup.py (Line 12 & 13)
# You can provide the script with either major, minor or patch (Case sensitive)
# Example usage:
# If the current version is 1.4.0, running './updateVersion.sh major' will change
# the current version to 2.0.0

if [ "$1" = "" ]; then
echo "You must provide an argument for this script"
echo "Your argument must be either major, minor or patch"
echo "See version semantics for more"
exit
fi

if [ "$1" != "major" ] && [ "$1" != "minor" ] && [ "$1" != "patch" ]; then
echo "Incorrect argument provided"
echo "Your argument must be either major, minor or patch (Case sensitive)"
exit
fi

VERSION_STRING=$(cat setup.cfg | grep "version")

IFS=' '
read -ra VERSION_STRING_ARR <<< $VERSION_STRING

VERSION="${VERSION_STRING_ARR[@]:2:2}"

echo "Current Version: $VERSION"

IFS='.'

read -ra VERSION_NUMBERS <<< $VERSION

MAJOR=${VERSION_NUMBERS[@]::1}
MINOR=${VERSION_NUMBERS[@]:1:1}
PATCH=${VERSION_NUMBERS[@]:2:2}

if [ "$1" = "major" ]; then
PATCH="0"
MINOR="0"
MAJOR=$(( $MAJOR + 1))
fi

if [ "$1" = "minor" ]; then
PATCH="0"
MINOR=$(( $MINOR + 1))
fi

if [ "$1" = "patch" ]; then
PATCH=$(( $PATCH + 1))
fi

UPDATED_VERSION="${MAJOR}.${MINOR}.${PATCH}"

echo "Updated Version: $UPDATED_VERSION"

sed -i "s/version = ${VERSION}/version = ${UPDATED_VERSION}/" setup.cfg
sed -i "s/^    version=\"${VERSION}\",/    version=\"${UPDATED_VERSION}\",/" setup.py
sed -i "s/^    download_url=\"https:\/\/github.com\/Milind220\/Ozone\/archive\/refs\/tags\/v${VERSION}.tar.gz\",/    download_url=\"https:\/\/github.com\/Milind220\/Ozone\/archive\/refs\/tags\/v${UPDATED_VERSION}.tar.gz\",/" setup.py

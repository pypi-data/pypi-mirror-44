#$/bin/bash

# This script creates new tag and adds changelog to CHANGELOG.rst.

# Creating new tag for gitchangelog
sed -i -E 's/__version__ = .[0-9]+\.[0-9]+\.[0-9]./__version__ = \"'"$1"'\"/g' netssh2/__init__.py;
git commit netssh2/__init__.py -m "Version bump to $1";
git tag -a $1 -m "$2";
# Updating changelog
gitchangelog;
git tag -d $1;
git reset --soft HEAD~1;
# Updating MANIFEST.IN
rm -f MANIFEST.in
check-manifest -c;
# Version bump commit
git commit netssh2/__init__.py CHANGELOG.rst MANIFEST.in -m "Version bump to $1";
git tag -a $1 -m "$2";
git push --follow-tags;


#!/bin/bash
set -e -u -o pipefail

# (In contrast, implicitly discovered files which produce ImportErrors are ignored.)
git ls-files listentweet | grep -e "\.py$" | xargs pytest --doctest-modules

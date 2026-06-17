#!/usr/bin/env bash
set -e

PR_ID="$1"

if [ -z "$PR_ID" ]; then
    echo "Usage: $0 <pr-id>"
    exit 1
fi

echo "#### Installing clients ####"

if [ ! -d "master/.git" ]; then
    echo ""
    echo "### Downloading master ###"
    git clone git@github.com:ddnet/ddnet.git master
    cd master
    git submodule update --init
    mkdir build
    mv storage.cfg build
    cd ..
fi

if [ ! -d "PR-${PR_ID}/.git" ]; then
    echo ""
    echo "### Downloading PR ${PR_ID} ####"
    cp -r master "PR-${PR_ID}"
    cd "PR-${PR_ID}"
    git fetch origin "pull/${PR_ID}/head:pr-${PR_ID}"
    git checkout "pr-${PR_ID}"
    #  no need to create build directory, because this is already copied
    cd ..
fi

echo ""
echo "#### Configuring clients ####"
python3 scripts/configure-clients.py vulkan master
python3 scripts/configure-clients.py vulkan "PR-${PR_ID}"


echo "#### Setting up demos and configs ####"
python3 scripts/setup-demos.py master
python3 scripts/setup-demos.py "PR-${PR_ID}"

echo ""
echo "#### Collecting frametimes ####"
python3 scripts/create-benchmarks.py master
python3 scripts/create-benchmarks.py "PR-${PR_ID}"

echo ""
echo "#### Collecting results ####"
python3 scripts/collect-data.py master "results-${PR_ID}"
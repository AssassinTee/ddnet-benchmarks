#!/usr/bin/env bash
set -e

mkdir -p clients
mkdir -p results

echo "#### Installing clients ####"
python3 scripts/install-clients.py client-list.json

echo ""
echo "#### Setting up demos and configs ####"
python3 scripts/setup-demos.py

echo ""
echo "#### Collecting frametimes ####"
python3 scripts/create-benchmarks.py

echo ""
echo "#### Collecting results ####"
python3 scripts/collect-data.py

echo ""
echo "#### Checking results for validity ####"
python3 scripts/check-results.py
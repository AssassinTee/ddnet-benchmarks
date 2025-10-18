#!/usr/bin/env bash
set -e

mkdir clients
mkdir results

echo "#### Installing clients ####"
python scripts/install-clients.py client-list.json

echo ""
echo "#### Setting up demos and configs ####"
python scripts/setup-demos.py

echo ""
echo "#### Collecting frametimes ####"
python scripts/create-benchmarks.py

echo ""
echo "#### Collecting results ####"
python scripts/collect-data.py

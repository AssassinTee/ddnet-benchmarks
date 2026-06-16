# DDNet-Benchmarks

Small repository creating and maintaining ddnet benchmarks

## Method

Goal is to download and benchmark a selection of demos for multiple client versions and graph some nice metrics.
In order to prevent other factors, we benchmark demos of online gameplay and not online gameplay itself in order to prevent lag, random text rendering (due to chat/server messages) and other influences.
All benchmarks are collected in a 30 second demo clip from the beginning and the collection stops after 30 seconds automatically (even if the demo is longer).

## Selected maps

See [resources](https://github.com/AssassinTee/ddnet-benchmark-resources/blob/main/README.md)

## Create benchmarks

- Download the demos and configs with `git submodule update --init`
- Select and download the clients you want to benchmark by modifying `client-list.json`
- run `./create-benchmarks.sh`, which will
  - install all clients from the list
  - install demos and configurations for frametime collection
  - collect frametimes
  - collect results in the `results` directory
- Run the [DDNet_Benchmarking](DDNet_Benchmarking.ipynb) notebook in order to visualize the data and calculate some nice graphs

## Installation

- Install python3
- Install packages with `pip install -r requirements.txt`
- Use any Jupyter server (like for example [Google Colab](https://colab.research.google.com/) or similar) to visualize the collected data

## Results

![AverageFPS.PNG](AverageFPS.png)

#!/usr/bin/env bash
# Склейка кадров (120 в секунду, 2 подкадра) в 60 fps с размытием движения + лёгкая копия
# bash encode.sh <имя> <ширина_лёгкой>x<высота_лёгкой>   пример: bash encode.sh promo 1280x720
NAME=${1:-film}; SMALL=${2:-1280x720}
mkdir -p results
ffmpeg -y -v error -framerate 120 -i frames/s%05d.jpg -i mix.wav \
  -vf "tmix=frames=2:weights='1 1',select='eq(mod(n\,2)\,1)',setpts=N/(60*TB),format=yuv420p" \
  -r 60 -c:v libx264 -preset slow -crf 17 -c:a aac -b:a 256k -shortest -movflags +faststart "results/$NAME.mp4"
ffmpeg -y -v error -i "results/$NAME.mp4" -vf "scale=${SMALL/x/:}" -c:v libx264 -preset slow -crf 23 -c:a aac -b:a 160k -movflags +faststart "results/${NAME}_phone.mp4"
ls -la results/$NAME*.mp4

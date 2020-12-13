#!/bin/bash

# This script cleans all cache for Microsoft Teams on Linux
# Tested on Ubuntu only. Feel free to test/use in other distributions.

cd "$HOME"/.config/Microsoft/Microsoft\ Teams || exit 1

#Microsoft teamsを起動
sleep 5
teams

#10秒待ってからキャッシュクリーン
sleep 10

# Test if Microsoft Teams is running
if [ "$(pgrep teams | wc -l)" -gt 1 ]
then
  rm -rf Application\ Cache/Cache/*
  rm -rf blob_storage/*
  rm -rf databases/*
  rm -rf GPUCache/*
  rm -rf IndexedDB/*
  rm -rf Local\ Storage/*
  rm -rf tmp/*
  rm -rf Cache/*
  #rm -rf backgrounds/*
  find ./ -maxdepth 1 -type f -name "*log*" -exec rm {} \;
  sleep 5
  killall teams
  # After this, MS Teams will open again.
else
  echo "Microsoft Teams is not running."
  exit
fi

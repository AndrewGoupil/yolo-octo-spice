#! /usr/bin
mplayer http://204.178.9.51$(curl --data "voice=crystal&txt=$@&speakButton=SPEAK" "http://204.178.9.51/tts/cgi-bin/nph-nvttsdemo" |grep ".wav"|cut -d\" -f2)

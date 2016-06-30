#!/bin/bash


inputfile=/home/edipdemirbilek/Desktop/Input/ntia_HeadShoulders-Female15_original.avi
outputFilePrefix=/home/edipdemirbilek/Desktop/Output/ntia_HeadShoulders-Female15_h264_720p_baseline
logFile=/home/edipdemirbilek/Desktop/Output/output.log

aNR=( 999 0 )
aQuant=( 23 27 31 35 )
aFPS=( 25 20 15 10 )

for NR in "${aNR[@]}"
do
	for Quant in "${aQuant[@]}"
	do
		for FPS in "${aFPS[@]}"
		do	
			outputFile=$outputFilePrefix
			outputFile+=_fps$FPS
			outputFile+=_q$Quant
			outputFile+=_nr$NR
			outputFile+=_amrwb_m08.3gp

			time gst-launch-1.0 filesrc location=$inputfile ! decodebin name=demux ! queue ! videorate ! videoconvert ! videoscale ! "video/x-raw,width=1280,height=720,framerate=$FPS/1" ! x264enc pass=4 quantizer=$Quant noise-reduction=$NR ! "video/x-h264,profile=constrained-baseline" ! qtmux name=mux ! filesink location=$outputFile demux. ! queue ! progressreport ! audiorate ! audioconvert ! audioresample ! voamrwbenc band-mode=8 ! mux. >> $logFile

		done

	done

done

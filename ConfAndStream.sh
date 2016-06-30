#!/bin/bash

ip=10.10.10.12

DELAY=0ms
JITTER=0ms
BW=10Mbps

serverInputFilePrefix=<InputVideoFileDirectory>/ntia_HeadShoulders-Female15_h264_720p_baseline

clientOutputFilePrefix=<OutputFileDirectory>/ntia_HeadShoulders-Female15_h264_720p_baseline

#aPLR=(0)
aPLR=(0 0.1 0.2 0.5 1 2 5 10)
aNR=( 999 0 )
aQuant=( 23 27 31 35 )
aFPS=( 25 20 15 10 )

for PLR in "${aPLR[@]}"
do
	for FPS in "${aFPS[@]}"
	do
		for Quant in "${aQuant[@]}"
		do	
			for NR in "${aNR[@]}"
			do
				serverFile=$serverInputFilePrefix
				serverFile+=_fps$FPS
				serverFile+=_q$Quant
				serverFile+=_nr$NR

				serverStatsFile=$serverFile
				serverStatsFile+=_amrwb_m08.csv

				serverVCapsFile=$serverFile
				serverVCapsFile+=_amrwb_m08.vcaps

				serverACapsFile=$serverFile
				serverACapsFile+=_amrwb_m08.acaps

				serverFile+=_amrwb_m08.3gp

				clientFile=$clientOutputFilePrefix
				clientFile+=_fps$FPS
				clientFile+=_q$Quant
				clientFile+=_nr$NR

				clientVCapsFile=$clientFile
				clientVCapsFile+=_amrwb_m08.vcaps

				clientACapsFile=$clientFile
				clientACapsFile+=_amrwb_m08.acaps

				clientFile+=_plr$PLR

				clientStatsFile=$clientFile
				clientStatsFile+=_amrwb_m08.csv

				clientFile+=_amrwb_m08.3gp

				rm -f $clientFile
				rm -f $clientStatsFile

				pkill -9 -e -f python
				ssh $ip pkill -9 -e -f python

				server="<GStreamerCodeDirectory>/RTPServer.py $serverFile $serverStatsFile $serverVCapsFile $serverACapsFile"
				client="<GStreamerCodeDirectory>/RTPClient.py $clientFile $clientStatsFile $clientVCapsFile $clientACapsFile"

				ssh $ip sudo /sbin/tc qdisc del dev eth1 root
				ssh $ip sudo /sbin/tc qdisc add dev eth1 root handle 1:1 netem delay $DELAY $JITTER
				ssh $ip sudo /sbin/tc qdisc add dev eth1 parent 1:1 handle 10:1 netem loss $PLR
				ssh $ip sudo /sbin/tc qdisc add dev eth1 parent 10:1 handle 20:1 htb default 1
				ssh $ip sudo /sbin/tc qdisc show

				python $client >> <OutputLogDirectory>/output.log &
				ssh $ip python $server  >> <OutputLogDirectory>/output.log &
				

				sleep 50
			done
		done

	done

done


# GStreamer Multimedia Quality Testbed

This test bed is used to create the INRS Audiovisual Quality dataset. The dataset is accessible at https://github.com/edipdemirbilek/TheINRSAudiovisualQualityDataset and the details are given in publication [1]

FileList:

GenVideoFiles.sh: This script is used to generate reference input video files based on Video Frame Rate, Quantization Parameter and Noise Reduction Values selected.

ConfAndStream.sh: This scripts stream the InputVideoFiles from Server to Client under various Packet Loss Rates. Packet Loss Rate is applied through TC QDISC. Give attantion to naming, audio and video caps files.

GStreamerCodes Folder: GStremaer RTP Server and RTP Client Codes. In addition to the streaming, they also collect the detailed RTCP statistics and save them to file system. 

[1] Demirbilek, Edip, and Jean-Charles Grégoire. “The INRS Audiovisual Quality Dataset." 2016 ACM Multimedia Conference (accepted).

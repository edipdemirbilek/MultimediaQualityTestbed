
s_print_stats=True
s_ssrc=True
s_internal=True
s_validated=True 
s_received_bye=True
s_is_csrc=True
s_is_sender=True
s_seqnum_base=True
s_clock_rate=True
s_rtcp_from=True
s_octets_sent=True
s_packets_sent=True
s_octets_received=True
s_packets_received=True
s_bitrate=True
s_packets_lost=True
s_jitter=True
s_sent_pli_count=True
s_recv_pli_count=True
s_sent_fir_count=True
s_recv_fir_count=True
s_have_sr=True
s_sr_ntptime=True
s_sr_rtptime=True
s_sr_octet_count=True
s_sr_packet_count=True
s_sent_rb=True
s_sent_rb_fractionlost=True
s_sent_rb_packetslost=True
s_sent_rb_exthighestseq=True
s_sent_rb_jitter=True
s_sent_rb_lsr=True
s_sent_rb_dlsr=True
s_have_rb=True
s_rb_fractionlost=True
s_rb_packetslost=True
s_rb_exthighestseq=True
s_rb_jitter=True
s_rb_lsr=True
s_rb_dlsr=True
s_rb_round_trip=True

r_print_stats=False
r_ssrc=True
r_internal=True
r_validated=True 
r_received_bye=True
r_is_csrc=True
r_is_sender=True
r_seqnum_base=True
r_clock_rate=True
r_rtcp_from=True
r_octets_sent=True
r_packets_sent=True
r_octets_received=True
r_packets_received=True
r_bitrate=True
r_packets_lost=True
r_jitter=True
r_sent_pli_count=True
r_recv_pli_count=True
r_sent_fir_count=True
r_recv_fir_count=True
r_have_sr=True
r_sr_ntptime=True
r_sr_rtptime=True
r_sr_octet_count=True
r_sr_packet_count=True
r_sent_rb=True
r_sent_rb_fractionlost=True
r_sent_rb_packetslost=True
r_sent_rb_exthighestseq=True
r_sent_rb_jitter=True
r_sent_rb_lsr=True
r_sent_rb_dlsr=True
r_have_rb=True
r_rb_fractionlost=True
r_rb_packetslost=True
r_rb_exthighestseq=True
r_rb_jitter=True
r_rb_lsr=True
r_rb_dlsr=True
r_rb_round_trip=True

def print_rtpsource_stats(rtpsource, sessionid, displayStats, saveStats, statsFileName):
    
    statsstr=""
    if rtpsource is None:
        statsstr="No-good RTP Source."
        return
    else:
        #print "Dir: "+str(dir(rtpsource_0))
        #print "RTP Source 0  Stats: " + str(rtpsource_0.get_property("stats").to_string())
        stats = rtpsource.get_property("stats")
        if stats.get_value("is-sender")==True and s_print_stats==True:
            statsstr+="Sessionid: "+str(sessionid)
            if s_ssrc==True:
                statsstr+=", ssrc: " + str(stats.get_value("ssrc"))
            if s_internal==True:
                statsstr+=", internal: " + str(stats.get_value("internal"))
            if s_validated==True:
                statsstr+=", validated: " + str(stats.get_value("validated"))
            if s_received_bye==True:
                statsstr+=", received-bye: " + str(stats.get_value("received-bye"))
            if s_is_csrc==True:
                statsstr+=", is-csrc: " + str(stats.get_value("is-csrc"))
            if s_is_sender==True:
                statsstr+=", is-sender: " + str(stats.get_value("is-sender"))
            if s_seqnum_base==True:
                statsstr+=", seqnum-base: " + str(stats.get_value("seqnum-base"))
            if s_clock_rate==True:
                statsstr+=", clock-rate: " + str(stats.get_value("clock-rate"))
            if s_rtcp_from==True:
                statsstr+=", rtcp-from: " + str(stats.get_value("rtcp-from"))
            if s_octets_sent==True:
                statsstr+=", octets-sent: " + str(stats.get_value("octets-sent"))
            if s_packets_sent==True:
                statsstr+=", packets-sent: " + str(stats.get_value("packets-sent"))
            if s_octets_received==True:
                statsstr+=", octets-received: " + str(stats.get_value("octets-received"))
            if s_packets_received==True:
                statsstr+=", packets-received: " + str(stats.get_value("packets-received"))
            if s_bitrate==True:
                statsstr+=", bitrate: " + str(stats.get_value("bitrate"))
            if s_packets_lost==True:
                statsstr+=", packets-lost: " + str(stats.get_value("packets-lost"))
            if s_jitter==True:
                statsstr+=", jitter: " + str(float(stats.get_value("jitter"))/float(stats.get_value("clock-rate"))*1000.0)
            if s_sent_pli_count==True:
                statsstr+=", sent-pli-count: " + str(stats.get_value("sent-pli-count"))
            if s_recv_pli_count==True:
                statsstr+=", recv-pli-count: " + str(stats.get_value("recv-pli-count"))
            if s_sent_fir_count==True:
                statsstr+=", sent-fir-count: " + str(stats.get_value("sent-fir-count"))
            if s_recv_fir_count==True:
                statsstr+=", recv-fir-count: " + str(stats.get_value("recv-fir-count"))
            if s_have_sr==True:
                statsstr+=", have-sr: " + str(stats.get_value("have-sr"))
            if s_sr_ntptime==True:
                statsstr+=", sr-ntptime: " + str(stats.get_value("sr-ntptime"))
            if s_sr_rtptime==True:
                statsstr+=", sr-rtptime: " + str(stats.get_value("sr-rtptime"))
            if s_sr_octet_count==True:
                statsstr+=", sr-octet-count: " + str(stats.get_value("sr-octet-count"))
            if s_sr_packet_count==True:
                statsstr+=", sr-packet-count: " + str(stats.get_value("sr-packet-count"))
            if s_sent_rb==True:
                statsstr+=", sent-rb: " + str(stats.get_value("sent-rb"))
            if s_sent_rb_fractionlost==True:
                statsstr+=", sent-rb-fractionlost: " + str(stats.get_value("sent-rb-fractionlost"))
            if s_sent_rb_packetslost==True:
                statsstr+=", sent-rb-packetslost: " + str(stats.get_value("sent-rb-packetslost"))
            if s_sent_rb_exthighestseq==True:
                statsstr+=", sent-rb-exthighestseq: " + str(stats.get_value("sent-rb-exthighestseq"))
            if s_sent_rb_jitter==True:
                statsstr+=", sent-rb-jitter: " + str(stats.get_value("sent-rb-jitter"))
            if s_sent_rb_lsr==True:
                statsstr+=", sent-rb-lsr: " + str(stats.get_value("sent-rb-lsr"))
            if s_sent_rb_dlsr==True:
                statsstr+=", sent-rb-dlsr: " + str(stats.get_value("sent-rb-dlsr"))
            if s_have_rb==True:
                statsstr+=", have-rb: " + str(stats.get_value("have-rb"))
            if s_rb_fractionlost==True:
                statsstr+=", rb-fractionlost: " + str(stats.get_value("rb-fractionlost"))
            if s_rb_packetslost==True:
                statsstr+=", rb-packetslost: " + str(stats.get_value("rb-packetslost"))
            if s_rb_exthighestseq==True:
                statsstr+=", rb-exthighestseq: " + str(stats.get_value("rb-exthighestseq"))
            if s_rb_jitter==True:
                statsstr+=", rb-jitter: " + str(stats.get_value("rb-jitter"))
            if s_rb_lsr==True:
                statsstr+=", rb-lsr: " + str(stats.get_value("rb-lsr"))
            if s_rb_dlsr==True:
                statsstr+=", rb-dlsr: " + str(stats.get_value("rb-dlsr"))
            if s_rb_round_trip==True:
                statsstr+=", rb-round-trip: " + str(stats.get_value("rb-round-trip"))
                
#        elif stats.get_value("is-sender")==False and r_print_stats==True:
#            statsstr+="Receiver. Sessionid: "+str(sessionid)
#            if r_ssrc==True:
#                statsstr+=", ssrc: " + str(stats.get_value("ssrc"))
#            if r_internal==True:
#                statsstr+=", internal: " + str(stats.get_value("internal"))
#            if r_validated==True:
#                statsstr+=", validated: " + str(stats.get_value("validated"))
#            if r_received_bye==True:
#                statsstr+=", received-bye: " + str(stats.get_value("received-bye"))
#            if r_is_csrc==True:
#                statsstr+=", is-csrc: " + str(stats.get_value("is-csrc"))
#            if r_is_sender==True:
#                statsstr+=", is-sender: " + str(stats.get_value("is-sender"))
#            if r_seqnum_base==True:
#                statsstr+=", seqnum-base: " + str(stats.get_value("seqnum-base"))
#            if r_clock_rate==True:
#                statsstr+=", clock-rate: " + str(stats.get_value("clock-rate"))
#            if r_rtcp_from==True:
#                statsstr+=", rtcp-from: " + str(stats.get_value("rtcp-from"))
#            if r_octets_sent==True:
#                statsstr+=", octets-sent: " + str(stats.get_value("octets-sent"))
#            if r_packets_sent==True:
#                statsstr+=", packets-sent: " + str(stats.get_value("packets-sent"))
#            if r_octets_received==True:
#                statsstr+=", octets-received: " + str(stats.get_value("octets-received"))
#            if r_packets_received==True:
#                statsstr+=", packets-received: " + str(stats.get_value("packets-received"))
#            if r_bitrate==True:
#                statsstr+=", bitrate: " + str(stats.get_value("bitrate"))
#            if r_packets_lost==True:
#               statsstr+=", packets-lost: " + str(stats.get_value("packets-lost"))
#            if r_jitter==True:
#                statsstr+=", jitter: " + str(stats.get_value("jitter"))
#            if r_sent_pli_count==True:
#                statsstr+=", sent-pli-count: " + str(stats.get_value("sent-pli-count"))
#            if r_recv_pli_count==True:
#                statsstr+=", recv-pli-count: " + str(stats.get_value("recv-pli-count"))
#            if r_sent_fir_count==True:
#                statsstr+=", sent-fir-count: " + str(stats.get_value("sent-fir-count"))
#            if r_recv_fir_count==True:
#                statsstr+=", recv-fir-count: " + str(stats.get_value("recv-fir-count"))
#            if r_have_sr==True:
#                statsstr+=", have-sr: " + str(stats.get_value("have-sr"))
#            if r_sr_ntptime==True:
#                statsstr+=", sr-ntptime: " + str(stats.get_value("sr-ntptime"))
#            if r_sr_rtptime==True:
#                statsstr+=", sr-rtptime: " + str(stats.get_value("sr-rtptime"))
#            if r_sr_octet_count==True:
#                statsstr+=", sr-octet-count: " + str(stats.get_value("sr-octet-count"))
#            if r_sr_packet_count==True:
#                statsstr+=", sr-packet-count: " + str(stats.get_value("sr-packet-count"))
#            if r_sent_rb==True:
#                statsstr+=", sent-rb: " + str(stats.get_value("sent-rb"))
#            if r_sent_rb_fractionlost==True:
#                statsstr+=", sent-rb-fractionlost: " + str(stats.get_value("sent-rb-fractionlost"))
#            if r_sent_rb_packetslost==True:
#                statsstr+=", sent-rb-packetslost: " + str(stats.get_value("sent-rb-packetslost"))
#            if r_sent_rb_exthighestseq==True:
#                statsstr+=", sent-rb-exthighestseq: " + str(stats.get_value("sent-rb-exthighestseq"))
#            if r_sent_rb_jitter==True:
#                statsstr+=", sent-rb-jitter: " + str(stats.get_value("sent-rb-jitter"))
#            if r_sent_rb_lsr==True:
#                statsstr+=", sent-rb-lsr: " + str(stats.get_value("sent-rb-lsr"))
#            if r_sent_rb_dlsr==True:
#                statsstr+=", sent-rb-dlsr: " + str(stats.get_value("sent-rb-dlsr"))
#            if r_have_rb==True:
#                statsstr+=", have-rb: " + str(stats.get_value("have-rb"))
#            if r_rb_fractionlost==True:
#                statsstr+=", rb-fractionlost: " + str(stats.get_value("rb-fractionlost"))
#            if r_rb_packetslost==True:
#               statsstr+=", rb-packetslost: " + str(stats.get_value("rb-packetslost"))
#            if r_rb_exthighestseq==True:
#                statsstr+=", rb-exthighestseq: " + str(stats.get_value("rb-exthighestseq"))
#            if r_rb_jitter==True:
#                statsstr+=", rb-jitter: " + str(stats.get_value("rb-jitter"))
#            if r_rb_lsr==True:
#                statsstr+=", rb-lsr: " + str(stats.get_value("rb-lsr"))
#            if r_rb_dlsr==True:
#                statsstr+=", rb-dlsr: " + str(stats.get_value("rb-dlsr"))
#            if r_rb_round_trip==True:
#                statsstr+=", rb-round-trip: " + str(stats.get_value("rb-round-trip"))

        else: statsstr=""
            
    if len(statsstr) > 1:
	if displayStats==True:
             print statsstr
        if saveStats==True:
             with open(statsFileName, "a") as csvfile:
    		csvfile.write(statsstr+'\n')
            
def print_udpsink_stats(stats_str, data): 
    
    print str(stats_str) +",  bytes-sent: " +str(data.get_value("bytes-sent")) \
    +", packets-sent: " +str(data.get_value("packets-sent")) \
    +", connect-time: " +str(data.get_value("connect-time")) \
    +", disconnect-time: " +str(data.get_value("disconnect-time"))

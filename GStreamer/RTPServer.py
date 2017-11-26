#!/usr/bin/env python
########### VIDEO_STREAMER 

# https://wiki.ubuntu.com/Novacut/GStreamer1.0

import gi
from gi.repository import GObject as gobject
from gi.repository import Gst as gst
gi.require_version('Gst', '1.0')
gobject.threads_init()
gst.init(None)

import sys
import os
import readline
import time
import RTPStats

REMOTE_HOST = '10.10.10.11'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline.new('server')
bus = pipeline.get_bus()

filesource = gst.ElementFactory.make("filesrc", "file-source")

filesource.set_property('location', sys.argv[1])
statsFile=sys.argv[2]

WRITE_VIDEO_CAPS = sys.argv[3]
WRITE_AUDIO_CAPS = sys.argv[4]

dvdemux = gst.ElementFactory.make("qtdemux", "dvdemux")

q1 = gst.ElementFactory.make("queue", "q1")
q2 = gst.ElementFactory.make("queue", "q2")
progressreport = gst.ElementFactory.make("progressreport", "progressreport")
rtph264pay = gst.ElementFactory.make("rtph264pay", "rtph264pay")
rtpamrpay = gst.ElementFactory.make("rtpamrpay", "rtpamrpay")

rtpbin = gst.ElementFactory.make('rtpbin', 'rtpbin')

#For Video
vudpsink_rtpout = gst.ElementFactory.make("udpsink", "vudpsink_rtpout")
vudpsink_rtpout.set_property('host', REMOTE_HOST)
vudpsink_rtpout.set_property('port', 5000)

vudpsink_rtcpout = gst.ElementFactory.make("udpsink", "vudpsink_rtcpout")
vudpsink_rtcpout.set_property('host', REMOTE_HOST)
vudpsink_rtcpout.set_property('port', 5001)
vudpsink_rtcpout.set_property('sync', False)
vudpsink_rtcpout.set_property('async', False)

vudpsrc_rtcpin = gst.ElementFactory.make("udpsrc", "vudpsrc_rtcpin")
vudpsrc_rtcpin.set_property('port', 5005)

#For Audio
audpsink_rtpout = gst.ElementFactory.make("udpsink", "audpsink_rtpout")
audpsink_rtpout.set_property('host', REMOTE_HOST)
audpsink_rtpout.set_property('port', 5002)

audpsink_rtcpout = gst.ElementFactory.make("udpsink", "audpsink_rtcpout")
audpsink_rtcpout.set_property('host', REMOTE_HOST)
audpsink_rtcpout.set_property('port', 5003)
audpsink_rtcpout.set_property('sync', False)
audpsink_rtcpout.set_property('async', False)

audpsrc_rtcpin = gst.ElementFactory.make("udpsrc", "audpsrc_rtcpin")
audpsrc_rtcpin.set_property('port', 5007)

# Add elements
pipeline.add(filesource)
pipeline.add(dvdemux)
pipeline.add(q1)
pipeline.add(q2)
pipeline.add(rtph264pay)
pipeline.add(progressreport)
pipeline.add(rtpamrpay)
pipeline.add(rtpbin)
pipeline.add(vudpsink_rtpout)
pipeline.add(vudpsink_rtcpout)
pipeline.add(vudpsrc_rtcpin)
pipeline.add(audpsink_rtpout)
pipeline.add(audpsink_rtcpout)
pipeline.add(audpsrc_rtcpin)

def dvdemux_padded(demuxer, pad):
    #print "Demux_Callback entry: "+str(pad.get_name())
    if pad.get_name() == "video_0":
        #print "Video Template"
        qv_pad = q1.get_static_pad("sink")
        pad.link(qv_pad)
    elif pad.get_name() == "audio_0":
        #print "Audio Template"
        qa_pad = q2.get_static_pad("sink")
        pad.link(qa_pad)
    else:
        print "SERVER: Template: "+str(pad.get_property("template").name_template)

# Create links
dvdemux.connect('pad-added', dvdemux_padded)

# Connected
def on_new_ssrc(rtpbin, sessionid, ssrc):
    print "SERVER: Got new remote session: "+str(sessionid) + " SSRC: " + str(ssrc)
    if sessionid == 0:
        on_new_ssrc.ssrc_0 = ssrc
    elif sessionid == 1:
        on_new_ssrc.ssrc_1 = ssrc
        
# New RTCP message
def on_ssrc_active(rtpbin, sessionid, ssrc):
    #print "SERVER: Got RTCP from session: "+str(sessionid) + " SSRC: " +str(ssrc)
    
    rtpsession= rtpbin.emit("get-internal-session", sessionid) # get the right session
    sources = rtpsession.get_property("sources")
    for source in sources:
        RTPStats.print_rtpsource_stats(source, sessionid, False, False, statsFile)

def on_bye_ssrc(rtpbin, sessionid, ssrc):
    print "SERVER: Bye RTCP from session: "+str(sessionid) + " SSRC: " +str(ssrc)
    
    rtpsession= rtpbin.emit("get-internal-session", sessionid) # get the right session
    sources = rtpsession.get_property("sources")
    for source in sources:
        RTPStats.print_rtpsource_stats(source, sessionid, False, False, statsFile)
        
on_new_ssrc.ssrc_0 = 0    
on_new_ssrc.ssrc_1 = 1 
rtpbin.connect('on-new-ssrc', on_new_ssrc)
rtpbin.connect('on-ssrc-active', on_ssrc_active)
rtpbin.connect('on-bye-ssrc', on_bye_ssrc)

filesource.link(dvdemux)
q1.link(rtph264pay)

q2.link(progressreport)
progressreport.link(rtpamrpay)

#q2.link(rtpamrpay)

rtph264pay.link_pads('src', rtpbin, 'send_rtp_sink_0')
rtpbin.link_pads('send_rtp_src_0', vudpsink_rtpout, 'sink')
rtpbin.link_pads('send_rtcp_src_0', vudpsink_rtcpout, 'sink')
vudpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0')

rtpamrpay.link_pads('src', rtpbin, 'send_rtp_sink_1')
rtpbin.link_pads('send_rtp_src_1', audpsink_rtpout, 'sink')
rtpbin.link_pads('send_rtcp_src_1', audpsink_rtcpout, 'sink')
audpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_1')
    
def print_udpsink_stats(): 
    
    udpsink = pipeline.get_by_name("vudpsink_rtpout")
    data = udpsink.emit("get-stats", REMOTE_HOST, 5000)
    RTPStats.print_udpsink_stats("Video Stats", data)
    
    udpsink = pipeline.get_by_name("audpsink_rtpout")
    data = udpsink.emit("get-stats", REMOTE_HOST, 5002) 
    RTPStats.print_udpsink_stats("Audio Stats", data)

    return True 

def eos():
                        
    print "SERVER: Sending EOS to pipeline."
    pipeline.send_event(gst.Event.new_eos())
    
    #We have to wait some time, but not sure if this long. 
    #Since it does nto bother us to wait a few sec extra, we keep this value.
    time.sleep(1)
    
    print "SERVER: Changing pipeline state to NULL."
    pipeline.set_state(gst.State.NULL)
    
    #We have to wait some time, but not sure if this long. 
    #Since it does nto bother us to wait a few sec extra, we keep this value.
    time.sleep(1)
    
    print "SERVER: Quitting the Mainloop."
    mainloop.quit()
    
def on_message(bus, message):
    #print "On_Message entry."
    t = message.type
    if t == gst.MessageType.EOS:
        print "SERVER: EOS Message."
        eos()
    elif t == gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print "SERVER: Error: %s" % err, debug
        pipeline.set_state(gst.State.NULL)
    #else:
    #    print "SERVER: Else Message: "+str(t)
            
def on_sync_message(bus, message):
    if message.get_structure() is None:
        print "SERVER: On_Sync_Message. Structure is none."
        return

    print "SERVER: Message Structure Name: " +str(message.get_structure().get_name())
    
def on_finish(bus, message):
    print "SERVER: Message:EOS."
    #eos()
    
def on_eos(bus, msg):
    print "SERVER: On_Eos."
    print_udpsink_stats()
    eos()
    
def on_error(bus, msg):
   print('SERVER: on_error():', msg.parse_error())

def on_warning(bus, msg):
   print "SERVER: Warning."
            
print "SERVER: Creating the bus."
#bus.add_signal_watch()
#bus.enable_sync_message_emission()
#bus.connect("message", on_message)
bus.connect('message::eos', on_eos)
bus.connect('message::error', on_error)
bus.connect('message::warning', on_warning)
bus.connect("sync-message::element", on_sync_message)
bus.add_signal_watch()

def run():
    vcaps = None
    acaps = None
    while vcaps is None or acaps is None:
        vcaps = vudpsink_rtpout.get_static_pad('sink').get_property('caps')
        acaps = audpsink_rtpout.get_static_pad('sink').get_property('caps')

        if vcaps is None:
            print "SERVER: Waiting for video interface/caps"
            
        if acaps is None:
            print "SERVER: Waiting for audio interface/caps"

        time.sleep(0.1)
        
    print vcaps.to_string()
    print acaps.to_string()
    print ("SERVER: Final caps written to", WRITE_VIDEO_CAPS)
    open(WRITE_VIDEO_CAPS, 'w').write(vcaps.to_string())
    
    print ("SERVER: Final caps written to", WRITE_AUDIO_CAPS)
    open(WRITE_AUDIO_CAPS, 'w').write(acaps.to_string())
    


def go():
    print "SERVER: Setting pipeline to PLAYING."
    pipeline.set_state(gst.State.PLAYING)
    print "SERVER: Waiting pipeline to settle."
    pipeline.get_state(1000)
    #run()
    try:
        print "SERVER: Running the Mainloop."
        mainloop.run()
        #print pipeline.set_state(gst.State.NULL)
    except KeyboardInterrupt:
        eos()
    
go()

#!/usr/bin/env python
# -=- encoding: utf-8 -=-
################ VIDEO RECEIVER

import gi
from gi.repository import GObject as gobject
from gi.repository import Gst as gst
gi.require_version('Gst', '1.0')
gobject.threads_init()
gst.init(None)

import time
import RTPStats
import sys

REMOTE_HOST = '10.10.10.12'

mainloop = gobject.MainLoop()
pipeline = gst.Pipeline.new('client')
bus = pipeline.get_bus()

rtpbin = gst.ElementFactory.make('rtpbin', 'rtpbin')
rtpbin.set_property('buffer-mode', 1)

# For Video
vudpsrc_rtpin = gst.ElementFactory.make('udpsrc', 'vudpsrc_rtpin')
vudpsrc_rtpin.set_property('port', 5000)

vCapsFile=sys.argv[3]
aCapsFile=sys.argv[4]
vcaps = open(vCapsFile, 'r').read()
acaps = open(aCapsFile, 'r').read()

vudpsrc_caps = gst.caps_from_string(vcaps)
#vudpsrc_caps = gst.caps_from_string("application/x-rtp,media=(string)video,clock-rate=(int)90000,encoding-name=(string)H264")
vudpsrc_rtpin.set_property('caps', vudpsrc_caps)

vudpsrc_rtcpin = gst.ElementFactory.make('udpsrc', 'vudpsrc_rtcpin')
vudpsrc_rtcpin.set_property('port', 5001)

vudpsink_rtcpout = gst.ElementFactory.make('udpsink', 'vudpsink_rtcpout')
vudpsink_rtcpout.set_property('host', REMOTE_HOST)
vudpsink_rtcpout.set_property('port', 5005)
vudpsink_rtcpout.set_property('sync', False)
vudpsink_rtcpout.set_property('async', False)

#For Audio
audpsrc_rtpin = gst.ElementFactory.make('udpsrc', 'audpsrc_rtpin')
audpsrc_rtpin.set_property('port', 5002)

audpsrc_caps = gst.caps_from_string(acaps)
#audpsrc_caps = gst.caps_from_string("application/x-rtp,media=(string)audio,clock-rate=(int)16000,encoding-name=(string)AMR-WB,encoding-params=(string)1,octet-align=(string)1")
audpsrc_rtpin.set_property('caps', audpsrc_caps)

audpsrc_rtcpin = gst.ElementFactory.make('udpsrc', 'audpsrc_rtcpin')
audpsrc_rtcpin.set_property('port', 5003)

audpsink_rtcpout = gst.ElementFactory.make('udpsink', 'audpsink_rtcpout')
audpsink_rtcpout.set_property('host', REMOTE_HOST)
audpsink_rtcpout.set_property('port', 5007)
audpsink_rtcpout.set_property('sync', False)
audpsink_rtcpout.set_property('async', False)

rtph264depay = gst.ElementFactory.make("rtph264depay", "rtph264depay")
rtpamrdepay = gst.ElementFactory.make("rtpamrdepay", "rtpamrdepay")

queuev1 = gst.ElementFactory.make("queue", "queuev1")
h264parse = gst.ElementFactory.make("h264parse", "h264parse")
queuev2 = gst.ElementFactory.make("queue", "queuev2")

queuea = gst.ElementFactory.make("queue", "queuea")

qtmux = gst.ElementFactory.make("qtmux", "qtmux")
filesink = gst.ElementFactory.make("filesink", "filesink")

filesink.set_property('location', sys.argv[1])
statsFile=sys.argv[2]

#Display
#autovideosink=gst.ElementFactory.make("autovideosink", "autovideosink")
#autoaudiosink=gst.ElementFactory.make("autoaudiosink", "autoaudiosink")

pipeline.add(rtpbin)
pipeline.add(vudpsrc_rtpin)
pipeline.add(vudpsrc_rtcpin)
pipeline.add(vudpsink_rtcpout)
pipeline.add(audpsrc_rtpin)
pipeline.add(audpsrc_rtcpin)
pipeline.add(audpsink_rtcpout)
pipeline.add(rtph264depay)
pipeline.add(rtpamrdepay)

pipeline.add(queuev1)
pipeline.add(h264parse)
pipeline.add(queuev2)
pipeline.add(queuea)

#File
pipeline.add(qtmux)
pipeline.add(filesink)

#Display
#pipeline.add(autovideosink)
#pipeline.add(autoaudiosink)

def pad_added_cb(rtpbin, pad, depay):
    if pad.get_name().startswith("recv_rtp_src_0") and depay.get_name().startswith("rtph264depay"):
        print "CLIENT: Linking video depay"
        depay_pad = rtph264depay.get_static_pad("sink")
        pad.link(depay_pad)
    elif pad.get_name().startswith("recv_rtp_src_1") and depay.get_name().startswith("rtpamrdepay"):
        print "CLIENT: Linking audio depay"
        depay_pad = rtpamrdepay.get_static_pad("sink")
        pad.link(depay_pad)
    #else:
    #    print "CLIENT: Can not do anything."


    
print "CLIENT: Linking static pads."
vudpsrc_rtpin.link_pads('src', rtpbin, 'recv_rtp_sink_0') 
vudpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_0') 
rtpbin.link_pads('send_rtcp_src_0', vudpsink_rtcpout, 'sink') 

audpsrc_rtpin.link_pads('src', rtpbin, 'recv_rtp_sink_1') 
audpsrc_rtcpin.link_pads('src', rtpbin, 'recv_rtcp_sink_1') 
rtpbin.link_pads('send_rtcp_src_1', audpsink_rtcpout, 'sink')

rtpbin.connect('pad-added', pad_added_cb, rtph264depay)
rtpbin.connect('pad-added', pad_added_cb, rtpamrdepay)

def on_bye_ssrc(rtpbin, sessionid, ssrc):
    #print "Got Bye from session: "+str(sessionid) + " SSRC: " +str(ssrc)
    
    rtpsession= rtpbin.emit("get-internal-session", sessionid) # get the right session
    sources = rtpsession.get_property("sources")
    for source in sources:
        RTPStats.print_rtpsource_stats(source, sessionid, True, True, statsFile)
    
    if on_bye_ssrc.bye_received_once==False:
        #print "First Bye SSRC received. Now goign to wait for the second Bye SSRC message."
        on_bye_ssrc.bye_received_once=True
        
    else:
        #print "Second Bye SSRC message received. We can initiate end operations."
        #do not call eos directly. This will work with severe warning.
        #At this stage, it is not in main thread context.
        #Below we add a signal so that eos will be called in main thread context.
        #eos() 
        gobject.idle_add (eos)
    
rtpbin.connect('on-bye-ssrc', on_bye_ssrc)
on_bye_ssrc.bye_received_once=False

def on_new_ssrc(rtpbin, sessionid, ssrc):
    print "CLIENT: Got New session: "+str(sessionid) + " SSRC: " +str(ssrc)
    
    rtpsession= rtpbin.emit("get-internal-session", sessionid) # get the right session
    sources = rtpsession.get_property("sources")
    for source in sources:
        RTPStats.print_rtpsource_stats(source, sessionid, False, False, statsFile)
    
    if sessionid == 0:
        on_new_ssrc.ssrc_0 = sessionid
    elif sessionid == 1:
        on_new_ssrc.ssrc_1 = sessionid
        
# New RTCP i belive
#http://lists.freedesktop.org/archives/gstreamer-devel/2014-May/047789.html
def on_ssrc_active(rtpbin, sessionid, ssrc):
    #print "Got RTCP session: "+str(sessionid) + " SSRC: " +str(ssrc)
    
    rtpsession= rtpbin.emit("get-internal-session", sessionid) # get the right session
    sources = rtpsession.get_property("sources")
    for source in sources:
        RTPStats.print_rtpsource_stats(source, sessionid, False, False, statsFile)

on_new_ssrc.ssrc_0 = 0    
on_new_ssrc.ssrc_1 = 1 
rtpbin.connect('on-new-ssrc', on_new_ssrc)
rtpbin.connect('on-ssrc-active', on_ssrc_active)

rtph264depay.link(queuev1)
queuev1.link(h264parse)
h264parse.link(queuev2)

rtpamrdepay.link(queuea)

#File
queuev2.link_pads('src', qtmux, 'video_0')
queuea.link_pads('src', qtmux, 'audio_0')
qtmux.link(filesink)

#Display
#queuev2.link(autovideosink)
#queuea.link(autoaudiosink)

def on_message(bus, message):
#    print "On_Message entry."
    t = message.type
    if t == gst.MessageType.EOS:
        print "CLIENT: EOS Message received."
        eos()
    elif t == gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print "CLIENT: Error: %s" % err, debug
        pipeline.set_state(gst.State.NULL)
    #else:
    #    print "Else Message: "+str(t)
            
def on_sync_message(bus, message):
    if message.get_structure() is None:
        print "CLIENT: On_Sync_Message. Structure is none"
        return

    print "CLIENT: Message Structure Name: " +str(message.get_structure().get_name())
                
     
def on_eos(bus, msg):
    print "CLIENT: On_Eos."
    eos()
    
def on_error(bus, msg):
   print('CLIENT: on_error():', msg.parse_error())

def on_warning(bus, msg):
   print "CLIENT: Warning."

def on_state(bus, msg):
   print "CLIENT: State Changed."
    
print "CLIENT: Creating the bus."

#bus.enable_sync_message_emission()
#bus.connect("message", on_message)
bus.connect('message::eos', on_eos)
bus.connect('message::error', on_error)
bus.connect('message::warning', on_warning)
#bus.connect('message::state-changed', on_state)
bus.connect("sync-message::element", on_sync_message)
#bus.add_signal_watch()

def start():
    pipeline.set_state(gst.State.PLAYING)
    vudpsink_rtcpout.set_locked_state(gst.State.PLAYING)
    audpsink_rtcpout.set_locked_state(gst.State.PLAYING)
    print "CLIENT: Started..."

def eos():
    
    print "CLIENT: Sending EOS to pipeline."
    pipeline.send_event(gst.Event.new_eos())
    
    #We have to wait some time, but not sure if this long. 
    #Since it does nto bother us to wait a few sec extra, we keep this value.
    time.sleep(1)
    
    print "CLIENT: Changing pipeline state to NULL."
    pipeline.set_state(gst.State.NULL)
    
    #We have to wait some time, but not sure if this long. 
    #Since it does nto bother us to wait a few sec extra, we keep this value.
    time.sleep(1)

    print "CLIENT: Quitting the Mainloop."
    mainloop.quit()
    
    
def loop():   
    try:
        print "CLIENT: Running the Mainloop."
        mainloop.run()
    except KeyboardInterrupt:
        eos()

if __name__ == '__main__':
    start()
    loop()

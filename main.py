#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import RPi.GPIO as GPIO
import socket
import fcntl
import struct
import VOICEAPI.BaiduVoiceTranslationAPI as voiceapi


led_pin = 26
light_state = False
should_close = False
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)


operation_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
allow_users_list = [u'Joyce',u'self']
def get_temp():
    tfile = open("/sys/bus/w1/devices/28-041690070bff/w1_slave")

    while(True):
        text = tfile.read()
        check =  text.split("\n")[0].split(" ")[-1]
        if check == "YES":
            break
    tfile.close()

    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return temperature




def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

class MyWXBot(WXBot):

    def __init__(self, apiKey, secretKey):
        super(MyWXBot, self).__init__()
        self.VoiceTranslation = voiceapi.BaiduVoiceHttpClient(apiKey,secretKey)
        self.prefix = u"./temp/"
        self.Language = "zh"
        self.Rate = 8000  # 采样率，支持8000和16000
        self.Channel = 1  # 声道，目前baidu只支持单声道
        self.Format = 'wav'  # 语音格式，支持wav pcm opus speex amr x-flac
        self.turn_on = set(u'开灯')
        self.turn_off = set(u'关灯')
        self.DEBUG = False
    def open_light(self):
        GPIO.output(led_pin, False)
        return

    def close_light(self):
        GPIO.output(led_pin, True)
        return

    def handing_voice(self, msg):
        namelist = msg['user']['name'].split(" ")
        name = self.to_unicode(namelist[0], 'utf-8')
        if name in allow_users_list:
            source = self.get_voice(msg['msg_id'])
            self.to_unicode(source, 'utf-8')
            source = self.prefix + source
            dest = "./temp/temp.wav"
            self.VoiceTranslation.mp3_to_wav(source, dest)
            cmd  = "rm "+ source
            os.system(cmd)
            Voice_resp = self.VoiceTranslation.VocieTranslation(
                self.Language, self.Channel, dest, self.Format, self.Rate)
            wordsset = set(Voice_resp)
            if len(wordsset & self.turn_on)== 2:
                print "开灯"
                self.open_light()
                sendmsg = u'灯已打开'
                if name == u'self':
                    self.send_msg_by_uid(sendmsg)
                else:
                    self.send_msg_by_uid(sendmsg, msg['user']['id'])
                return
            if len(wordsset & self.turn_off) == 2:
                print "关灯"
                sendmsg = u'灯已关闭'
                self.close_light()
                if name == u'self':
                    self.send_msg_by_uid(sendmsg)
                else:
                    self.send_msg_by_uid(sendmsg, msg['user']['id'])
                return
            print Voice_resp
            print len(wordsset & self.turn_on)
            print len(wordsset & self.turn_off)
        else:
            print "inligal user"

    def handling_msg(self, msg):
        namelist = msg['user']['name'].split(" ")
        name = self.to_unicode(namelist[0], 'utf-8')
        if name not in allow_users_list:
            print "ilegal user!"
            return
        if msg['content']['data'] == u'开灯':
            self.open_light()
        if msg['content']['data'] == u'关灯':
            self.close_light()
        if msg['content']['data'] == u'关灯':
            self.close_light()
        if msg['content']['data'] == u'获得IP':
            IP =  get_ip_address('wlan0')
            sendmsg = u'IP地址为：'+unicode(IP, 'utf-8')
            if name == u'self':
                self.send_msg_by_uid(sendmsg)
            else:
                self.send_msg_by_uid(sendmsg,msg['user']['id'])
        if msg['content']['data'] == u'室温':
            temp = get_temp()
            string_temp = "%2.3f" % temp
            sendmsg = u'当前室温：' + unicode(string_temp, 'utf-8')
            if name == u'self':
                self.send_msg_by_uid(sendmsg)
            else:
                self.send_msg_by_uid(sendmsg,msg['user']['id'])

        return

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 or msg['msg_type_id'] == 1:
            if msg['content']['type'] == 0:
                self.handling_msg(msg)
                return
            #voice
            if msg['content']['type'] == 4:
                self.handing_voice(msg)
                return
        return


def main():
    bot = MyWXBot("sample",
                  "sample")
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    bot.run()


if __name__ == '__main__':
    main()

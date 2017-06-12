#coding:utf-8
#-------------------------------------------------
# Baidu语音识别API Python版 
# Ver 0.2
# update 无需设定cuid，直接获取，修复中文注释导致无法调用
#-------------------------------------------------
#                  
# Ver 0.1                                  
#-------------------------------------------------
# Create By Damon.shen


import json
import base64
import os
import urllib2
from pydub import AudioSegment

class BaiduVoiceHttpClient():
    apiKey = ""
    secretKey = ""
    

    def __init__(self,apiKey,secretKey):
        self.apiKey = apiKey;
        self.secretKey = secretKey;

    def __getToken(self):
        auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s" % (self.apiKey, self.secretKey);
        response = self.__request(auth_url,'');
        return response['access_token'];

    def VocieTranslation(self,Language,Channel,audioFile,Format,Rate):

        Token = self.__getToken();
        cuid = Token[Token.index("-") + 1:];
        API_url = "http://vop.baidu.com/server_api";
        
        audioFileLen = os.path.getsize(audioFile);
        audio = open(audioFile,'rb');
        base_data = base64.b64encode(audio.read());
        audio.close();
        
        Postdata = {'format':Format,'rate':Rate,'channel':Channel,'lan':Language,'token':Token,'cuid':cuid,'len':audioFileLen,'speech':base_data};

        response = self.__request(API_url,Postdata);
        if (response['err_no'] == 0):
            return response['result'][0]
        else:
            return response['err_msg']
    


    def __request(self,url,data):
        try:
            res =  urllib2.urlopen(url = url,data=json.dumps(data));
            json_data = json.loads(res.read());
            return json_data;
        except Exception, e:
            print e;

    def mp3_to_wav(self, source, dest):
        sound = AudioSegment.from_mp3(source)
        sound.set_channels(1)
        sound.set_sample_width(2)
        sound.export(dest, format="wav")


def local_test():
    VoiceTranslation = BaiduVoiceHttpClient(
        "o4ED25Kh3e0YkyEYCHaEGVTF","90010c9bd49413dec5279c4417927746")
    source = "/home/yb/dev/wxBot/temp/33.mp3"
    dest = "/home/yb/dev/wxBot/temp/temp.wav"
    VoiceTranslation.mp3_to_wav(source, dest)
    Language = "zh"
    Rate = 8000  # 采样率，支持8000和16000
    Channel = 1  # 声道，目前baidu只支持单声道
    Format = 'wav'  # 语音格式，支持wav pcm opus speex amr x-flac
    Voice_resp = VoiceTranslation.VocieTranslation(Language, Channel,
                                                 "/home/yb/dev/wxBot/temp/111.wav", Format,
                                      Rate)
    for each in Voice_resp:
        print each

if __name__ == '__main__':
    local_test()
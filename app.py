import requests ,os #line:1
import threading ,csv ,time #line:2
from glob import glob #line:3
import shutil ,zipfile #line:4
from random import choice #line:5
import random #line:6
from flask import Flask ,render_template ,request ,redirect ,url_for ,jsonify ,send_file #line:7
from apscheduler .schedulers .background import BackgroundScheduler #line:8
from itertools import zip_longest #line:9
stop_sending =False #line:10
background_task_started =True #line:11
def create_allfiles_folder ():#line:13
    OO00O000O00O0O0OO ='allfiles'#line:14
    os .makedirs ("uploaded",exist_ok =True )#line:15
    if not os .path .exists (OO00O000O00O0O0OO ):#line:17
        os .makedirs (OO00O000O00O0O0OO )#line:18
        time .sleep (2 )#line:19
        os .makedirs (OO00O000O00O0O0OO +"//apifile")#line:20
        print (f"'{OO00O000O00O0O0OO}' folder has been created.")#line:21
    else :#line:22
        print (f"'{OO00O000O00O0O0OO}' folder already exists.")#line:23
def generate_custom_uuid ():#line:25
    O000O0OO0OO00OO0O ="INV"#line:27
    O00OO0O000O000O00 =random .randint (100000 ,999999 )#line:30
    OOO00000O00OOO00O =random .randint (1000 ,9999 )#line:31
    O0OOOO0OOOO0O0OOO =f"{O000O0OO0OO00OO0O}-{O00OO0O000O000O00}-{OOO00000O00OOO00O}"#line:33
    return O0OOOO0OOOO0O0OOO #line:35
def new ():#line:36
    try :#line:37
        OOOO0O0O00OO0OOOO =str (os .getcwd ())+'/allfiles'#line:38
        OO0OO0OO0OO0000OO =3000 #line:40
        OOOO0000OOOOOO00O =50 #line:41
        OO0O00O0O0OOOOOO0 =os .path .join (OOOO0O0O00OO0OOOO ,'checkemail.csv')#line:44
        if not os .path .exists (OO0O00O0O0OOOOOO0 ):#line:45
            print (f"Error: {OO0O00O0O0OOOOOO0} does not exist.")#line:46
            return #line:47
        with open (OO0O00O0O0OOOOOO0 ,'r')as OOO0O00O00OO0000O :#line:49
            O00OO000000O0OO00 =[O00OO00OOOOOOOO00 .strip ()for O00OO00OOOOOOOO00 in OOO0O00O00OO0000O .readlines ()if "@"in O00OO00OOOOOOOO00 ]#line:50
        O00OOOO0O000O0000 =0 #line:52
        for O0000O0OOO0O0OOO0 in os .listdir (OOOO0O0O00OO0OOOO ):#line:55
            OO0000OO0OOOO0O0O =os .path .join (OOOO0O0O00OO0OOOO ,O0000O0OOO0O0OOO0 )#line:56
            if os .path .isdir (OO0000OO0OOOO0O0O ):#line:57
                for OO00O0OOO00OO0OOO in os .listdir (OO0000OO0OOOO0O0O ):#line:59
                    OOOOO0000O0O00O0O =os .path .join (OO0000OO0OOOO0O0O ,OO00O0OOO00OO0OOO )#line:60
                    if OO00O0OOO00OO0OOO .startswith ("contact")and OO00O0OOO00OO0OOO .endswith ((".txt",".csv")):#line:62
                        with open (OOOOO0000O0O00O0O ,'r')as OO00000O00OOO0OO0 :#line:64
                            O0O0O0O0O0000000O =csv .reader (OO00000O00OOO0OO0 )#line:65
                            OOOO00000OOO0OOO0 =next (O0O0O0O0O0000000O )#line:66
                            OOO0OO0OOOOOOOO00 =list (O0O0O0O0O0000000O )#line:69
                            O0O0000OO000O0000 =len (OOO0OO0OOOOOOOO00 )//OO0OO0OO0OO0000OO +(1 if len (OOO0OO0OOOOOOOO00 )%OO0OO0OO0OO0000OO >0 else 0 )#line:70
                            for O0O000O00O00OOO00 in range (O0O0000OO000O0000 ):#line:72
                                O00OO0000OOOOOO0O =OOO0OO0OOOOOOOO00 [O0O000O00O00OOO00 *OO0OO0OO0OO0000OO :(O0O000O00O00OOO00 +1 )*OO0OO0OO0OO0000OO ]#line:73
                                OOO00OOOOO00OOO0O =os .path .join (OO0000OO0OOOO0O0O ,f'lead_{O0O000O00O00OOO00 + 1}.csv')#line:74
                                with open (OOO00OOOOO00OOO0O ,'w',newline ='')as OOO000OO0OO0O000O :#line:76
                                    OOOO000OOOOOO0O00 =csv .writer (OOO000OO0OO0O000O )#line:77
                                    OOOO000OOOOOO0O00 .writerow (['name','email'])#line:78
                                    for OO00O0O0OOOOOOOO0 ,O0000O0000000OOO0 in enumerate (O00OO0000OOOOOO0O ):#line:81
                                        O000OO0O0OOO000OO =generate_custom_uuid ()#line:82
                                        O000OO0O0OOO000OO =str (O000OO0O0OOO000OO )#line:83
                                        if OO00O0O0OOOOOOOO0 ==0 and O00OOOO0O000O0000 <len (O00OO000000O0OO00 ):#line:85
                                            OOOO000OOOOOO0O00 .writerow ([O000OO0O0OOO000OO ,O00OO000000O0OO00 [O00OOOO0O000O0000 ]])#line:86
                                            O00OOOO0O000O0000 =(O00OOOO0O000O0000 +1 )%len (O00OO000000O0OO00 )#line:87
                                        OOOO000OOOOOO0O00 .writerow (O0000O0000000OOO0 )#line:88
                                        if (OO00O0O0OOOOOOOO0 +1 )%OOOO0000OOOOOO00O ==0 and O00OOOO0O000O0000 <len (O00OO000000O0OO00 ):#line:91
                                            OOOO000OOOOOO0O00 .writerow ([O000OO0O0OOO000OO ,O00OO000000O0OO00 [O00OOOO0O000O0000 ]])#line:92
                                            O00OOOO0O000O0000 =(O00OOOO0O000O0000 +1 )%len (O00OO000000O0OO00 )#line:93
                        try :#line:95
                            os .remove (OOOOO0000O0O00O0O )#line:96
                        except Exception as OO000000OOO0O0O00 :#line:97
                            print (OO000000OOO0O0O00 )#line:98
                    elif OO00O0OOO00OO0OOO .startswith ("gmail")and OO00O0OOO00OO0OOO .endswith ((".txt",".csv")):#line:100
                        with open (OOOOO0000O0O00O0O ,'r')as OO00000O00OOO0OO0 :#line:102
                            OOO0OO0OOOOOOOO00 =OO00000O00OOO0OO0 .readlines ()#line:103
                            for O0O000O00O00OOO00 ,O0000O0000000OOO0 in enumerate (OOO0OO0OOOOOOOO00 ):#line:104
                                if "@"not in str (O0000O0000000OOO0 ):#line:105
                                    continue #line:106
                                OOO0OO0OOOOO0OOO0 ,OO0OO0OO00OOO00OO =O0000O0000000OOO0 .strip ().split (',')#line:107
                                OOO00OOOOO00OOO0O =os .path .join (OO0000OO0OOOO0O0O ,f'cred{O0O000O00O00OOO00 + 1}.csv')#line:108
                                with open (OOO00OOOOO00OOO0O ,'w',newline ='')as OOO000OO0OO0O000O :#line:109
                                    OOOO000OOOOOO0O00 =csv .writer (OOO000OO0OO0O000O )#line:110
                                    OOOO000OOOOOO0O00 .writerow (['email','password'])#line:111
                                    OOOO000OOOOOO0O00 .writerow ([OOO0OO0OOOOO0OOO0 ,OO0OO0OO00OOO00OO ])#line:112
                        try :#line:113
                            os .remove (OOOOO0000O0O00O0O )#line:114
                        except :#line:115
                            pass #line:116
        try :#line:118
            OOO0O00O00OO0000O .close ()#line:119
            os .remove (OO0O00O0O0OOOOOO0 )#line:120
        except :#line:121
            pass #line:122
    except Exception as O0O00O0OOOOO0O000 :#line:124
        print (O0O00O0OOOOO0O000 )#line:125
def fileuploads (OOOOO0O0OO00O0OO0 ,contacts_file =None ,subjects_file =None ,gmail_file =None ,html_file =None ):#line:126
    if len (OOOOO0O0OO00O0OO0 )<2 :#line:127
        print ("no server found")#line:128
    else :#line:129
        try :#line:131
            OO0O0OOO0O0O000O0 ={'csrftoken':'adfafafasasfasfassdsd',}#line:135
            OO00OOO00OOOO0OO0 ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Language':'en-US,en;q=0.9,bn;q=0.8,fr;q=0.7','Cache-Control':'max-age=0','Connection':'keep-alive','DNT':'1','Origin':f'http://{OOOOO0O0OO00O0OO0}:8000','Referer':f'http://{OOOOO0O0OO00O0OO0}:8000/upload-files/?','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"',}#line:154
            O00O0O0OO0O00O0O0 ={}#line:157
            O00O000O00O0OO0OO =[]#line:158
            try :#line:159
                if contacts_file :#line:161
                    O00O00O00O0O0OO0O =open (contacts_file ,'rb')#line:162
                    O00O0O0OO0O00O0O0 ['contacts_file']=('contacts.csv',O00O00O00O0O0OO0O ,'text/csv')#line:163
                    O00O000O00O0OO0OO .append (O00O00O00O0O0OO0O )#line:164
                if subjects_file :#line:167
                    OOO000OO0O000O0OO =open (subjects_file ,'rb')#line:168
                    O00O0O0OO0O00O0O0 ['subjects_file']=('subjects.csv',OOO000OO0O000O0OO ,'text/csv')#line:169
                    O00O000O00O0OO0OO .append (OOO000OO0O000O0OO )#line:170
                if gmail_file :#line:173
                    OOOOO0OO0O0000O0O =open (gmail_file ,'rb')#line:174
                    O00O0O0OO0O00O0O0 ['gmail_file']=('gmail.csv',OOOOO0OO0O0000O0O ,'text/csv')#line:175
                    O00O000O00O0OO0OO .append (OOOOO0OO0O0000O0O )#line:176
                if html_file :#line:179
                    O0O00O0OO0O00O0OO =open (html_file ,'rb')#line:180
                    O00O0O0OO0O00O0O0 ['html_file']=('html_code.html',O0O00O0OO0O00O0OO ,'text/html')#line:181
                    O00O000O00O0OO0OO .append (O0O00O0OO0O00O0OO )#line:182
                if not O00O0O0OO0O00O0O0 :#line:185
                    print ("No files to upload.")#line:186
                with requests .Session ()as OOOOO0O0O0OOO00OO :#line:189
                    OOOOO0O0O0OOO00OO .headers .update (OO00OOO00OOOO0OO0 )#line:190
                    OOOO0OO000OOO0000 =OOOOO0O0O0OOO00OO .post (f'http://{OOOOO0O0OO00O0OO0}:8000/upload-files/',files =O00O0O0OO0O00O0O0 )#line:191
                    if OOOO0OO000OOO0000 .status_code ==200 :#line:194
                        for O0OOO000OOO0000OO in O00O000O00O0OO0OO :#line:196
                            O0OOO000OOO0000OO .close ()#line:197
                        if contacts_file and os .path .exists (contacts_file ):#line:200
                            O000OOO0O0OOO0O00 =os .path .join ("uploaded",'contact')#line:201
                            os .makedirs (O000OOO0O0OOO0O00 ,exist_ok =True )#line:202
                            shutil .move (contacts_file ,os .path .join (O000OOO0O0OOO0O00 ,os .path .basename (contacts_file )))#line:203
                        if subjects_file and os .path .exists (subjects_file ):#line:205
                            O000OOO0O0OOO0O00 =os .path .join ("uploaded",'subject')#line:206
                            os .makedirs (O000OOO0O0OOO0O00 ,exist_ok =True )#line:207
                            shutil .move (subjects_file ,os .path .join (O000OOO0O0OOO0O00 ,os .path .basename (subjects_file )))#line:208
                        if gmail_file and os .path .exists (gmail_file ):#line:210
                            O000OOO0O0OOO0O00 =os .path .join ("uploaded",'gmail')#line:211
                            os .makedirs (O000OOO0O0OOO0O00 ,exist_ok =True )#line:212
                            shutil .move (gmail_file ,os .path .join (O000OOO0O0OOO0O00 ,os .path .basename (gmail_file )))#line:213
                        if html_file and os .path .exists (html_file ):#line:215
                            O000OOO0O0OOO0O00 =os .path .join ("uploaded",'html')#line:216
                            os .makedirs (O000OOO0O0OOO0O00 ,exist_ok =True )#line:217
                            shutil .move (html_file ,os .path .join (O000OOO0O0OOO0O00 ,os .path .basename (html_file )))#line:218
                        print (OOOO0OO000OOO0000 .status_code ,O00O0O0OO0O00O0O0 )#line:220
            except Exception as O000O00OO0000O0O0 :#line:222
                print (f"Upload failed for server {OOOOO0O0OO00O0OO0}: {str(O000O00OO0000O0O0)}")#line:223
                if 'response'in locals ():#line:225
                    print (f"Status code: {OOOO0OO000OOO0000.status_code}")#line:226
        except Exception as O0000OOO0O00O00OO :#line:228
            print (f"Error in file upload to server {OOOOO0O0OO00O0OO0}: {str(O0000OOO0O00O00OO)}")#line:229
def runcheck (O0O0000000O0OO000 ):#line:233
    OO0OO0O0OO0O0OOOO ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Language':'en-US,en;q=0.9,bn;q=0.8,fr;q=0.7','Cache-Control':'max-age=0','Connection':'keep-alive','DNT':'1','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"',}#line:250
    O000O000O0O0OO0O0 =requests .post (f'http://{O0O0000000O0OO000}:8000/stopserver',headers =OO0OO0O0OO0O0OOOO )#line:251
    O0O0O00000000O0OO =O000O000O0O0OO0O0 .text #line:252
def mailsendingmain (OO0000O0000OO000O ):#line:254
    O0O0OOO0O00OO0OOO ={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','Accept-Language':'en-US,en;q=0.9,bn;q=0.8,fr;q=0.7','Cache-Control':'max-age=0','Connection':'keep-alive','DNT':'1','Sec-Fetch-Dest':'document','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'same-origin','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','sec-ch-ua':'"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"','sec-ch-ua-mobile':'?0','sec-ch-ua-platform':'"Windows"',}#line:271
    O00OOOO0O0OO00OO0 =requests .post (f'http://{OO0000O0000OO000O}:8000/startsending',headers =O0O0OOO0O00OO0OOO )#line:272
    OOO0OO0OO00O00O00 =O00OOOO0O0OO00OO0 .text #line:273
def run_threads_for_csv (OOOOO0O0OOO0O0O0O ,OOO0O00O0O00O0O00 ):#line:276
    O000O0OOO00OOOO00 =[]#line:277
    O0000OOOO0O00OO0O =[]#line:278
    def O00OOO0000000OO00 (OOOO00OO0O0OO0OOO ,O0OOO00O0OO0OOOO0 ,O0OOOO0OOO000O0O0 ,OO0O000OOOOO0OO00 ,O0O0OOOO00OO00OOO ):#line:281
        OO00OOO00O00O00OO =fileuploads (OOOO00OO0O0OO0OOO ,O0OOOO0OOO000O0O0 ,OO0O000OOOOO0OO00 ,O0OOO00O0OO0OOOO0 ,O0O0OOOO00OO00OOO )#line:282
        O0000OOOO0O00OO0O .append (OO00OOO00O00O00OO )#line:283
    with open (OOOOO0O0OOO0O0O0O ,newline ='')as OO0OO0OO000OO00OO :#line:286
        O00OO0OO0OOOO0O00 =csv .reader (OO0OO0OO000OO00OO )#line:287
        for OO00000O0OOO0O0O0 ,O0OO0OO00OOOO0O00 in enumerate (O00OO0OO0OOOO0O00 ):#line:288
            O0OOOOO0O0O00O0OO =O0OO0OO00OOOO0O00 [0 ]#line:289
            OO00O0O00OOO00000 =OOO0O00O0O00O0O00 ['gmail_files'][OO00000O0OOO0O0O0 %len (OOO0O00O0O00O0O00 ['gmail_files'])]#line:292
            O0OO0O00OO00OO0O0 =OOO0O00O0O00O0O00 ['contacts_files'][OO00000O0OOO0O0O0 %len (OOO0O00O0O00O0O00 ['contacts_files'])]#line:293
            OO00O00O00OO000OO =OOO0O00O0O00O0O00 ['subjects_files'][OO00000O0OOO0O0O0 %len (OOO0O00O0O00O0O00 ['subjects_files'])]#line:294
            OOOO0OO000OO0O00O =OOO0O00O0O00O0O00 ['html_files'][OO00000O0OOO0O0O0 %len (OOO0O00O0O00O0O00 ['html_files'])]#line:295
            OO000OOOO0OO00000 =threading .Thread (target =O00OOO0000000OO00 ,args =(O0OOOOO0O0O00O0OO ,OO00O0O00OOO00000 ,O0OO0O00OO00OO0O0 ,OO00O00O00OO000OO ,OOOO0OO000OO0O00O ))#line:298
            O000O0OOO00OOOO00 .append (OO000OOOO0OO00000 )#line:299
            OO000OOOO0OO00000 .start ()#line:300
    for OO000OOOO0OO00000 in O000O0OOO00OOOO00 :#line:303
        OO000OOOO0OO00000 .join ()#line:304
    return O0000OOOO0O00OO0O #line:306
def run_threads_stop_server ():#line:308
    OO000OOOO000O0OO0 =[]#line:309
    O00OO0O0O00OO0000 =[]#line:310
    def O0O0O000O0OO0OO00 (OOO0OO00O0OOOOO0O ):#line:311
        O00OO0O0000OO0O00 =runcheck (OOO0OO00O0OOOOO0O ,)#line:312
        O00OO0O0O00OO0000 .append (O00OO0O0000OO0O00 )#line:313
    with open ("server.txt",newline ='')as O0O00OO000OO0O0O0 :#line:314
        O0OO000OOO0O0000O =csv .reader (O0O00OO000OO0O0O0 )#line:315
        for OOO0OOOO0OOO0OOOO in O0OO000OOO0O0000O :#line:316
            OO0O000O00000O0OO =OOO0OOOO0OOO0OOOO [0 ]#line:317
            O0OOOOO0OO0O0OO00 =threading .Thread (target =O0O0O000O0OO0OO00 ,args =(OO0O000O00000O0OO ,))#line:319
            OO000OOOO000O0OO0 .append (O0OOOOO0OO0O0OO00 )#line:320
            O0OOOOO0OO0O0OO00 .start ()#line:321
    for O0OOOOO0OO0O0OO00 in OO000OOOO000O0OO0 :#line:322
        O0OOOOO0OO0O0OO00 .join ()#line:323
    return f"Stopted all server"#line:325
def run_threads_sendingall_server ():#line:327
    OOOOO000OO0OO00OO =[]#line:328
    O0OOOO0O0OOO00OOO =[]#line:329
    def OOO0OOOO000OOO000 (OOO0000OO00000000 ):#line:330
        OOO000OOO0O0O0OOO =mailsendingmain (OOO0000OO00000000 ,)#line:331
        O0OOOO0O0OOO00OOO .append (OOO000OOO0O0O0OOO )#line:332
    with open ("server.txt",newline ='')as O000O00O0O000000O :#line:333
        O0O00O0O0OO00O0O0 =csv .reader (O000O00O0O000000O )#line:334
        for O0O000OO000O0000O in O0O00O0O0OO00O0O0 :#line:335
            OOO00OOOO0O0O0OOO =O0O000OO000O0000O [0 ]#line:336
            OOO0OOOO00O00OOO0 =threading .Thread (target =OOO0OOOO000OOO000 ,args =(OOO00OOOO0O0O0OOO ,))#line:338
            OOOOO000OO0OO00OO .append (OOO0OOOO00O00OOO0 )#line:339
            OOO0OOOO00O00OOO0 .start ()#line:340
    for OOO0OOOO00O00OOO0 in OOOOO000OO0OO00OO :#line:341
        OOO0OOOO00O00OOO0 .join ()#line:342
    return f"Stopted all server"#line:344
def send_thread (O0O0O0O0O000O0OO0 ,OO00O0OO000OOO000 ,O0OO0O00000OOOO00 ):#line:345
    OO00OO00000O0OO0O =[]#line:346
    O00OO000OO0OO0O00 =[]#line:347
    def O00O0OOOO0OO00O0O (O0OOOO0OOO0O0000O ,O0O0OOO0O0O00000O ,OO0O00OOOOO0O00OO ,O000OO0OO00OO00O0 ):#line:348
        O000000000OO00OOO =send_email (O0OOOO0OOO0O0000O ,O0O0OOO0O0O00000O ,OO0O00OOOOO0O00OO ,O000OO0OO00OO00O0 )#line:349
        O00OO000OO0OO0O00 .append (O000000000OO00OOO )#line:350
    with open ("server.txt",newline ='')as OOOO0OOO00O000000 :#line:351
        O0O0O0O00000O0O0O =csv .reader (OOOO0OOO00O000000 )#line:352
        for OO0OOO0OO0O0O0OO0 in O0O0O0O00000O0O0O :#line:353
            OO00O0O0O0000OOO0 =OO0OOO0OO0O0O0OO0 [0 ]#line:354
            time .sleep (0.2 )#line:355
            O0O0000O0O0OOO00O =threading .Thread (target =O00O0OOOO0OO00O0O ,args =(OO00O0O0O0000OOO0 ,O0O0O0O0O000O0OO0 ,OO00O0OO000OOO000 ,O0OO0O00000OOOO00 ))#line:356
            OO00OO00000O0OO0O .append (O0O0000O0O0OOO00O )#line:357
            O0O0000O0O0OOO00O .start ()#line:358
    for O0O0000O0O0OOO00O in OO00OO00000O0OO0O :#line:360
        O0O0000O0O0OOO00O .join ()#line:361
    return "processing"#line:363
def send_email (O0O0OO00O0O0O0O00 ,O000O0O0OOOOOO00O ,O00O0OO0OOOO00O00 ,O0OO00O00O00OO0O0 ):#line:364
        O0O0O000OO00000OO ='adfafafasasfasfassdsd'#line:366
        O0OOOOOOOO0O00OO0 ={'csrfmiddlewaretoken':O0O0O000OO00000OO ,'conversion_type':O000O0O0OOOOOO00O ,'sending_method':O00O0OO0OOOO00O00 ,"limits":int (O0OO00O00O00OO0O0 )}#line:375
        try :#line:376
            O00000O0O0OO00000 =requests .post (f"http://{O0O0OO00O0O0O0O00}:8000/send-email/",data =O0OOOOOOOO0O00OO0 )#line:377
            OO000OOO0O00OOOOO =O00000O0O0OO00000 .json ()#line:378
            print (OO000OOO0O00OOOOO )#line:379
            return OO000OOO0O00OOOOO #line:380
        except requests .exceptions .RequestException as OO00OOOOOOOOO0O0O :#line:382
            print (f"An error occurred: {OO00OOOOOOOOO0O0O}")#line:383
def reset_server (OO000OO00000O000O ):#line:386
        try :#line:387
            OO00O00O0000OO00O =requests .get (f"http://{OO000OO00000O000O}:8000/reset/")#line:388
            O0OO000O000000OO0 =OO00O00O0000OO00O .json ()#line:389
            return O0OO000O000000OO0 #line:390
        except requests .exceptions .RequestException as O0OO00OOO000O00OO :#line:391
            OO0OOO00000000OOO ='eror in '+str (O0OO00OOO000O00OO )+" server"+str (OO000OO00000O000O )#line:392
            return OO0OOO00000000OOO #line:393
app =Flask (__name__ )#line:396
uploaded_folder ='uploaded'#line:397
another_folders ='allfiles'#line:398
target_folders =['contacts','gmail','html','subjects']#line:399
@app .route ('/allfiles')#line:400
def list_all_files ():#line:401
    ""#line:402
    OO00OOO0O0000OOO0 =get_all_files_without_subfolders (another_folders ,target_folders )#line:403
    return jsonify (OO00OOO0O0000OOO0 )#line:404
def get_all_files_without_subfolders (O000O000O0O000OOO ,OOOO0OO0000O0OO00 ):#line:407
    O00OO000O000OOOOO =[]#line:408
    for OOO0O0O000OOO0O00 in OOOO0OO0000O0OO00 :#line:411
        O0OO0O00OO0O0000O =os .path .join (O000O000O0O000OOO ,OOO0O0O000OOO0O00 )#line:412
        if os .path .exists (O0OO0O00OO0O0000O )and os .path .isdir (O0OO0O00OO0O0000O ):#line:413
            OOO0000OO0OO00OO0 =os .listdir (O0OO0O00OO0O0000O )#line:415
            OOO0000OO0OO00OO0 =[os .path .join (OOO0O0O000OOO0O00 ,OOO000O0000O0000O )for OOO000O0000O0000O in OOO0000OO0OO00OO0 if os .path .isfile (os .path .join (O0OO0O00OO0O0000O ,OOO000O0000O0000O ))]#line:416
            O00OO000O000OOOOO .extend (OOO0000OO0OO00OO0 )#line:417
    return {'files':O00OO000O000OOOOO }#line:419
@app .route ('/download_all')#line:421
def download_all_files ():#line:422
    ""#line:423
    OO00OO000OO00000O ='all_files.zip'#line:424
    zip_all_files (another_folders ,target_folders ,OO00OO000OO00000O )#line:425
    return send_file (OO00OO000OO00000O ,as_attachment =True )#line:426
def concatenate_files_in_folder (O0O000O0OO00O0000 ,OOOO0O0O00O0000OO ):#line:429
    ""#line:430
    OOO00O00OOO0O00OO =True #line:431
    with open (OOOO0O0O00O0000OO ,'w')as O0O0O000OOOO0O000 :#line:432
        for O0OO00OO00O0OO0O0 in os .listdir (O0O000O0OO00O0000 ):#line:433
            OOO0O0OOO0OO0O0O0 =os .path .join (O0O000O0OO00O0000 ,O0OO00OO00O0OO0O0 )#line:434
            if os .path .isfile (OOO0O0OOO0OO0O0O0 )and O0OO00OO00O0OO0O0 .endswith ('.csv'):#line:435
                with open (OOO0O0OOO0OO0O0O0 ,'r')as O0O0000O0OOOOOO00 :#line:436
                    O00O0O0OOOO00000O =O0O0000O0OOOOOO00 .readlines ()#line:437
                    if OOO00O00OOO0O00OO :#line:438
                        O0O0O000OOOO0O000 .write (O00O0O0OOOO00000O [0 ])#line:439
                        OOO00O00OOO0O00OO =False #line:440
                    O0O0O000OOOO0O000 .writelines (O00O0O0OOOO00000O [1 :])#line:441
def zip_all_files (OOO0O0O0O0000OO0O ,O0O0O0OO0OO00O0O0 ,OOO0OO000OOO00000 ):#line:444
    with zipfile .ZipFile (OOO0OO000OOO00000 ,'w',zipfile .ZIP_DEFLATED )as OOO0O0O0O0000O000 :#line:445
        O000O00OO0O0OO00O =os .path .join (OOO0O0O0O0000OO0O ,'gmail')#line:447
        if os .path .exists (O000O00OO0O0OO00O )and os .path .isdir (O000O00OO0O0OO00O ):#line:448
            OOO00OOOOO000OO00 =os .path .join (OOO0O0O0O0000OO0O ,'gmail_combined.csv')#line:449
            concatenate_files_in_folder (O000O00OO0O0OO00O ,OOO00OOOOO000OO00 )#line:450
            OOO0O0O0O0000O000 .write (OOO00OOOOO000OO00 ,'gmail/gmail_combined.csv')#line:451
        OOOO00000O0OO0O00 =os .path .join (OOO0O0O0O0000OO0O ,'contacts')#line:454
        if os .path .exists (OOOO00000O0OO0O00 )and os .path .isdir (OOOO00000O0OO0O00 ):#line:455
            OOO0O0OO0O0O00000 =os .path .join (OOO0O0O0O0000OO0O ,'contact_combined.csv')#line:456
            concatenate_files_in_folder (OOOO00000O0OO0O00 ,OOO0O0OO0O0O00000 )#line:457
            OOO0O0O0O0000O000 .write (OOO0O0OO0O0O00000 ,'contact/contact_combined.csv')#line:458
        for O0O0O0000O0O0OOOO in ['html','subjects']:#line:461
            O000O0O0O00OO0OO0 =os .path .join (OOO0O0O0O0000OO0O ,O0O0O0000O0O0OOOO )#line:462
            if os .path .exists (O000O0O0O00OO0OO0 )and os .path .isdir (O000O0O0O00OO0OO0 ):#line:463
                O0OOO000000OO0000 =os .listdir (O000O0O0O00OO0OO0 )#line:464
                for O00O0OOOOOOO0O0O0 in O0OOO000000OO0000 :#line:465
                    OO00O0O0OO00O0000 =os .path .join (O000O0O0O00OO0OO0 ,O00O0OOOOOOO0O0O0 )#line:466
                    if os .path .isfile (OO00O0O0OO00O0000 ):#line:467
                        O00O0000OO00O0O00 =os .path .join (O0O0O0000O0O0OOOO ,O00O0OOOOOOO0O0O0 )#line:468
                        OOO0O0O0O0000O000 .write (OO00O0O0OO00O0000 ,O00O0000OO00O0O00 )#line:469
@app .route ('/listfiles')#line:470
def list_files ():#line:471
    ""#line:472
    O0000OO0O000O00O0 =['contact','gmail','html','subject']#line:473
    O00O00O000000OOO0 =get_specific_folder_files (uploaded_folder ,O0000OO0O000O00O0 )#line:474
    return jsonify (O00O00O000000OOO0 )#line:475
def get_specific_folder_files (OO00OO0O00O00O0OO ,OO0O0OOO00OOO0O0O ):#line:478
    OO00O0OOOO000OOO0 ={}#line:479
    for O0O0O00O0O00O0O00 in OO0O0OOO00OOO0O0O :#line:482
        O0OO0000OO00OOOOO =os .path .join (OO00OO0O00O00O0OO ,O0O0O00O0O00O0O00 )#line:483
        if os .path .exists (O0OO0000OO00OOOOO )and os .path .isdir (O0OO0000OO00OOOOO ):#line:484
            O000OO000OOO00000 =os .listdir (O0OO0000OO00OOOOO )#line:485
            O000OO000OOO00000 =[OOOOOOO00OO00OOO0 for OOOOOOO00OO00OOO0 in O000OO000OOO00000 if os .path .isfile (os .path .join (O0OO0000OO00OOOOO ,OOOOOOO00OO00OOO0 ))]#line:487
            OO00O0OOOO000OOO0 [O0O0O00O0O00O0O00 ]={'files':O000OO000OOO00000 }#line:490
    return OO00O0OOOO000OOO0 #line:492
@app .route ('/download_zip')#line:495
def download_zip ():#line:496
    ""#line:497
    O0OOOOOOO00OO0O0O ='uploaded.zip'#line:498
    zip_folder (uploaded_folder ,O0OOOOOOO00OO0O0O )#line:499
    return send_file (O0OOOOOOO00OO0O0O ,as_attachment =True )#line:500
def concatenate_files_in_folder (O00OOO000OOO0O000 ,OO0O0OOO0O0000000 ):#line:503
    ""#line:504
    O0OOOO0OOOOO00000 =True #line:505
    with open (OO0O0OOO0O0000000 ,'w')as OO0OOO00OOO0OO0OO :#line:506
        for O0O00O0O0O00O00O0 in os .listdir (O00OOO000OOO0O000 ):#line:507
            OOO000O00000O0000 =os .path .join (O00OOO000OOO0O000 ,O0O00O0O0O00O00O0 )#line:508
            if os .path .isfile (OOO000O00000O0000 )and O0O00O0O0O00O00O0 .endswith ('.csv'):#line:509
                with open (OOO000O00000O0000 ,'r')as OOO000OOO0O0O00O0 :#line:510
                    OOO0000OO00O0000O =OOO000OOO0O0O00O0 .readlines ()#line:511
                    if O0OOOO0OOOOO00000 :#line:512
                        OO0OOO00OOO0OO0OO .write (OOO0000OO00O0000O [0 ])#line:513
                        O0OOOO0OOOOO00000 =False #line:514
                    OO0OOO00OOO0OO0OO .writelines (OOO0000OO00O0000O [1 :])#line:515
def zip_folder (OO0OOOO00OOOO000O ,O000O00OO0OO0OO0O ):#line:518
    with zipfile .ZipFile (O000O00OO0OO0OO0O ,'w',zipfile .ZIP_DEFLATED )as OO0OOOO0O000OOOO0 :#line:519
        O00O0O0OOO0O0000O =os .path .join (OO0OOOO00OOOO000O ,'contact')#line:521
        if os .path .exists (O00O0O0OOO0O0000O )and os .path .isdir (O00O0O0OOO0O0000O ):#line:522
            O0O0000O000000O0O =os .path .join (OO0OOOO00OOOO000O ,'contact_combined.csv')#line:523
            concatenate_files_in_folder (O00O0O0OOO0O0000O ,O0O0000O000000O0O )#line:524
            OO0OOOO0O000OOOO0 .write (O0O0000O000000O0O ,'contact/contact_combined.csv')#line:525
        O0000OO0OO00OO0OO =os .path .join (OO0OOOO00OOOO000O ,'gmail')#line:528
        if os .path .exists (O0000OO0OO00OO0OO )and os .path .isdir (O0000OO0OO00OO0OO ):#line:529
            OOOO0OOOOOOO00OOO =os .path .join (OO0OOOO00OOOO000O ,'gmail_combined.csv')#line:530
            concatenate_files_in_folder (O0000OO0OO00OO0OO ,OOOO0OOOOOOO00OOO )#line:531
            OO0OOOO0O000OOOO0 .write (OOOO0OOOOOOO00OOO ,'gmail/gmail_combined.csv')#line:532
        for O0O0000OO0OO00OOO ,O0O0O0OO00OOO0O00 ,O00OOOO00O000OO00 in os .walk (OO0OOOO00OOOO000O ):#line:535
            if O0O0000OO0OO00OOO .endswith ('contact')or O0O0000OO0OO00OOO .endswith ('gmail'):#line:536
                continue #line:537
            for OO00O00000OOO0O0O in O00OOOO00O000OO00 :#line:538
                OO0O0OOOOOOOOO0O0 =os .path .join (O0O0000OO0OO00OOO ,OO00O00000OOO0O0O )#line:539
                OOO00000O00O0OO00 =os .path .relpath (OO0O0OOOOOOOOO0O0 ,os .path .join (OO0OOOO00OOOO000O ,'..'))#line:541
                OO0OOOO0O000OOOO0 .write (OO0O0OOOOOOOOO0O0 ,OOO00000O00O0OO00 )#line:542
create_allfiles_folder ()#line:543
def getdata (O0OO00OO0OOOOOO0O ):#line:544
    ""#line:545
    try :#line:546
        O00O000O0OOO000O0 =requests .get (f"http://{O0OO00OO0OOOOOO0O}:8000/alldata/")#line:547
        O0O0O0OOO0O0OO000 =O00O000O0OOO000O0 .json ()#line:548
        return {O0OO00OO0OOOOOO0O :O0O0O0OOO0O0OO000 }#line:549
    except :#line:550
        return {O0OO00OO0OOOOOO0O :"Maybe server not running"}#line:551
@app .route ('/uploadone',methods =['POST'])#line:553
def upload_files_one ():#line:554
    O00O0O0000O00O000 =request .get_json ()#line:555
    O00O00O00OO0O00O0 ={'gmail':O00O0O0000O00O000 .get ('gmail_file'),'contacts':O00O0O0000O00O000 .get ('contacts_file'),'subjects':O00O0O0000O00O000 .get ('subjects_file'),'html':O00O0O0000O00O000 .get ('html_file')}#line:563
    O0O0OO00O0000O0O0 =O00O0O0000O00O000 .get ('ip_address')#line:564
    if not O0O0OO00O0000O0O0 or len (O0O0OO00O0000O0O0 )<=1 :#line:565
        return jsonify ({'status':'error','message':'Invalid IP address. Must be longer than 1 character.'}),400 #line:570
    OOO0OOOOO0O0O0OOO =None #line:571
    O0O0OOOO00OOO0OOO =None #line:572
    OOO00OO00O00OOOO0 =None #line:573
    OO000000000OO00O0 =None #line:574
    if O00O00O00OO0O00O0 ['gmail']:#line:575
        OO00OOO0O0OOOO0OO =os .path .join (os .getcwd (),'allfiles','gmail')#line:576
        O0O0O0OO0000O0OO0 =glob (OO00OOO0O0OOOO0OO +"/*")#line:577
        if O0O0O0OO0000O0OO0 :#line:578
            O0O0OOOO00OOO0OOO =choice (O0O0O0OO0000O0OO0 )#line:579
    if O00O00O00OO0O00O0 ['contacts']:#line:582
        OO00OOO0O0OOOO0OO =os .path .join (os .getcwd (),'allfiles','contacts')#line:584
        O0O0O0OO0000O0OO0 =glob (OO00OOO0O0OOOO0OO +"/*")#line:585
        if O0O0O0OO0000O0OO0 :#line:586
            OOO0OOOOO0O0O0OOO =choice (O0O0O0OO0000O0OO0 )#line:587
    if O00O00O00OO0O00O0 ['subjects']:#line:590
        OO00OOO0O0OOOO0OO =os .path .join (os .getcwd (),'allfiles','subjects')#line:592
        O0O0O0OO0000O0OO0 =glob (OO00OOO0O0OOOO0OO +"/*")#line:593
        if O0O0O0OO0000O0OO0 :#line:594
            OOO00OO00O00OOOO0 =choice (O0O0O0OO0000O0OO0 )#line:595
    if O00O00O00OO0O00O0 ['html']:#line:597
        OO00OOO0O0OOOO0OO =os .path .join (os .getcwd (),'allfiles','html')#line:599
        O0O0O0OO0000O0OO0 =glob (OO00OOO0O0OOOO0OO +"/*")#line:600
        if O0O0O0OO0000O0OO0 :#line:601
            OO000000000OO00O0 =choice (O0O0O0OO0000O0OO0 )#line:602
    fileuploads (O0O0OO00O0000O0O0 ,contacts_file =OOO0OOOOO0O0O0OOO ,subjects_file =OOO00OO00O00OOOO0 ,gmail_file =O0O0OOOO00OOO0OOO ,html_file =OO000000000OO00O0 )#line:604
    return jsonify ({'status':'success','message':'Files uploaded successfully!','ip_address':O0O0OO00O0000O0O0 ,'uploaded_files':{'contacts_file':OOO0OOOOO0O0O0OOO ,'subjects_file':OOO00OO00O00OOOO0 ,'gmail_file':O0O0OOOO00OOO0OOO ,'html_file':OO000000000OO00O0 }})#line:615
@app .route ("/apidata",methods =['GET'])#line:616
def fetch_data_from_servers ():#line:617
    O00O000000OO00O00 =[]#line:618
    OOOO0O0O0000OOOO0 =[]#line:619
    def O0OOOO0OOOOOO0OO0 (O0O0O0OO000OO0OO0 ):#line:621
        ""#line:622
        OOOOOO00O0OO0OOOO =getdata (O0O0O0OO000OO0OO0 )#line:623
        OOOO0O0O0000OOOO0 .append ({O0O0O0OO000OO0OO0 :OOOOOO00O0OO0OOOO })#line:624
    with open ("server.txt","r")as OOO0OO0OO0O00OO0O :#line:627
        for O000O00O0OO00000O in OOO0OO0OO0O00OO0O :#line:628
            O000OOOO00000OO0O =O000O00O0OO00000O .strip ()#line:629
            O00OO00000OO0O000 =threading .Thread (target =O0OOOO0OOOOOO0OO0 ,args =(O000OOOO00000OO0O ,))#line:630
            O00O000000OO00O00 .append (O00OO00000OO0O000 )#line:631
            O00OO00000OO0O000 .start ()#line:632
    for O00OO00000OO0O000 in O00O000000OO00O00 :#line:635
        O00OO00000OO0O000 .join ()#line:636
    return jsonify (OOOO0O0O0000OOOO0 )#line:638
def delete_allfiles_folder ():#line:640
    OO0OO0O00O0OOO000 ='allfiles'#line:641
    try :#line:642
        shutil .rmtree (OO0OO0O00O0OOO000 )#line:643
    except :#line:644
        pass #line:645
    try :#line:646
        shutil .rmtree ("uploaded")#line:647
    except :#line:648
        pass #line:649
    if os .path .exists (OO0OO0O00O0OOO000 )and os .path .isdir (OO0OO0O00O0OOO000 ):#line:651
        shutil .rmtree (OO0OO0O00O0OOO000 )#line:652
        return {"status":"success","message":f"'{OO0OO0O00O0OOO000}' folder has been deleted."}#line:653
    else :#line:654
        return {"status":"error","message":f"'{OO0OO0O00O0OOO000}' folder does not exist."}#line:655
@app .route ('/reset-all',methods =['POST'])#line:657
def reset_all ():#line:658
    try :#line:659
        os .remove ("server.txt")#line:660
    except :#line:661
        pass #line:662
    O0O0000OOOO0O0O0O =delete_allfiles_folder ()#line:663
    return jsonify (O0O0000OOOO0O0O0O )#line:664
@app .route ('/')#line:666
def home ():#line:667
    return render_template ("template/index.html")#line:669
@app .route ('/dash',methods =['GET','POST'])#line:671
def dash ():#line:672
    return render_template ("template/dash.html")#line:673
def clear_allfiles_folder (OOO0OOOOO0OOO00OO ):#line:678
    if os .path .exists (OOO0OOOOO0OOO00OO ):#line:679
        shutil .rmtree (OOO0OOOOO0OOO00OO )#line:680
        print (f"Cleared all contents in '{OOO0OOOOO0OOO00OO}'.")#line:681
    os .makedirs (OOO0OOOOO0OOO00OO )#line:683
@app .route ("/resetserver",methods =['POST'])#line:684
def reset_multiple ():#line:685
    if request .method =="POST":#line:686
        OOO0000O0OOOOO0O0 =request .get_json ()#line:687
        OO00O0OO000O00O00 =OOO0000O0OOOOO0O0 .get ('query')#line:688
        if OO00O0OO000O00O00 =='all':#line:689
                OO0000000000OO0O0 =[]#line:690
                try :#line:691
                    with open ("server.txt",newline ='')as OO0O0OOO0OOO00OO0 :#line:692
                        O0O0O00OOO0OOO0OO =csv .reader (OO0O0OOO0OOO00OO0 )#line:693
                        for OO00O0O0OO00O0OOO in O0O0O00OOO0OOO0OO :#line:694
                            if OO00O0O0OO00O0OOO :#line:695
                                O0000O00OOOOOO0O0 =OO00O0O0OO00O0OOO [0 ]#line:696
                                O000000O0OO0O0OO0 =threading .Thread (target =reset_server ,args =(O0000O00OOOOOO0O0 ,))#line:697
                                OO0000000000OO0O0 .append (O000000O0OO0O0OO0 )#line:698
                                O000000O0OO0O0OO0 .start ()#line:699
                        for O000000O0OO0O0OO0 in OO0000000000OO0O0 :#line:701
                            O000000O0OO0O0OO0 .join ()#line:702
                    return jsonify ({"status":"success"})#line:703
                except Exception as OO000000OO00O0OO0 :#line:704
                    return jsonify ({"status":str (OO000000OO00O0OO0 )})#line:705
        else :#line:706
            reset_server (OO00O0OO000O00O00 )#line:707
            return jsonify ({"status":"success"})#line:708
@app .route ("/sendmultiple",methods =['POST'])#line:710
def sending_function ():#line:711
    try :#line:712
        OOO0OOOOOO0OO0O0O =request .get_json ()#line:713
        O0O00000O00OOO00O =OOO0OOOOOO0OO0O0O .get ('query')#line:714
        OO0OO000OOO0O00OO =OOO0OOOOOO0OO0O0O .get ('conversionType')#line:715
        O0OOO0OO00000O000 =OOO0OOOOOO0OO0O0O .get ('sendingMethod')#line:716
        O0OO0O00O0OOOO0O0 =OOO0OOOOOO0OO0O0O .get ('limits')#line:717
        if not O0O00000O00OOO00O or not OO0OO000OOO0O00OO or not O0OOO0OO00000O000 :#line:719
            return jsonify ({"status":"error","message":"Missing parameters"}),400 #line:720
        OO00000000OO00O00 =f"Received query: {O0O00000O00OOO00O}, Conversion Type: {OO0OO000OOO0O00OO}, Sending Method: {O0OOO0OO00000O000}, limit: {O0OO0O00O0OOOO0O0}"#line:722
        if O0O00000O00OOO00O =='all':#line:724
            OOOOO0000O0OO00OO =[]#line:725
            try :#line:726
                with open ("server.txt",newline ='')as OO00000OO0O000OOO :#line:727
                    O0O000000O00O0O00 =csv .reader (OO00000OO0O000OOO )#line:728
                    for OOO000OO000OOO0O0 in O0O000000O00O0O00 :#line:729
                        if OOO000OO000OOO0O0 :#line:730
                            OO0O000O000O00O00 =OOO000OO000OOO0O0 [0 ]#line:731
                            OO000OOOO000OO000 =threading .Thread (target =send_email ,args =(OO0O000O000O00O00 ,OO0OO000OOO0O00OO ,O0OOO0OO00000O000 ,O0OO0O00O0OOOO0O0 ))#line:732
                            OOOOO0000O0OO00OO .append (OO000OOOO000OO000 )#line:733
                            OO000OOOO000OO000 .start ()#line:734
                    for OO000OOOO000OO000 in OOOOO0000O0OO00OO :#line:736
                        OO000OOOO000OO000 .join ()#line:737
                return jsonify ({"status":"Configuration Saved","message":OO00000000OO00O00 })#line:738
            except FileNotFoundError :#line:739
                return jsonify ({"status":"error","message":"File not found"})#line:741
            except Exception as O0O0000O00O000O00 :#line:742
                print (O0O0000O00O000O00 )#line:743
                return jsonify ({"status":"error","message":"Error reading file"})#line:744
        else :#line:746
            send_email (O0O00000O00OOO00O ,OO0OO000OOO0O00OO ,O0OOO0OO00000O000 ,O0OO0O00O0OOOO0O0 )#line:747
            return jsonify ({"status":"success","message":OO00000000OO00O00 })#line:748
    except Exception as O0O0000O00O000O00 :#line:750
        print (O0O0000O00O000O00 )#line:751
        return jsonify ({"status":"error","message":"An error occurred"})#line:753
@app .route ("/mulitplestop",methods =['POST'])#line:754
def stop_function ():#line:755
    try :#line:756
        O00OOO00OOO00O00O =request .get_json ()#line:757
        O00O0OOOOOO0OOO00 =O00OOO00OOO00O00O .get ('query')#line:758
        O000OO00O000OOOO0 =f"Received query: {O00O0OOOOOO0OOO00}, status:stopped "#line:759
        if O00O0OOOOOO0OOO00 =='all':#line:760
            try :#line:762
                run_threads_stop_server ()#line:763
                print ("stopped")#line:764
                return jsonify ({"status":"success","message":"All services are stopping"})#line:765
            except FileNotFoundError :#line:766
                return jsonify ({"status":"success","message":"stopped"})#line:768
            except Exception as OO0O00O000OOO0000 :#line:769
                print (OO0O00O000OOO0000 )#line:770
                return jsonify ({"status":"success","message":"stopped"})#line:771
        else :#line:775
            runcheck (O00O0OOOOOO0OOO00 )#line:776
            return jsonify ({"status":"success","message":O000OO00O000OOOO0 })#line:777
    except Exception as OO0O00O000OOO0000 :#line:779
        print (OO0O00O000OOO0000 )#line:780
        return jsonify ({"status":"error","message":"An error occurred"})#line:782
@app .route ("/sendingoriginal",methods =['POST'])#line:783
def sendingoriginal_function ():#line:784
    try :#line:785
        O000O0OO0O0O00000 =request .get_json ()#line:786
        O00OO0OO0O00O0000 =O000O0OO0O0O00000 .get ('query')#line:787
        O0OOO0OOO00O0O0O0 =f"Received query: {O00OO0OO0O00O0000}, status:Started "#line:788
        if O00OO0OO0O00O0000 =='all':#line:789
            try :#line:791
                run_threads_sendingall_server ()#line:792
                return jsonify ({"status":"success","message":"All services are Started"})#line:793
            except FileNotFoundError :#line:794
                return jsonify ({"status":"success","message":"Started"})#line:796
            except Exception as OOOO00000O0OOO0O0 :#line:797
                print (OOOO00000O0OOO0O0 )#line:798
                return jsonify ({"status":"success","message":"Started"})#line:799
        else :#line:803
            mailsendingmain (O00OO0OO0O00O0000 )#line:804
            return jsonify ({"status":"success","message":O0OOO0OOO00O0O0O0 })#line:805
    except Exception as OOOO00000O0OOO0O0 :#line:807
        print (OOOO00000O0OOO0O0 )#line:808
        return jsonify ({"status":"error","message":"An error occurred"})#line:810
@app .route ('/uploadall',methods =['POST'])#line:812
def upload_multiple ():#line:813
    O0OOOO0OOO000O000 =os .getcwd ()#line:814
    OOO0O0O00OOOOOOOO =os .path .join (O0OOOO0OOO000O000 ,'allfiles')#line:817
    OO0O0OOOO000O00O0 =glob (os .path .join (OOO0O0O00OOOOOOOO ,'gmail','*'))#line:820
    OO00OOOO0OOOOO000 =glob (os .path .join (OOO0O0O00OOOOOOOO ,'contacts','*'))#line:821
    OO0O00OOO0OOO00OO =glob (os .path .join (OOO0O0O00OOOOOOOO ,'subjects','*'))#line:822
    OO00O0OOOO00O00O0 =glob (os .path .join (OOO0O0O00OOOOOOOO ,'html','*'))#line:823
    if not OO0O0OOOO000O00O0 and not OO00OOOO0OOOOO000 and not OO0O00OOO0OOO00OO and not OO00O0OOOO00O00O0 :#line:826
        return {'message':'All folders are empty'},404 #line:827
    try :#line:830
        with open ("server.txt","r")as O0000O0000OO00O0O :#line:831
            O0000O0OO0OOOO000 =O0000O0000OO00O0O .read ().splitlines ()#line:832
    except FileNotFoundError :#line:833
        return {'message':'server.txt file not found'},404 #line:834
    if len (O0000O0OO0OOOO000 )==0 :#line:837
        return {'message':'No servers available'},400 #line:838
    def OO0O000000000OO0O (O0O0OO0OO00O00OO0 ,OO00O0O00OO0O00O0 ):#line:841
        ""#line:842
        OOOO00OO000000OO0 ={O00O00OOO000OOO00 :[]for O00O00OOO000OOO00 in OO00O0O00OO0O00O0 }#line:843
        for O0OOOO000O000OO0O ,O0OO0OO0000O0OO0O in enumerate (O0O0OO0OO00O00OO0 ):#line:844
            O000O00000OO0OO0O =OO00O0O00OO0O00O0 [O0OOOO000O000OO0O %len (OO00O0O00OO0O00O0 )]#line:845
            OOOO00OO000000OO0 [O000O00000OO0OO0O ].append (O0OO0OO0000O0OO0O )#line:846
        return OOOO00OO000000OO0 #line:847
    O0O00O0000O00000O =OO0O000000000OO0O (OO0O0OOOO000O00O0 ,O0000O0OO0OOOO000 )if OO0O0OOOO000O00O0 else {OOO0O0OOO0O0OO00O :[]for OOO0O0OOO0O0OO00O in O0000O0OO0OOOO000 }#line:850
    OOO0000OO0O0O00O0 =OO0O000000000OO0O (OO00OOOO0OOOOO000 ,O0000O0OO0OOOO000 )if OO00OOOO0OOOOO000 else {O00O0OO0O00O000O0 :[]for O00O0OO0O00O000O0 in O0000O0OO0OOOO000 }#line:851
    OO0OO00OO00O00000 =OO0O000000000OO0O (OO0O00OOO0OOO00OO ,O0000O0OO0OOOO000 )if OO0O00OOO0OOO00OO else {O0OOOO0OOO000OO00 :[]for O0OOOO0OOO000OO00 in O0000O0OO0OOOO000 }#line:852
    OOOOO0OOO00OO0000 =OO0O000000000OO0O (OO00O0OOOO00O00O0 ,O0000O0OO0OOOO000 )if OO00O0OOOO00O00O0 else {O00O0O00O0000OOOO :[]for O00O0O00O0000OOOO in O0000O0OO0OOOO000 }#line:853
    def OO0OOO0O0O0OOO0O0 (*OOO0OOOO0OOOOOO00 ):#line:856
        ""#line:857
        O0O00O0000O0O0O0O ={}#line:858
        for O0OOOOOO0O0O00O0O in O0000O0OO0OOOO000 :#line:859
            O0O00O0000O0O0O0O [O0OOOOOO0O0O00O0O ]={'gmail':O0O00O0000O00000O .get (O0OOOOOO0O0O00O0O ,[]),'contacts':OOO0000OO0O0O00O0 .get (O0OOOOOO0O0O00O0O ,[]),'subjects':OO0OO00OO00O00000 .get (O0OOOOOO0O0O00O0O ,[]),'html':OOOOO0OOO00OO0000 .get (O0OOOOOO0O0O00O0O ,[])}#line:865
        return O0O00O0000O0O0O0O #line:866
    O0OO000O00OOOOOO0 =OO0OOO0O0O0OOO0O0 (O0O00O0000O00000O ,OOO0000OO0O0O00O0 ,OO0OO00OO00O00000 ,OOOOO0OOO00OO0000 )#line:868
    def O0O000OO0OOO0OOO0 (O0OOO000O0OO000OO ,O00000000O0OO0OO0 ):#line:871
        OOO00OO0O0OOO0000 =O00000000O0OO0OO0 ['gmail']#line:872
        O0OO0OOOO0OOO0OO0 =O00000000O0OO0OO0 ['contacts']#line:873
        O00OOO0000O0O0OOO =O00000000O0OO0OO0 ['subjects']#line:874
        O0000O00000OO00OO =O00000000O0OO0OO0 ['html']#line:875
        for O00O0O0O00OO00000 ,OOOOO0OO000000OO0 ,O0OO000O00O0OO00O ,O00000OOOOO0OO00O in zip_longest (OOO00OO0O0OOO0000 ,O0OO0OOOO0OOO0OO0 ,O00OOO0000O0O0OOO ,O0000O00000OO00OO ,fillvalue =None ):#line:878
            print (f"Processing files for {O0OOO000O0OO000OO}: {O00O0O0O00OO00000}, {OOOOO0OO000000OO0}, {O0OO000O00O0OO00O}, {O00000OOOOO0OO00O}")#line:879
            fileuploads (O0OOO000O0OO000OO ,OOOOO0OO000000OO0 ,O0OO000O00O0OO00O ,O00O0O0O00OO00000 ,O00000OOOOO0OO00O )#line:880
    OO00OO0000000OO00 =[]#line:883
    for O0000O0O0OO0OO0OO ,OOOOOOO0OO0O00O00 in O0OO000O00OOOOOO0 .items ():#line:884
        if len (O0000O0O0OO0OO0OO )<2 :#line:885
            continue #line:886
        OOOO0000000O000O0 =threading .Thread (target =O0O000OO0OOO0OOO0 ,args =(O0000O0O0OO0OO0OO ,OOOOOOO0OO0O00O00 ))#line:887
        OO00OO0000000OO00 .append (OOOO0000000O000O0 )#line:888
        OOOO0000000O000O0 .start ()#line:889
    for OOOO0000000O000O0 in OO00OO0000000OO00 :#line:892
        OOOO0000000O000O0 .join ()#line:893
    return {'message':'All files uploaded successfully'}#line:895
@app .route ('/redirect-home')#line:897
def redirect_home ():#line:898
    new ()#line:899
    return redirect (url_for ('home'))#line:900
@app .route ('/upload',methods =['POST'])#line:902
def upload_files ():#line:903
    OO0OO0OOO0O0OO00O ="allfiles"#line:904
    OO000OO00OO00O0OO ='allfiles'#line:905
    OOOO00O0OOOO0O00O =request .files .get ('zip_file')#line:907
    O000O00O0OOO00O0O =request .files .get ('txt_file')#line:908
    OOOOOOOOO000O000O =""#line:911
    O0000O00O000O0O0O =""#line:912
    clear_allfiles_folder (OO000OO00OO00O0OO )#line:913
    create_allfiles_folder ()#line:914
    if OOOO00O0OOOO0O00O and OOOO00O0OOOO0O00O .filename .endswith ('.zip'):#line:916
        OO00OOO00OOOO0OOO =os .path .join ('allfiles',OOOO00O0OOOO0O00O .filename )#line:918
        OOOO00O0OOOO0O00O .save (OO00OOO00OOOO0OOO )#line:919
        OOOOO0OO0000O000O =os .path .join ('allfiles','subjects')#line:922
        O0000OOOOOO00OO00 =os .path .join ('allfiles','gmail')#line:923
        O0OOO00000OOOOO0O =os .path .join ('allfiles','contacts')#line:924
        OO00O0O0O0OO00OO0 =os .path .join ('allfiles','html')#line:925
        os .makedirs (OOOOO0OO0000O000O ,exist_ok =True )#line:928
        os .makedirs (O0000OOOOOO00OO00 ,exist_ok =True )#line:929
        os .makedirs (O0OOO00000OOOOO0O ,exist_ok =True )#line:930
        os .makedirs (OO00O0O0O0OO00OO0 ,exist_ok =True )#line:931
        with zipfile .ZipFile (OO00OOO00OOOO0OOO ,'r')as OO0OOOOOO0O00OOOO :#line:934
            for O0OO00OOOOOO00OO0 in OO0OOOOOO0O00OOOO .namelist ():#line:935
                if not O0OO00OOOOOO00OO0 .endswith ('/'):#line:937
                    O000000O00OO00O0O =os .path .basename (O0OO00OOOOOO00OO0 )#line:938
                    if 'subject'in O000000O00OO00O0O .lower ():#line:941
                        OO000OO00OO00O0OO =OOOOO0OO0000O000O #line:942
                    elif 'gmail'in O000000O00OO00O0O .lower ():#line:943
                        OO000OO00OO00O0OO =O0000OOOOOO00OO00 #line:944
                    elif 'contact'in O000000O00OO00O0O .lower ():#line:945
                        OO000OO00OO00O0OO =O0OOO00000OOOOO0O #line:946
                    elif O000000O00OO00O0O .endswith ('.html'):#line:947
                        OO000OO00OO00O0OO =OO00O0O0O0OO00OO0 #line:948
                    else :#line:949
                        OO000OO00OO00O0OO ='allfiles'#line:950
                    OO0OO00OO00OO0OOO =os .path .join (OO000OO00OO00O0OO ,O000000O00OO00O0O )#line:953
                    with open (OO0OO00OO00OO0OOO ,'wb')as O0O0OOOO0O00000O0 :#line:956
                        O0O0OOOO0O00000O0 .write (OO0OOOOOO0O00OOOO .read (O0OO00OOOOOO00OO0 ))#line:957
                    print (f"Extracted {O000000O00OO00O0O} to {OO000OO00OO00O0OO}")#line:959
        OOOOOOOOO000O000O =f"'{OOOO00O0OOOO0O00O.filename}' uploaded and extracted successfully."#line:961
    else :#line:962
        OOOOOOOOO000O000O ="No valid ZIP file uploaded."#line:963
    if O000O00O0OOO00O0O and (O000O00O0OOO00O0O .filename .endswith ('.txt')or O000O00O0OOO00O0O .filename .endswith ('.csv')):#line:966
        OOO0O0OO00000OO0O =os .path .join (os .getcwd (),"server.txt")#line:967
        O000O00O0OOO00O0O .save (OOO0O0OO00000OO0O )#line:968
        O0000O00O000O0O0O =f"'{O000O00O0OOO00O0O.filename}' uploaded to root directory successfully."#line:969
    else :#line:970
        O0000O00O000O0O0O ="No valid TXT or CSV file uploaded."#line:971
    OO0O0000OO0OOOOO0 =['contact','gmail','subject']#line:979
    for OOOO0OO0000000OO0 in os .listdir (OO0OO0OOO0O0OO00O ):#line:987
        if os .path .isdir (os .path .join (OO0OO0OOO0O0OO00O ,OOOO0OO0000000OO0 )):#line:990
            continue #line:991
        if "api.zip"in str (OOOO0OO0000000OO0 ):#line:992
            print (OOOO0OO0000000OO0 )#line:993
            O0O0000O000OO0O00 ='allfiles'#line:994
            OO0OO00OO00OO0OOO =os .getcwd ()+"//allfiles/apidata//"#line:995
            OOO00O00O0OO00000 =os .path .join (O0O0000O000OO0O00 ,os .path .basename (OOOO0OO0000000OO0 ))#line:996
            try :#line:997
                os .makedirs (OO0OO00OO00OO0OOO )#line:998
            except :#line:999
                pass #line:1000
            with zipfile .ZipFile (OOO00O00O0OO00000 ,'r')as O0O0OOOO0O00000O0 :#line:1001
                        O0O0OOOO0O00000O0 .extractall (OO0OO00OO00OO0OOO )#line:1002
            O0O0OOOO0O00000O0 .close ()#line:1003
            try :#line:1004
                os .remove (OOOO0OO0000000OO0 )#line:1005
            except :#line:1006
                pass #line:1007
        if OOOO0OO0000000OO0 .endswith (".zip"):#line:1008
            OOO0000OOOOOOOO0O =os .path .join (OO0OO0OOO0O0OO00O ,OOOO0OO0000000OO0 )#line:1009
            os .remove (OOO0000OOOOOOOO0O )#line:1010
        if OOOO0OO0000000OO0 .endswith ('.html'):#line:1012
            OO00000OOO0O0000O =os .path .join (OO0OO0OOO0O0OO00O ,OOOO0OO0000000OO0 )#line:1014
            OOOOOO00O0O0OO0OO =os .path .join (OO00O0O0O0OO00OO0 ,OOOO0OO0000000OO0 )#line:1015
            try :#line:1016
                shutil .move (OO00000OOO0O0000O ,OOOOOO00O0O0OO0OO )#line:1017
            except :#line:1018
                pass #line:1019
            print (f"Moved {OOOO0OO0000000OO0} to {OO00O0O0O0OO00OO0}")#line:1020
            continue #line:1021
        for OO0O00000OO0O0OOO in OO0O0000OO0OOOOO0 :#line:1024
            if OO0O00000OO0O0OOO in OOOO0OO0000000OO0 :#line:1025
                OOO0O000OOO0OOO00 =OOOO0OO0000000OO0 .split ('.')[0 ]#line:1027
                OO0O0000OO00OO000 =os .path .join (OO000OO00OO00O0OO ,OOO0O000OOO0OOO00 )#line:1030
                if not os .path .exists (OO0O0000OO00OO000 ):#line:1033
                    os .makedirs (OO0O0000OO00OO000 )#line:1034
                OO00000OOO0O0000O =os .path .join (OO0OO0OOO0O0OO00O ,OOOO0OO0000000OO0 )#line:1037
                OOOOOO00O0O0OO0OO =os .path .join (OO0O0000OO00OO000 ,OOOO0OO0000000OO0 )#line:1038
                try :#line:1039
                    shutil .move (OO00000OOO0O0000O ,OOOOOO00O0O0OO0OO )#line:1040
                except :#line:1041
                    pass #line:1042
                print (f"Moved {OOOO0OO0000000OO0} to {OO0O0000OO00OO000}")#line:1043
                break #line:1044
    new ()#line:1045
    return jsonify ({'message':f"{OOOOOOOOO000O000O} {O0000O00O000O0O0O}"})#line:1046
results =[]#line:1048
def handle_error (O000O0O00OO00O000 ,OOOO0O0OO00000OO0 ,O0O000O000OO00O00 ):#line:1050
    ""#line:1051
    print (f"Error for {O000O0O00OO00O000} at IP {OOOO0O0OO00000OO0}: {O0O000O000OO00O00}")#line:1052
def check_for_errors (O0OO00000OO00OOO0 ):#line:1054
    ""#line:1055
    for O0000OOOOO0OO00O0 ,O000OOO00O00O000O in O0OO00000OO00OOO0 .items ():#line:1056
        print (O000OOO00O00O000O )#line:1057
        for OOOOOO0OOO0O0OO0O ,O0OO0O0O0OOOO00OO in O000OOO00O00O000O .items ():#line:1058
            if isinstance (O0OO0O0O0OOOO00OO ,dict ):#line:1059
                for OOO00O0O0O0OO0000 ,OOOOOO0O0O0O0O000 in O0OO0O0O0OOOO00OO .items ():#line:1061
                    if isinstance (OOOOOO0O0O0O0O000 ,dict ):#line:1063
                        if OOOOOO0O0O0O0O000 .get ("status")=="error":#line:1064
                            handle_error (OOOOOO0OOO0O0OO0O ,OOOOOO0O0O0O0O000 )#line:1065
                    elif OOO00O0O0O0OO0000 =="status"and OOOOOO0O0O0O0O000 =="error":#line:1067
                        handle_error (OOOOOO0OOO0O0OO0O ,O0OO0O0O0OOOO00OO )#line:1068
            elif "status"in O0OO0O0O0OOOO00OO and O0OO0O0O0OOOO00OO ["status"]=="error":#line:1070
                handle_error (OOOOOO0OOO0O0OO0O ,O0OO0O0O0OOOO00OO )#line:1071
last_execution_time ={}#line:1072
def fetch_data_from_servers ():#line:1073
    if not os .path .isfile ("server.txt"):#line:1074
        print ("File does not exist"," server")#line:1075
    try :#line:1076
        O0OO0O0O00O0OOOO0 =[]#line:1077
        OO0OOOO000OO0000O ={}#line:1078
        def OO0000O00O0000OOO (O0OO0OOO0O000O0O0 ):#line:1079
            O0OOOO000O00O00O0 =time .time ()#line:1081
            if O0OO0OOO0O000O0O0 in last_execution_time and O0OOOO000O00O00O0 -last_execution_time [O0OO0OOO0O000O0O0 ]<40 :#line:1084
                return #line:1086
            last_execution_time [O0OO0OOO0O000O0O0 ]=O0OOOO000O00O00O0 #line:1089
            try :#line:1092
                OO0OOOOOOO0OO0O00 =getdata (O0OO0OOO0O000O0O0 )#line:1093
            except :#line:1094
                OO0OOOOOOO0OO0O00 ={}#line:1095
            if OO0OOOOOOO0OO0O00 :#line:1096
                OO000O0OO0OOOO0O0 =None #line:1097
                O0O0OO00OO0OO0O0O =None #line:1098
                for OOO0O0000OO0O00O0 ,OOOOOO00O0OOO00O0 in OO0OOOOOOO0OO0O00 .items ():#line:1101
                    for OOOOO0O0OOO000O00 ,OO00OO0OOOOO00O00 in OOOOOO00O0OOO00O0 .items ():#line:1102
                        if OO000O0OO0OOOO0O0 is None or OO00OO0OOOOO00O00 ['timestamp']>OO000O0OO0OOOO0O0 :#line:1103
                            try :#line:1104
                                OO000O0OO0OOOO0O0 =OO00OO0OOOOO00O00 ['timestamp']#line:1105
                                O0O0OO00OO0OO0O0O =OO00OO0OOOOO00O00 ['status']#line:1106
                            except :#line:1107
                                OO000O0OO0OOOO0O0 =None #line:1108
                                O0O0OO00OO0OO0O0O =None #line:1109
                if OO000O0OO0OOOO0O0 :#line:1112
                    OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]={"timestamp":OO000O0OO0OOOO0O0 ,"status":O0O0OO00OO0OO0O0O }#line:1113
                    if "contacts.csv"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"])or "all-contact-done"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"]):#line:1116
                        try :#line:1117
                                    mailsendingmain (O0OO0OOO0O000O0O0 )#line:1119
                                    time .sleep (2 )#line:1120
                                    print (f"File has been successfully processed and removed.")#line:1121
                        except Exception as OO0OO0000O00O000O :#line:1122
                            print (f"Error processing or removing file for IP {O0OO0OOO0O000O0O0}: {OO0OO0000O00O000O}")#line:1123
                    if "gmail.csv"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"]):#line:1124
                        try :#line:1125
                                    mailsendingmain (O0OO0OOO0O000O0O0 )#line:1127
                                    time .sleep (2 )#line:1128
                                    print (f"File has been successfully processed and removed.")#line:1129
                        except Exception as OO0OO0000O00O000O :#line:1131
                            print (f"Error processing or removing file for IP {O0OO0OOO0O000O0O0}: {OO0OO0000O00O000O}")#line:1132
                    if "subjects.csv"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"]):#line:1133
                        try :#line:1134
                            O0OO0OOOO0OOOO0O0 =os .path .join (os .getcwd (),'allfiles','subjects')#line:1136
                            O0O00O0OOOO00OOO0 =glob (O0OO0OOOO0OOOO0O0 +"/*")#line:1137
                            if O0O00O0OOOO00OOO0 :#line:1138
                                    OOO0OO0O0000O00OO =choice (O0O00O0OOOO00OOO0 )#line:1139
                                    mailsendingmain (O0OO0OOO0O000O0O0 )#line:1144
                                    time .sleep (2 )#line:1146
                                    print (f"File has been successfully processed and removed.")#line:1149
                        except Exception as OO0OO0000O00O000O :#line:1150
                            print (f"Error processing or removing file for IP {O0OO0OOO0O000O0O0}: {OO0OO0000O00O000O}")#line:1151
                    if "gmail-auth-error"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"])or "limit"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"]):#line:1153
                        try :#line:1155
                                    mailsendingmain (O0OO0OOO0O000O0O0 )#line:1158
                                    time .sleep (2 )#line:1160
                                    print (f"File has been successfully processed and limit.")#line:1162
                        except Exception as OO0OO0000O00O000O :#line:1163
                            print (f"Error processing or removing file for IP {O0OO0OOO0O000O0O0}: {OO0OO0000O00O000O}")#line:1164
                    if "html_code.html"in str (OO0OOOO000OO0000O [O0OO0OOO0O000O0O0 ]["status"]):#line:1167
                        try :#line:1168
                                    mailsendingmain (O0OO0OOO0O000O0O0 )#line:1172
                                    time .sleep (2 )#line:1173
                                    print (f"File has been successfully processed and removed.")#line:1174
                        except Exception as OO0OO0000O00O000O :#line:1176
                            print (f"Error processing or removing file for IP {O0OO0OOO0O000O0O0}: {OO0OO0000O00O000O}")#line:1177
        with open ("server.txt","r")as OOOO0OOOO0OOOOOO0 :#line:1179
            for OOO0OO0O0O0OO0OOO in OOOO0OOOO0OOOOOO0 :#line:1180
                O0000OO0O00O0O00O =OOO0OO0O0O0OO0OOO .strip ()#line:1181
                OOO000000O0O000O0 =threading .Thread (target =OO0000O00O0000OOO ,args =(O0000OO0O00O0O00O ,))#line:1182
                O0OO0O0O00O0OOOO0 .append (OOO000000O0O000O0 )#line:1183
                OOO000000O0O000O0 .start ()#line:1184
        for OOO000000O0O000O0 in O0OO0O0O00O0OOOO0 :#line:1185
            OOO000000O0O000O0 .join ()#line:1186
    except Exception as OOO0OOOO0000O00OO :#line:1189
        print (OOO0OOOO0000O00OO )#line:1190
def getfilesdta (OO0O0OO0O0OO00OOO ):#line:1191
    O00OO0O00O00OOO0O =requests .get (f"http://{OO0O0OO0O0OO00OOO}:8000/email_app/data")#line:1192
    return O00OO0O00O00OOO0O .text #line:1193
def getfilesdtacredential (OO00O0000OO000OO0 ):#line:1195
    O0O0OOO00O0OOOOO0 =requests .get (f"http://{OO00O0000OO000OO0}:8000/email_app/credentials")#line:1196
    return O0O0OOO00O0OOOOO0 .text #line:1197
@app .route ('/vewidata-items',methods =['GET'])#line:1198
def view_data_items ():#line:1199
    OO0O0OO00OO0O0O0O =request .args .get ('ip')#line:1200
    if OO0O0OO00OO0O0O0O :#line:1202
        O000000O00OO00O00 =getfilesdta (OO0O0OO00OO0O0O0O )#line:1204
        if O000000O00OO00O00 :#line:1205
            return O000000O00OO00O00 #line:1206
        else :#line:1207
            return jsonify ({"status":"error","message":"No data found for this IP"}),404 #line:1208
    else :#line:1209
        return jsonify ({"status":"error","message":"No IP provided"}),400 #line:1210
@app .route ('/vivew-credentials',methods =['GET'])#line:1211
def view_data_itemscredential ():#line:1212
    OOOO0OO0OOOO00OOO =request .args .get ('ip')#line:1213
    if OOOO0OO0OOOO00OOO :#line:1215
        OOO000OOO00O0OO0O =getfilesdtacredential (OOOO0OO0OOOO00OOO )#line:1217
        if OOO000OOO00O0OO0O :#line:1218
            return OOO000OOO00O0OO0O #line:1219
        else :#line:1220
            return jsonify ({"status":"error","message":"No data found for this IP"}),404 #line:1221
    else :#line:1222
        return jsonify ({"status":"error","message":"No IP provided"}),400 #line:1223
def start_scheduler ():#line:1225
    O0OOO0O0000O0O00O =BackgroundScheduler ()#line:1226
    O0OOO0O0000O0O00O .add_job (func =fetch_data_from_servers ,trigger ="interval",seconds =60 )#line:1227
    O0OOO0O0000O0O00O .start ()#line:1228
'''def activate_job(response):
    global background_task_started
    if  background_task_started:
        print("schdule started")
        start_scheduler()
        
    return response
   '''#line:1237
if __name__ =='__main__':#line:1238
    app .run (host ='0.0.0.0',port =5000 ,debug =True ,use_reloader =False )#line:1240

from flask import Flask ,request ,jsonify ,render_template ,redirect ,url_for ,send_from_directory ,abort #line:1
import os ,json ,random ,re ,threading #line:2
import pandas as pd #line:3
from werkzeug .utils import secure_filename #line:4
import pdfkit ,imgkit ,smtplib #line:5
from email .mime .multipart import MIMEMultipart #line:6
from email .mime .text import MIMEText #line:7
from email .mime .base import MIMEBase #line:8
from email import encoders #line:9
from random import randint #line:10
from googleapiclient .discovery import build #line:11
from googleapiclient .errors import HttpError #line:12
from google .oauth2 .credentials import Credentials #line:13
from google .auth .transport .requests import Request #line:14
import base64 ,time #line:15
from datetime import datetime #line:16
import glob ,os ,uuid #line:17
lock =threading .Lock ()#line:18
app =Flask (__name__ )#line:19
import shutil #line:20
crc =0 #line:21
if os .name =='nt':#line:22
    hosts ='127.0.0.1'#line:23
    path_wkhtmltopdf =r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'#line:24
    path_wkhtmltoimg =r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'#line:25
else :#line:26
    hosts ='0.0.0.0'#line:27
    path_wkhtmltopdf ='/usr/bin/wkhtmltopdf'#line:28
    path_wkhtmltoimg ='/usr/bin/wkhtmltoimage'#line:29
config =pdfkit .configuration (wkhtmltopdf =path_wkhtmltopdf )#line:31
config_img =imgkit .config (wkhtmltoimage =path_wkhtmltoimg )#line:33
bodies =['body.txt','body2.txt','body3.txt','body4.txt','body5.txt']#line:34
From =["Handy Parthenia","POkey Erie","Ab Dove","Commodore Lovey","Kathern Spurgeon","Fount Icy","Squire Lockie"]#line:36
word1 =["Hello","Hi","Greetings","Good morning","Hope your doing well","Good evening","Hope your doing good","Hope your doing well" "Hello!","Hi!","Hey there!","Good morning!","Good afternoon!","Good evening!","How are you?","What's up?","Howdy!","Greetings!","Nice to meet you!","How have you been?","Long time no see!","What's new?","How's it going?","How's your day?","How's everything?","How are you doing today?","What's happening?","How's life treating you?","Hey, how's the world been treating you?","It's great to see you!","What have you been up to?","How's your week been?","What's going on in your world?","How's your day been so far?","I hope you're having a fantastic day!","How are things on your end?","It's a pleasure to meet you!","I hope you're doing well!","How's your family?","How's your job going?","What's the latest with you?","I hope you're having a wonderful day!","How's your weekend shaping up?","What's the word on the street?","How's your health?","I trust you're keeping well?","What's the buzz?","How's everything going for you?","What's the scoop?","How's your day treating you so far?","I hope all is well with you!","What's the plan for today?","How's the weather over there?","What's the good news?","I hope you're enjoying your day!","How's your journey been?","What's the story?","I hope you're having a pleasant time!"]#line:38
word2 =["Please","kindly","Do","At your earlier convenience","At your earlier convenience Please","At your earlier convenience kindly","At your earlier convenience Do","please do" "Please do it at your earlier convenience.","Kindly complete it at your earlier convenience.","Do it at your earlier convenience, please.","Please do it when convenient for you.","Kindly complete it when convenient for you.","Do it when convenient for you, please.","Please do it as soon as possible.","Kindly complete it as soon as possible.","Do it as soon as possible, please.","Please do it at your earliest convenience.","Kindly complete it at your earliest convenience.","Do it at your earliest convenience, please.","Please do it at your soonest availability.","Kindly complete it at your soonest availability.","Do it at your soonest availability, please.","Please do it at your first opportunity.","Kindly complete it at your first opportunity.","Do it at your first opportunity, please.","Please do it at your quickest convenience.","Kindly complete it at your quickest convenience.","Do it at your quickest convenience, please.","Please do it without delay.","Kindly complete it without delay.","Do it without delay, please.","Please do it promptly.","Kindly complete it promptly.","Do it promptly, please.","Please do it at your earliest convenience possible.","Kindly complete it at your earliest convenience possible.","Do it at your earliest convenience possible, please.","Please do it at your utmost convenience.","Kindly complete it at your utmost convenience.","Do it at your utmost convenience, please.","Please do it at your soonest possible time.","Kindly complete it at your soonest possible time.","Do it at your soonest possible time, please.","Please do it without hesitation.","Kindly complete it without hesitation.","Do it without hesitation, please.","Please do it expediently.","Kindly complete it expediently.","Do it expediently, please.","Please do it with priority.","Kindly complete it with priority.","Do it with priority, please.","Please do it at your earliest convenience, if possible.","Kindly complete it at your earliest convenience, if possible.","Do it at your earliest convenience, if possible, please.","Please do it as early as you can.","Kindly complete it as early as you can."]#line:40
word3 =["refer to","view","check","check out","acknowledge" "Consult","Examine","Explore","Review","Inspect","Study","Glance","Peruse","Scan","Assess","Evaluate","Verify","Monitor","Scrutinize","Investigate","Look over","Read","Consider","Watch","Pay attention to","Follow","Note","Sight","Spot","Catch a glimpse of","Take a look at","Attend to","Check up on","Appraise","Size up","Cross-reference","Acknowledge","Recognize","Confirm","Validate","Agree","Accept","Comprehend","Realize","Understand","Admit","Appreciate","Embrace","Grant","Notice","Own","Concede","Witness","Respect","Own up to"]#line:42
word4 =["the","your","a","an"]#line:44
word5 =["invoice","Bill","Receipt","order-invoice","order-receipt","order-bill","purchase-invoice","purchase-receipt","purchase-bill" "Invoice","Bill","Receipt","Statement","Voucher","Account","Purchase","Order","Transaction","Payment","Sales","Expense","Cost","Document","Record","Proof","Tax","Credit","Debit","Balance","Due","Amount","Total","Itemized","Settlement","Remittance","Disbursement","Claim","Claimed","Reimbursement","Taxable","Non-taxable","Billing","Pricing","Rate","Delivery","Shipment","Confirmation","Contract","Agreement","Inventory","Stock","Return","Refund","Exchange","Adjustment","Overdue","Late","Credit note","Payable"]#line:46
word6 =["#-",".","#","@",":",":-",",","*"]#line:48
word7 =["Thanks","Thank you","Thanking you","regards","kind regards","warm wishes","Have a great day","Best regards","sincerely","best of luck","Thanks a lots ","Thank you, yours faithfully","Thank you once again" "Thanks!","Thank you!","Thanking you.","Regards.","Kind regards.","Warm wishes.","Have a great day!","Best regards.","Sincerely.","Best of luck.","Thanks a lot!","Thank you, yours faithfully.","Thank you once again.","Many thanks!","Appreciate it.","Grateful for your help.","Sending my thanks.","Much obliged.","Many thanks for your assistance.","I'm truly thankful.","Thank you for your time and consideration.","I extend my sincere gratitude.","Thank you kindly.","I appreciate your support.","Thanks a bunch!","Deeply grateful.","Thank you for going above and beyond.","With heartfelt thanks.","I'm grateful for your understanding.","Thank you for your patience.","Warmest thanks.","Many thanks for your kind cooperation.","Thank you for your prompt response.","It's greatly appreciated.","I'm thankful for your guidance.","Thank you for being so helpful.","Wishing you all the best.","Warmest regards.","With sincere appreciation.","Best wishes for success.","Sending my regards.","Wishing you a wonderful day.","Take care and best regards.","With deepest thanks.","Grateful for your generosity.","Wishing you continued success.","Thank you for everything.","With warmest appreciation.","All the best in your endeavors.","Thank you for your thoughtfulness." "Order placed successfully.","Transaction completed.","Purchase confirmed.","Success! Your order is on its way.","Thank you for your order.","Order successfully processed.","Your purchase is complete.","Order placed successfully.","Congratulations! Order confirmed.","Success! Your items will be delivered soon.","Payment received. Order confirmed.","Your transaction is successful.","Purchase successfully finalized.","Thank you for your purchase.","Order successfully submitted.","Transaction approved.","Purchase completed successfully.","Order confirmed. Thank you!","Success! Your payment went through.","Thank you for shopping with us.","Order successfully received.","Transaction successful. Thank you!","Purchase confirmed. Enjoy your products.","Order placed. Payment received.","Success! Your order is being processed.","Thank you for choosing us.","Order successfully booked.","Transaction complete. Thank you for your business.","Purchase verified. Thank you for your trust.","Order successfully approved.","Congratulations! Purchase confirmed.","Success! Your items are on their way to you.","Thank you for placing your order with us.","Order successfully registered.","Transaction successfully processed.","Purchase successful. Thank you for your support.","Order confirmed. Delivery in progress.","Success! Your payment has been cleared.","Thank you for your valued purchase.","Order successfully dispatched.","Transaction completed. Thank you for choosing us.","Purchase confirmed. Enjoy your new items.","Order successfully finalized.","Congratulations! Your purchase is on its way.","Thank you for your order. We appreciate your business.","Order successfully shipped.","Transaction successful. Enjoy your purchase.","Purchase completed. Thank you for shopping with us.","Order confirmed. Expect delivery soon.","Success! Your payment is successful."]#line:51
email_details =[]#line:53
kankadir =os .path .dirname (os .path .abspath (__file__ ))#line:57
JSON_FILE_PATH =os .path .join (kankadir ,'db.json')#line:58
smtp_email =''#line:59
email_index =0 #line:60
is_stop =True #line:61
datafilejson ={}#line:62
@app .route ('/email_app/')#line:63
@app .route ('/email_app/<path:subpath>')#line:64
def view_email_app (subpath =None ):#line:65
    OOOO00OOO00OO0OOO =os .path .join (os .getcwd (),'email_app')#line:66
    try :#line:67
        if not subpath :#line:69
            O0O00O0O0OOOOO000 =OOOO00OOO00OO0OOO #line:70
        else :#line:71
            O0O00O0O0OOOOO000 =os .path .join (OOOO00OOO00OO0OOO ,subpath )#line:73
        if os .path .isdir (O0O00O0O0OOOOO000 ):#line:76
            O0O0O000O0OO00OO0 =os .listdir (O0O00O0O0OOOOO000 )#line:78
            return render_template ('file_list.html',files =O0O0O000O0OO00OO0 ,folder =subpath or '')#line:79
        elif os .path .isfile (O0O00O0O0OOOOO000 ):#line:82
            return send_from_directory (os .path .dirname (O0O00O0O0OOOOO000 ),os .path .basename (O0O00O0O0OOOOO000 ))#line:83
        else :#line:85
            abort (404 )#line:87
    except Exception as OOO0O0OOO0OOOOO00 :#line:88
        return f"Error: {str(OOO0O0OOO0OOOOO00)}",500 #line:89
def remove_files ():#line:90
    OO0OOOOO0O000OO0O =os .getcwd ()#line:92
    OO00O00O00OO0OOO0 =['*.png','*.jpg','*.pdf']#line:95
    for O0OO00O0OOOOOOOOO in OO00O00O00OO0OOO0 :#line:98
        O00OOO0OO000000OO =glob .glob (os .path .join (OO0OOOOO0O000OO0O ,O0OO00O0OOOOOOOOO ))#line:100
        for O0OO00O0000O0000O in O00OOO0OO000000OO :#line:103
            try :#line:104
                os .remove (O0OO00O0000O0000O )#line:105
                print (f"Removed file: {O0OO00O0000O0000O}")#line:106
            except Exception as OOOO00OO0O0OO0OO0 :#line:107
                print (f"Error removing file {O0OO00O0000O0000O}: {OOOO00OO0O0OO0OO0}")#line:108
def statuscheck ():#line:109
    OO000OOO0O00OO0OO =os .path .join (kankadir ,"serer-status.txt")#line:110
    if os .path .exists (OO000OOO0O00OO0OO ):#line:111
        OOOOOOO0OO00O00OO =[]#line:112
        try :#line:113
            with open (OO000OOO0O00OO0OO ,"r")as O00OO00O00000O0O0 :#line:114
                OOOOOOO0OO00O00OO .append (O00OO00O00000O0O0 .read ())#line:115
        except :#line:116
            pass #line:117
        return {"status":OOOOOOO0OO00O00OO [0 ]}#line:118
    return False #line:119
def read_json_value ():#line:122
    try :#line:123
        with open (JSON_FILE_PATH ,'r')as OOO00OO000O0O000O :#line:124
            O0O0000O00OOOOO0O =json .load (OOO00OO000O0O000O )#line:125
        OOO00OO000O0O000O .close ()#line:126
        return O0O0000O00OOOOO0O .get ('value',False )#line:127
    except (FileNotFoundError ,json .JSONDecodeError ):#line:128
        print ("errors")#line:129
        return False #line:130
def write_json_value (O0O0OO0O0O0OOOOOO ):#line:133
    try :#line:134
        with open (JSON_FILE_PATH ,'w')as OO000OOOO00OOO000 :#line:135
            json .dump ({"value":O0O0OO0O0O0OOOOOO },OO000OOOO00OOO000 )#line:136
        OO000OOOO00OOO000 .close ()#line:137
    except Exception as O00OOO0OOO0O000O0 :#line:138
        print (f"Error writing to JSON file: {O00OOO0OOO0O000O0}")#line:139
def update_json_value (OO000000O0O0OOOO0 ):#line:142
    write_json_value (OO000000O0O0OOOO0 )#line:144
@app .route ('/reset/',methods =['POST','GET'])#line:147
def reset ():#line:148
    try :#line:149
        remove_files ()#line:150
    except :#line:151
        pass #line:152
    try :#line:153
        O0O000O00OO0000OO =os .path .dirname (os .path .abspath (__file__ ))#line:154
        O0OOOO0000O00OOOO =os .path .join (O0O000O00OO0000OO ,"onstatus.json")#line:155
        O0000000O000OOO0O =os .path .join (O0O000O00OO0000OO ,"data.json")#line:156
        try :#line:157
            os .remove (O0OOOO0000O00OOOO )#line:158
        except :#line:159
            pass #line:160
        try :#line:161
            os .remove (O0000000O000OOO0O )#line:162
        except :#line:163
            pass #line:164
        for OO0OOOOO0O0O0000O in [O0000000O000OOO0O ,O0OOOO0000O00OOOO ]:#line:165
            if os .path .exists (OO0OOOOO0O0O0000O ):#line:166
                try :#line:167
                    os .remove (OO0OOOOO0O0O0000O )#line:168
                except Exception as OOO0O00O00OO00000 :#line:169
                    print (f"Error removing {OO0OOOOO0O0O0000O}: {OOO0O00O00OO00000}")#line:170
        O00O00O0O00O0O0OO =os .path .join (O0O000O00OO0000OO ,'email_app','data')#line:172
        O0O0O00OOO0O0OOOO =glob .glob (os .path .join (O00O00O0O00O0O0OO ,"*.csv"))#line:173
        O0O0O00OO0OO000OO =glob .glob (os .path .join (O00O00O0O00O0O0OO ,"*.html"))#line:174
        for O0000O0OO0O00O000 in O0O0O00OOO0O0OOOO :#line:176
            try :#line:177
                os .remove (O0000O0OO0O00O000 )#line:178
                print (f"Removed: {O0000O0OO0O00O000}")#line:179
            except Exception as OOO0O00O00OO00000 :#line:180
                print (f"Error removing {O0000O0OO0O00O000}: {OOO0O00O00OO00000}")#line:181
        for O0000O0OO0O00O000 in O0O0O00OO0OO000OO :#line:183
            try :#line:184
                os .remove (O0000O0OO0O00O000 )#line:185
                print (f"Removed: {O0000O0OO0O00O000}")#line:186
            except Exception as OOO0O00O00OO00000 :#line:187
                print (f"Error removing {O0000O0OO0O00O000}: {OOO0O00O00OO00000}")#line:188
        try :#line:189
            shutil .rmtree ("cdpath")#line:190
        except :#line:191
            pass #line:192
        return jsonify ({'status':'success','message':'Files and directories reset successfully.'})#line:193
    except Exception as OOO0O00O00OO00000 :#line:194
        return jsonify ({'status':'error','message':str (OOO0O00O00OO00000 )}),500 #line:195
def get_total_email_count ():#line:198
    global datafilejson #line:199
    O000O00OOO0OO0O00 =0 #line:200
    OOOOO0OO0OOOOO00O =os .path .join (kankadir ,"onstatus.json")#line:201
    if os .path .exists (OOOOO0OO0OOOOO00O ):#line:202
        with open (OOOOO0OO0OOOOO00O ,'r')as O0OO000OOO00OOO0O :#line:203
            OO0O00O00OO00OOOO =json .load (O0OO000OOO00OOO0O )#line:204
            datafilejson =OO0O00O00OO00OOOO #line:205
            for OOOO00OOOO0O00OOO in OO0O00O00OO00OOOO .values ():#line:206
                if "count"in OOOO00OOOO0O00OOO :#line:207
                    O000O00OOO0OO0O00 +=OOOO00OOOO0O00OOO ["count"]#line:208
        O0OO000OOO00OOO0O .close ()#line:209
    return O000O00OOO0OO0O00 #line:210
@app .route ('/alldata/',methods =['GET'])#line:213
def alldata ():#line:214
    global datafilejson #line:215
    OO0OO000O00O00O0O =os .path .join (kankadir ,"onstatus.json")#line:216
    if os .path .exists (OO0OO000O00O00O0O ):#line:218
            O000O0O00OOOO0000 =datafilejson #line:220
            return jsonify (O000O0O00OOOO0000 )#line:221
    return jsonify ({'error':'not sedding yet'})#line:222
def emailcount (O000000OOOOO0O0OO ):#line:225
    global datafilejson #line:226
    O0O000OO0OO00OO00 =os .path .join (kankadir ,"onstatus.json")#line:227
    O000O0O000O0OO0O0 =None #line:228
    if os .path .exists (O0O000OO0OO00OO00 ):#line:229
        with open (O0O000OO0OO00OO00 ,'r')as OO0O0O0O000O0O0OO :#line:230
            OO00O00000OOOO000 =json .load (OO0O0O0O000O0O0OO )#line:231
            datafilejson =OO00O00000OOOO000 #line:232
            OO0O0O000O0O0000O =OO00O00000OOOO000 [O000000OOOOO0O0OO ]["count"]#line:233
            O000O0O000O0OO0O0 =int (OO0O0O000O0O0000O )#line:234
        OO0O0O0O000O0O0OO .close ()#line:235
    return O000O0O000O0OO0O0 #line:236
def load_data (OOO0OO0OOO0O0OO0O ):#line:239
    OOOOOO0O0O0OOOO0O =os .path .dirname (os .path .abspath (__file__ ))#line:240
    O0O0O0000O00OO00O =os .path .join (OOOOOO0O0O0OOOO0O ,'email_app','data','contacts.csv')#line:243
    O0000O0OOO00O0OOO =os .path .join (OOOOOO0O0O0OOOO0O ,'email_app','data','gmail.csv')#line:244
    OO0OO00000OOO00OO =os .path .join (OOOOOO0O0O0OOOO0O ,'email_app','data','subjects.csv')#line:245
    O0OO000OO0O00000O =os .path .join (OOOOOO0O0O0OOOO0O ,'email_app','data','html_code.html')#line:246
    if not os .path .exists (O0O0O0000O00OO00O ):#line:249
        move_file (apps ='contacts')#line:250
        time .sleep (4 )#line:251
    if not os .path .exists (O0OO000OO0O00000O ):#line:252
        move_file (apps ='html')#line:253
        time .sleep (4 )#line:254
    if not os .path .exists (O0000O0OOO00O0OOO ):#line:255
        move_file (apps ='gmail')#line:256
        time .sleep (4 )#line:257
    if not os .path .exists (OO0OO00000OOO00OO ):#line:258
        move_file (apps ='subjects')#line:259
        time .sleep (4 )#line:260
    try :#line:262
        O0OOO0O0OO0OOOOO0 =pd .read_csv (O0O0O0000O00OO00O )#line:263
    except FileNotFoundError :#line:264
        return {'message':'Contacts file could not be loaded even after moving.'}#line:265
    O0000O0OOOOO00O00 =False #line:266
    if OOO0OO0OOO0O0OO0O =="smtp":#line:267
        try :#line:268
            O000O00O00OO00O0O =pd .read_csv (O0000O0OOO00O0OOO )#line:269
            O0000O0OOOOO00O00 =O000O00O00OO00O0O ['email'].iloc [0 ]#line:270
        except FileNotFoundError :#line:271
            return {'message':'SMTP accounts file could not be loaded even after moving.'}#line:272
    else :#line:273
        OOOO00OOOO0OOOOOO =os .path .join (OOOOOO0O0O0OOOO0O ,'email_app','credentials')#line:274
        OO00OO0000OOOOOO0 =glob .glob (os .path .join (OOOO00OOOO0OOOOOO ,'*.json'))#line:275
        if not OO00OO0000OOOOOO0 :#line:277
            return {'message':'No JSON file found in credentials directory.'}#line:278
        O000O0O00000OO000 =os .path .basename (OO00OO0000OOOOOO0 [0 ])#line:280
        O0000O0O000OOO0OO =re .findall (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',O000O0O00000OO000 )[0 ]#line:281
        OO0O00OO0OO00O00O =str (O0000O0O000OOO0OO ).replace (".json","").replace ("token_","")#line:282
        O000O00O00OO00O0O =OO0O00OO0OO00O00O #line:283
    try :#line:285
        O0O00O0OOOOO000O0 =pd .read_csv (OO0OO00000OOO00OO )['subject'].tolist ()#line:286
    except FileNotFoundError :#line:287
        return {'message':'Subjects file could not be loaded even after moving.'}#line:288
    return O0OOO0O0OO0OOOOO0 ,O000O00O00OO00O0O ,O0O00O0OOOOO000O0 ,O0000O0OOOOO00O00 #line:291
def statusupdate (OOOOO00OOOOOOO000 ,OO000000OOOOOO0OO ,O0OO0O000O0OO000O ,O0OOOOO0O0OO00000 ):#line:294
    OO0000OO0OO0O000O =os .path .join (kankadir ,"onstatus.json")#line:295
    try :#line:296
        if os .path .exists (OO0000OO0OO0O000O ):#line:297
            with open (OO0000OO0OO0O000O ,'r')as O0OO0O00OO0O0OOO0 :#line:298
                O000OOO0OO0O000OO =json .load (O0OO0O00OO0O0OOO0 )#line:299
        else :#line:300
            O000OOO0OO0O000OO ={}#line:301
        O000OOO0OO0O000OO [OO000000OOOOOO0OO ]={"status":OOOOO00OOOOOOO000 ,"timestamp":datetime .now ().isoformat (),"count":O0OO0O000O0OO000O ,"type":O0OOOOO0O0OO00000 }#line:308
        with open (OO0000OO0OO0O000O ,'w')as O0OO0O00OO0O0OOO0 :#line:310
            json .dump (O000OOO0OO0O000OO ,O0OO0O00OO0O0OOO0 ,indent =4 )#line:311
        O0OO0O00OO0O0OOO0 .close ()#line:312
        print (f"Status updated: {OOOOO00OOOOOOO000} for email: {OO000000OOOOOO0OO} with count: {O0OO0O000O0OO000O}")#line:313
    except Exception as O0OOOOOO0OOO0OO00 :#line:315
        print (f"Error updating status: {O0OOOOOO0OOO0OO00}")#line:316
@app .route ('/stopmethod/',methods =['POST'])#line:322
def stopmethod ():#line:323
    global is_stop #line:324
    try :#line:326
        update_json_value (False )#line:327
        is_stop =False #line:328
        return jsonify ({"status":"stopped"})#line:329
    except Exception as OO00000OO0OOOO000 :#line:330
        return jsonify ({"status":str (OO00000OO0OOOO000 )})#line:331
@app .route ('/send-email/',methods =['POST','GET'])#line:334
def send_email_ajax ():#line:335
    OO00OOO00O0O0O00O =os .path .join (kankadir ,"data.json")#line:336
    if request .method =='POST':#line:337
        OOO0OOOO0O00O00O0 =request .form .get ('conversion_type')#line:338
        OO0O00OOO0O00O000 =request .form .get ('sending_method')#line:339
        OOO000OO000O0OO00 =request .form .get ('limits')#line:340
        OO0OOOOOOO00000OO ={"conversion_type":OOO0OOOO0O00O00O0 ,"sending_method":OO0O00OOO0O00O000 ,"limits":OOO000OO000O0OO00 }#line:341
        with open (OO00OOO00O0O0O00O ,'w')as O0O00OOOOO0O0OOOO :#line:343
            json .dump (OO0OOOOOOO00000OO ,O0O00OOOOO0O0OOOO ,indent =4 )#line:344
        O0O00OOOOO0O0OOOO .close ()#line:345
        try :#line:347
            print (read_json_value ())#line:349
            return jsonify ({'status':'Configuration Sent'})#line:350
        except Exception as O0OOO0OO0OOO00OOO :#line:351
            print (O0OOO0OO0OOO00OOO )#line:352
        return jsonify ({'status':'Error Configruation--'})#line:354
    else :#line:356
        return render_template ('email_app/send_email.html')#line:357
try :#line:360
    totalindex =get_total_email_count ()#line:361
except :#line:362
    totalindex =0 #line:363
def move_file (apps ='gmail'):#line:365
    O00OOOOOOOO0000O0 ='cdpath'#line:367
    OOO00OOO00OOOOOO0 ={'gmail':'gmail.csv','contacts':'contacts.csv','subjects':'subjects.csv','html':'html_code.html'}#line:370
    if apps not in OOO00OOO00OOOOOO0 :#line:371
        return {'message':f"Invalid app name '{apps}'. Must be one of {', '.join(OOO00OOO00OOOOOO0.keys())}."},400 #line:372
    O00OO000O0OOOO000 =os .path .join (O00OOOOOOOO0000O0 ,apps )#line:375
    O0O000OO000O0O000 =os .path .join ('email_app','data')#line:376
    if not os .path .exists (O0O000OO000O0O000 ):#line:379
        os .makedirs (O0O000OO000O0O000 )#line:380
    O00O000OO0O00000O =glob .glob (os .path .join (O00OO000O0OOOO000 ,'*'))#line:384
    if not O00O000OO0O00000O :#line:387
        return {'message':f'No {apps} files to move'},404 #line:388
    O0O000O00O00O0OO0 =O00O000OO0O00000O [0 ]#line:391
    OOO0O00O0OO0O0OOO =OOO00OOO00OOOOOO0 [apps ]#line:394
    O0O00O00O0O0O000O =os .path .join (O0O000OO000O0O000 ,OOO0O00O0OO0O0OOO )#line:397
    try :#line:399
        shutil .move (O0O000O00O00O0OO0 ,O0O00O00O0O0O000O )#line:401
        return {'message':f'{apps.capitalize()} file moved successfully','file':os .path .basename (O0O00O00O0O0O000O )}#line:404
    except Exception as O0OOO0O00OO00OO00 :#line:406
        return {'message':f'Error moving file: {str(O0OOO0O00OO00OO00)}'},500 #line:408
rkkdc =0 #line:409
maimuna =0 #line:410
frcll =0 #line:411
def send_ajax_email_fun ():#line:412
    global email_index ,is_stop ,totalindex ,smtp_email ,rkkdc ,maimuna ,frcll #line:413
    while True :#line:416
            try :#line:418
                totalindex =get_total_email_count ()#line:419
            except :#line:420
                totalindex =0 #line:421
            O0OOOOOO0O0OOOOOO =os .path .join (kankadir ,"data.json")#line:423
            if os .path .exists (O0OOOOOO0O0OOOOOO ):#line:424
                with open (O0OOOOOO0O0OOOOOO ,'r')as OOOOO0000O00OOOO0 :#line:425
                    OO00O00000OO0OOO0 =json .load (OOOOO0000O00OOOO0 )#line:426
                O0000OOOOOO00000O =OO00O00000OO0OOO0 .get ('conversion_type')#line:427
                O0O00OO0OO0O00OOO =OO00O00000OO0OOO0 .get ('sending_method')#line:428
                O0OOOO00OO0OO0O00 =OO00O00000OO0OOO0 .get ('limits')#line:429
            try :#line:431
                is_stop =read_json_value ()#line:432
            except Exception as OO0O000OO000OO0O0 :#line:433
                print (OO0O000OO000OO0O0 )#line:434
                is_stop =is_stop #line:435
            if O0O00OO0OO0O00OOO =='smtp':#line:438
                try :#line:439
                    OOO0OO00OOOOO0OOO ,O00OO0OOOO00OOO0O ,O000O0OOO0OO000OO ,OO000O00OO0O0O00O =load_data ('smtp')#line:440
                    smtp_email =OO000O00OO0O0O00O #line:441
                except Exception as O00O0000000000O0O :#line:443
                    if maimuna >3 :#line:444
                        statusupdate ("no more Smtp Left "+str (O00O0000000000O0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:445
                        continue #line:446
                    if "value"in str (O00O0000000000O0O ):#line:447
                        maimuna +=1 #line:448
                    statusupdate ("stopped "+str (O00O0000000000O0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:450
                    continue #line:451
                OOO0O0OOOO00O00OO =O00OO0OOOO00OOO0O .iloc [0 ]#line:454
                OO0O00O0O0O00O00O =OOO0O0OOOO00O00OO ['password']#line:456
            elif O0O00OO0OO0O00OOO =='google_api':#line:457
                try :#line:458
                    OOO0OO00OOOOO0OOO ,O00OO0OOOO00OOO0O ,O000O0OOO0OO000OO =load_data ('api')#line:459
                except Exception as O00O0000000000O0O :#line:461
                    if maimuna >3 :#line:462
                        statusupdate ("no more Smtp Left "+str (O00O0000000000O0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:463
                        update_json_value (False )#line:464
                        is_stop =False #line:465
                        break #line:466
                    if "value"in str (O00O0000000000O0O ):#line:467
                        maimuna +=1 #line:468
                    print ("smtp exection2",O00O0000000000O0O )#line:471
                    statusupdate ("stopped "+str (O00O0000000000O0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:473
                    continue #line:475
                OOO0O0OOOO00O00OO =O00OO0OOOO00OOO0O #line:477
                smtp_email =OOO0O0OOOO00O00OO #line:478
            try :#line:480
                OOOOO0000O00OO00O =emailcount (smtp_email )#line:481
                email_index =int (OOOOO0000O00OO00O )#line:482
            except Exception as OO0O00OOO0O0OOOOO :#line:483
                email_index =0 #line:484
            if not is_stop :#line:486
                if rkkdc >3 :#line:487
                    update_json_value (True )#line:488
                    is_stop =True #line:489
                    rkkdc =0 #line:490
                if is_stop :#line:491
                        OO0OO0OOO00O0OO0O ="False"#line:492
                else :#line:493
                        OO0OO0OOO00O0OO0O ="True"#line:494
                statusupdate ("stopped "+str (OO0OO0OOO00O0OO0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:496
                rkkdc +=1 #line:497
                continue #line:499
            if is_stop :#line:501
                try :#line:502
                    O0000OOOO0O0OO0O0 =OOO0OO00OOOOO0OOO .iloc [totalindex ]#line:503
                    print ("sucess total inex",len (OOO0OO00OOOOO0OOO ),totalindex ,is_stop )#line:504
                except Exception as O0OOOOO000000O00O :#line:505
                    print ("total index",O0OOOOO000000O00O )#line:506
                    OOOO000OOOOOO0O0O =os .path .join ("cpdata")#line:508
                    O0O0O0O0OOO000OOO =glob (OOOO000OOOOOO0O0O +"/*cont*.csv")#line:509
                    statusupdate ("all-contact-done"+str (O0OOOOO000000O00O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:511
                    try :#line:512
                            time .sleep (2 )#line:513
                            os .remove ("email_app/data/contacts.csv")#line:514
                    except :#line:515
                            pass #line:516
                try :#line:520
                    O0000OOO0O0OO0000 =int (email_index )#line:521
                    if int (O0000OOO0O0OO0000 )>int (O0OOOO00OO0OO0O00 ):#line:522
                        print ("limit smtp")#line:523
                        statusupdate ("limit",smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:524
                        try :#line:525
                            os .remove ("email_app/data/gmail.csv")#line:526
                            time .sleep (2 )#line:527
                        except :#line:528
                            pass #line:529
                        continue #line:531
                except Exception as OO0OO0O00O0OOOO00 :#line:532
                    statusupdate ("limit"+str (OO0OO0O00O0OOOO00 ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:533
                    continue #line:534
                OO00OO0O0O0O00O00 =random .choice (O000O0OOO0OO000OO )#line:535
                OO00OO0000O00O0OO =MIMEMultipart ()#line:536
                O000OOO000O00O0O0 =randint (100000000 ,9999999999 )#line:537
                OOO0OOO0OOO0OOOO0 =randint (1111 ,9999 )#line:538
                O000O0OOO0OO000OO =OO00OO0O0O0O00O00 +" "+"Inv0"+str (O000OOO000O00O0O0 )+" of your item!"#line:539
                OO00OO0000O00O0OO ['Subject']=O000O0OOO0OO000OO #line:540
                OO00OO0000O00O0OO ['From']=f"{random.choice(From)}{OOO0OOO0OOO0OOOO0}<{smtp_email}>"#line:541
                OO00OO0000O00O0OO ['To']=O0000OOOO0O0OO0O0 ['email']#line:542
                O0OOO0O0OO00OOOO0 =randint (100000000 ,999999999 )#line:543
                O0000OO0O0O00OOOO =random .choice (bodies )#line:544
                O00000O000OOOOOO0 =os .path .join (kankadir ,'email_app','data',O0000OO0O0O00OOOO )#line:545
                O00O0OO0O0OO00000 =open (O00000O000OOOOOO0 ,'r').read ()#line:546
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$email',O0000OOOO0O0OO0O0 ['email'])#line:547
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$name',O0000OOOO0O0OO0O0 ['name'])#line:548
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$invoice_no',str (O0OOO0O0OO00OOOO0 ))#line:549
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word1',random .choice (word1 ))#line:550
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word2',random .choice (word2 ))#line:551
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word3',random .choice (word3 ))#line:552
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word4',random .choice (word4 ))#line:553
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word5',random .choice (word5 ))#line:554
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word6',random .choice (word6 ))#line:555
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$word7',random .choice (word7 ))#line:556
                O00O0OO0O0OO00000 =O00O0OO0O0OO00000 .replace ('$invoice_no.smfdmj',str (O0OOO0O0OO00OOOO0 ))#line:557
                OO00OO0000O00O0OO .attach (MIMEText (O00O0OO0O0OO00000 ))#line:558
                try :#line:560
                    OO0O0O000OOO000O0 =os .path .join (kankadir ,'email_app','data','html_code.html')#line:561
                    OO0O0O0OO000O0OOO =open (OO0O0O000OOO000O0 ,'r').read ()#line:562
                    OO0O0O0OO000O0OOO =OO0O0O0OO000O0OOO .replace ('$email',O0000OOOO0O0OO0O0 ['email'])#line:565
                    OO0O0O0OO000O0OOO =OO0O0O0OO000O0OOO .replace ('$name',O0000OOOO0O0OO0O0 ['name'])#line:566
                    OO0O0O0OO000O0OOO =OO0O0O0OO000O0OOO .replace ('$invoice_no.smfdmj',str (O0OOO0O0OO00OOOO0 ))#line:567
                    with open (OO0O0O000OOO000O0 ,'w')as O00000O0OOO0O00O0 :#line:568
                        O00000O0OOO0O00O0 .write (OO0O0O0OO000O0OOO )#line:569
                except Exception as OOOO0O0OO0OO00O00 :#line:570
                    print (OOOO0O0OO0OO00O00 ,"html file")#line:571
                    statusupdate ("stopped html file not found "+str (OOOO0O0OO0OO00O00 ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:572
                    try :#line:573
                        os .remove ("email_app/data/html_code.html")#line:574
                        time .sleep (3 )#line:575
                    except :#line:576
                        pass #line:577
                if O0000OOOOOO00000O =='html_pdf':#line:579
                    O0OOO0O0000O0000O ="Invoice"+str (O000OOO000O00O0O0 )+".pdf"#line:580
                    pdfkit .from_file (OO0O0O000OOO000O0 ,O0OOO0O0000O0000O ,configuration =config )#line:581
                    attach_file_to_email (OO00OO0000O00O0OO ,O0OOO0O0000O0000O )#line:582
                elif O0000OOOOOO00000O =='html_png':#line:583
                    O0OOO0O0000O0000O ="Invoice"+str (O000OOO000O00O0O0 )+".png"#line:584
                    imgkit .from_file (OO0O0O000OOO000O0 ,O0OOO0O0000O0000O ,config =config_img )#line:585
                    attach_file_to_email (OO00OO0000O00O0OO ,O0OOO0O0000O0000O )#line:586
                elif O0000OOOOOO00000O =='html_jpg':#line:587
                    O0OOO0O0000O0000O ="Invoice"+str (O000OOO000O00O0O0 )+".jpg"#line:588
                    imgkit .from_file (OO0O0O000OOO000O0 ,O0OOO0O0000O0000O ,config =config_img )#line:589
                    attach_file_to_email (OO00OO0000O00O0OO ,O0OOO0O0000O0000O )#line:590
                try :#line:592
                    if O0O00OO0OO0O00OOO =='smtp':#line:593
                        try :#line:594
                            send_smtp_email (OO00OO0000O00O0OO ,smtp_email ,OO0O00O0O0O00O00O )#line:595
                            email_index +=1 #line:596
                            frcll =0 #line:597
                        except Exception as O0OOOO00OO0OOOO00 :#line:598
                            if frcll <2 :#line:599
                                if "Connection unexpectedly"in str (O0OOOO00OO0OOOO00 ):#line:600
                                    statusupdate ("gmail-auth-error Connection unexpectedly Closed -- retry "+str (frcll ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:601
                                    frcll +1 #line:602
                                    continue #line:603
                            if frcll >2 :#line:605
                                statusupdate ("gmail-auth-error  "+str (O0OOOO00OO0OOOO00 ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:606
                                frcll =0 #line:607
                                try :#line:608
                                    time .sleep (3 )#line:609
                                    os .remove ("email_app/data/gmail.csv")#line:610
                                    continue #line:611
                                except :#line:612
                                    pass #line:613
                    elif O0O00OO0OO0O00OOO =='google_api':#line:616
                        try :#line:617
                            email_index +=1 #line:618
                            send_email_google_api (OO00OO0000O00O0OO ,smtp_email )#line:619
                        except :#line:620
                            statusupdate ("api-error",smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:621
                    print (email_index ,smtp_email ,"till running",totalindex )#line:624
                    if O0000OOOOOO00000O in ['html_png','html_jpg','html_pdf']:#line:625
                        os .remove (O0OOO0O0000O0000O )#line:626
                    if is_stop :#line:627
                        OO0OO0OOO00O0OO0O =True #line:628
                    else :#line:629
                        OO0OO0OOO00O0OO0O =False #line:630
                    statusupdate ("processing "+str (OO0OO0OOO00O0OO0O ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:631
                    rkkdc =0 #line:632
                    print ({'status':'success','message':f"Email sent to {O0000OOOO0O0OO0O0['email']}",'email_index':email_index })#line:633
                except Exception as OOOO0O00O00OOO0OO :#line:635
                    print (OOOO0O00O00OOO0OO ,"over all execption")#line:636
                    if O0000OOOOOO00000O in ['html_png','html_jpg','html_pdf']:#line:637
                        os .remove (O0OOO0O0000O0000O )#line:638
                    statusupdate (str (OOOO0O00O00OOO0OO ),smtp_email ,email_index ,O0O00OO0OO0O00OOO )#line:639
                    print ({'status':'error','message':str (OOOO0O00O00OOO0OO )})#line:641
def conect_send ():#line:647
    threading .Thread (target =send_ajax_email_fun ).start ()#line:648
def attach_file_to_email (OO000OO0O000OOOOO ,O0OOO0O0OOOOO00OO ):#line:651
    with open (O0OOO0O0OOOOO00OO ,'rb')as O0000O00OOOO00000 :#line:652
        O0OOO000O0O000O00 =MIMEBase ('application','octet-stream')#line:653
        O0OOO000O0O000O00 .set_payload (O0000O00OOOO00000 .read ())#line:654
        encoders .encode_base64 (O0OOO000O0O000O00 )#line:655
        O0OOO000O0O000O00 .add_header ('Content-Disposition',f'attachment; filename={os.path.basename(O0OOO0O0OOOOO00OO)}')#line:656
        OO000OO0O000OOOOO .attach (O0OOO000O0O000O00 )#line:657
def send_smtp_email (OOO00O0O00O000000 ,OO000000OOO000OO0 ,O000O0O0O00O0O0OO ):#line:660
    OO00OOO000O0O0000 =smtplib .SMTP ('smtp.gmail.com',587 )#line:661
    OO00OOO000O0O0000 .ehlo ()#line:662
    OO00OOO000O0O0000 .starttls ()#line:663
    OO00OOO000O0O0000 .ehlo ()#line:664
    OO00OOO000O0O0000 .login (OO000000OOO000OO0 ,O000O0O0O00O0O0OO )#line:665
    OO00OOO000O0O0000 .sendmail (OO000000OOO000OO0 ,OOO00O0O00O000000 ['To'],OOO00O0O00O000000 .as_string ())#line:666
    OO00OOO000O0O0000 .quit ()#line:667
def send_email_google_api (O00O00O0OOOO0OO0O ,O000O00000OOOOOO0 ):#line:670
    OOOOO0O0OO0000OOO =os .path .join (kankadir ,'email_app','credentials')#line:671
    O0O0O0OO0OO0O0000 =['https://mail.google.com/']#line:672
    OO0OO0000O00O000O =None #line:673
    if os .path .exists (OOOOO0O0OO0000OOO +'/token_'+O000O00000OOOOOO0 +'.json'):#line:674
        OO0OO0000O00O000O =Credentials .from_authorized_user_file (OOOOO0O0OO0000OOO +'/token_'+O000O00000OOOOOO0 +'.json',O0O0O0OO0OO0O0000 )#line:675
    if not OO0OO0000O00O000O or not OO0OO0000O00O000O .valid :#line:676
        if OO0OO0000O00O000O and OO0OO0000O00O000O .expired and OO0OO0000O00O000O .refresh_token :#line:677
            OO0OO0000O00O000O .refresh (Request ())#line:678
        else :#line:679
            raise Exception ("Token expired and no refresh token available. Please re-authenticate.")#line:680
        with open (OOOOO0O0OO0000OOO +'/token_'+O000O00000OOOOOO0 +'.json','w')as OO000O0O0000OO00O :#line:682
            OO000O0O0000OO00O .write (OO0OO0000O00O000O .to_json ())#line:683
    O0O0O00O00OO00OOO =build ('gmail','v1',credentials =OO0OO0000O00O000O )#line:685
    OOO0OO0O00OOO0OO0 =base64 .urlsafe_b64encode (O00O00O0OOOO0OO0O .as_bytes ()).decode ('utf-8')#line:686
    O00OO0OO0O0OOO0O0 ={'raw':OOO0OO0O00OOO0OO0 }#line:687
    try :#line:689
        O00O00O0OOOO0OO0O =O0O0O00O00OO00OOO .users ().messages ().send (userId ='me',body =O00OO0OO0O0OOO0O0 ).execute ()#line:690
        print (f'Successfully sent email using Google API: {O00O00O0OOOO0OO0O["id"]}')#line:691
    except HttpError as OO0OO0O0O00OOO00O :#line:692
        print (f'An error occurred: {OO0OO0O0O00OOO00O}')#line:693
        raise #line:694
@app .route ('/upload-files/',methods =['POST','GET'])#line:697
def upload_files_home ():#line:698
    if request .method =='POST':#line:699
        OOOO0OO000O000000 =os .path .join ('cdpath')#line:700
        if not os .path .exists (OOOO0OO000O000000 ):#line:701
            os .makedirs (OOOO0OO000O000000 )#line:702
        def O0OOOOO00OOO0OOOO (O00O0OO0OOO0O0O0O ,O0OO000000O00OO00 ,O0O0O0OO0O0OO000O ):#line:704
            ""#line:705
            if O00O0OO0OOO0O0O0O :#line:706
                OOO00OOOO00O0O0O0 =os .path .join (OOOO0OO000O000000 ,O0OO000000O00OO00 )#line:707
                if not os .path .exists (OOO00OOOO00O0O0O0 ):#line:708
                    os .makedirs (OOO00OOOO00O0O0O0 )#line:709
                O00OOO0OOO0OOOO0O =f"{O0O0O0OO0O0OO000O}_{uuid.uuid4()}.csv"if O0O0O0OO0O0OO000O !='html'else f"{O0O0O0OO0O0OO000O}_{uuid.uuid4()}.html"#line:712
                OOO00000000O0OO0O =os .path .join (OOO00OOOO00O0O0O0 ,O00OOO0OOO0OOOO0O )#line:714
                O00O0OO0OOO0O0O0O .save (OOO00000000O0OO0O )#line:715
                return OOO00000000O0OO0O #line:716
            return None #line:717
        O0O00O0OOOOOOO00O =O0OOOOO00OOO0OOOO (request .files .get ('contacts_file'),'contacts','contacts')#line:720
        OOOO0OOO0O0O0O0OO =O0OOOOO00OOO0OOOO (request .files .get ('subjects_file'),'subjects','subjects')#line:721
        O0O000OOO00OOO00O =O0OOOOO00OOO0OOOO (request .files .get ('gmail_file'),'gmail','gmail')#line:722
        O0OOOO0000O0OOOO0 =O0OOOOO00OOO0OOOO (request .files .get ('html_file'),'html','html')#line:723
        if not (O0O00O0OOOOOOO00O or OOOO0OOO0O0O0O0OO or O0O000OOO00OOO00O or O0OOOO0000O0OOOO0 ):#line:725
            return jsonify ({'message':'No files were uploaded.'}),400 #line:726
        return jsonify ({'success':True ,'contacts_file':O0O00O0OOOOOOO00O ,'subjects_file':OOOO0OOO0O0O0O0OO ,'gmail_file':O0O000OOO00OOO00O ,'html_file':O0OOOO0000O0OOOO0 })#line:727
    return render_template ('email_app/upload_files_home.html')#line:728
@app .route ('/')#line:731
def home ():#line:732
    return render_template ('email_app/home.html')#line:733
@app .route ('/upload-credentials/',methods =['POST','GET'])#line:736
def upload_credentials ():#line:737
    if request .method =='POST':#line:738
        OOOOO00O0O00O00O0 =os .path .join (kankadir ,'email_app','credentials')#line:739
        if not os .path .exists (OOOOO00O0O00O00O0 ):#line:740
            os .makedirs (OOOOO00O0O00O00O0 )#line:741
        def O0000O0000OOOOOO0 (OO0O0OOOO000O0OOO ):#line:743
            O0O000O0O00O0O000 =os .path .join (OOOOO00O0O00O00O0 ,OO0O0OOOO000O0OOO )#line:744
            if os .path .exists (O0O000O0O00O0O000 ):#line:745
                os .remove (O0O000O0O00O0O000 )#line:746
        OO0OOOOO0OO00O0OO =request .files .getlist ('credentials_files')#line:748
        if OO0OOOOO0OO00O0OO :#line:749
            for OO00OO0O000OO00O0 in OO0OOOOO0OO00O0OO :#line:750
                O0000O0000OOOOOO0 (OO00OO0O000OO00O0 .filename )#line:751
                OO00OO0O000OO00O0 .save (os .path .join (OOOOO00O0O00O00O0 ,secure_filename (OO00OO0O000OO00O0 .filename )))#line:752
        return jsonify ({"status":"successfully uploaded"})#line:754
    return render_template ('email_app/upload_credentials.html')#line:756
'''
def send_ajax_function():
    """Simulate a long-running background task with Flask application context."""
    global is_stop
    with app.app_context():  # Push the application context
        print("Task started in background...")
        while  is_stop:
            print("Sending email...")
            time.sleep(1)  # Simulate sending an email every 2 seconds
            if not is_stop:
                break
        print("Task completed or stopped.")'''#line:770
@app .route ('/startsending',methods =['POST'])#line:771
def start_task ():#line:772
    ""#line:773
    global is_stop #line:774
    is_stop =True #line:775
    update_json_value (True )#line:776
    with lock :#line:777
        if is_stop :#line:778
            OO00000OOO000000O =threading .Thread (target =send_ajax_email_fun )#line:779
            OO00000OOO000000O .start ()#line:780
            return jsonify ({"status":"Task started in the background."}),200 #line:781
        else :#line:782
            time .sleep (1 )#line:783
            return jsonify ({"status":"Task is already Stopped."}),200 #line:784
@app .route ('/stopserver',methods =['POST'])#line:785
def stop_task ():#line:787
    ""#line:788
    global is_stop #line:789
    with lock :#line:790
        update_json_value (False )#line:791
        print (read_json_value ())#line:792
        is_stop =False #line:793
    return jsonify ({"status":"Task stopped."}),200 #line:794
if __name__ =='__main__':#line:795
    app .run (host =hosts ,port =8000 ,debug =True )#line:796

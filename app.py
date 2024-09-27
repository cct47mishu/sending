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
    path_wkhtmltopdf =r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'#line:23
    path_wkhtmltoimg =r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'#line:24
else :#line:25
    path_wkhtmltopdf ='/usr/bin/wkhtmltopdf'#line:26
    path_wkhtmltoimg ='/usr/bin/wkhtmltoimage'#line:27
config =pdfkit .configuration (wkhtmltopdf =path_wkhtmltopdf )#line:29
config_img =imgkit .config (wkhtmltoimage =path_wkhtmltoimg )#line:31
bodies =['body.txt','body2.txt','body3.txt','body4.txt','body5.txt']#line:32
From =["Billing Support#","PP Support Team#","Billing Desk#","Billing Department","PP Billing Team#","PP Order update#","PP Billing#"]#line:34
word1 =["Hello","Hi","Greetings","Good morning","Hope your doing well","Good evening","Hope your doing good","Hope your doing well" "Hello!","Hi!","Hey there!","Good morning!","Good afternoon!","Good evening!","How are you?","What's up?","Howdy!","Greetings!","Nice to meet you!","How have you been?","Long time no see!","What's new?","How's it going?","How's your day?","How's everything?","How are you doing today?","What's happening?","How's life treating you?","Hey, how's the world been treating you?","It's great to see you!","What have you been up to?","How's your week been?","What's going on in your world?","How's your day been so far?","I hope you're having a fantastic day!","How are things on your end?","It's a pleasure to meet you!","I hope you're doing well!","How's your family?","How's your job going?","What's the latest with you?","I hope you're having a wonderful day!","How's your weekend shaping up?","What's the word on the street?","How's your health?","I trust you're keeping well?","What's the buzz?","How's everything going for you?","What's the scoop?","How's your day treating you so far?","I hope all is well with you!","What's the plan for today?","How's the weather over there?","What's the good news?","I hope you're enjoying your day!","How's your journey been?","What's the story?","I hope you're having a pleasant time!"]#line:36
word2 =["Please","kindly","Do","At your earlier convenience","At your earlier convenience Please","At your earlier convenience kindly","At your earlier convenience Do","please do" "Please do it at your earlier convenience.","Kindly complete it at your earlier convenience.","Do it at your earlier convenience, please.","Please do it when convenient for you.","Kindly complete it when convenient for you.","Do it when convenient for you, please.","Please do it as soon as possible.","Kindly complete it as soon as possible.","Do it as soon as possible, please.","Please do it at your earliest convenience.","Kindly complete it at your earliest convenience.","Do it at your earliest convenience, please.","Please do it at your soonest availability.","Kindly complete it at your soonest availability.","Do it at your soonest availability, please.","Please do it at your first opportunity.","Kindly complete it at your first opportunity.","Do it at your first opportunity, please.","Please do it at your quickest convenience.","Kindly complete it at your quickest convenience.","Do it at your quickest convenience, please.","Please do it without delay.","Kindly complete it without delay.","Do it without delay, please.","Please do it promptly.","Kindly complete it promptly.","Do it promptly, please.","Please do it at your earliest convenience possible.","Kindly complete it at your earliest convenience possible.","Do it at your earliest convenience possible, please.","Please do it at your utmost convenience.","Kindly complete it at your utmost convenience.","Do it at your utmost convenience, please.","Please do it at your soonest possible time.","Kindly complete it at your soonest possible time.","Do it at your soonest possible time, please.","Please do it without hesitation.","Kindly complete it without hesitation.","Do it without hesitation, please.","Please do it expediently.","Kindly complete it expediently.","Do it expediently, please.","Please do it with priority.","Kindly complete it with priority.","Do it with priority, please.","Please do it at your earliest convenience, if possible.","Kindly complete it at your earliest convenience, if possible.","Do it at your earliest convenience, if possible, please.","Please do it as early as you can.","Kindly complete it as early as you can."]#line:38
word3 =["refer to","view","check","check out","acknowledge" "Consult","Examine","Explore","Review","Inspect","Study","Glance","Peruse","Scan","Assess","Evaluate","Verify","Monitor","Scrutinize","Investigate","Look over","Read","Consider","Watch","Pay attention to","Follow","Note","Sight","Spot","Catch a glimpse of","Take a look at","Attend to","Check up on","Appraise","Size up","Cross-reference","Acknowledge","Recognize","Confirm","Validate","Agree","Accept","Comprehend","Realize","Understand","Admit","Appreciate","Embrace","Grant","Notice","Own","Concede","Witness","Respect","Own up to"]#line:40
word4 =["the","your","a","an"]#line:42
word5 =["invoice","Bill","Receipt","order-invoice","order-receipt","order-bill","purchase-invoice","purchase-receipt","purchase-bill" "Invoice","Bill","Receipt","Statement","Voucher","Account","Purchase","Order","Transaction","Payment","Sales","Expense","Cost","Document","Record","Proof","Tax","Credit","Debit","Balance","Due","Amount","Total","Itemized","Settlement","Remittance","Disbursement","Claim","Claimed","Reimbursement","Taxable","Non-taxable","Billing","Pricing","Rate","Delivery","Shipment","Confirmation","Contract","Agreement","Inventory","Stock","Return","Refund","Exchange","Adjustment","Overdue","Late","Credit note","Payable"]#line:44
word6 =["#-",".","#","@",":",":-",",","*"]#line:46
word7 =["Thanks","Thank you","Thanking you","regards","kind regards","warm wishes","Have a great day","Best regards","sincerely","best of luck","Thanks a lots ","Thank you, yours faithfully","Thank you once again" "Thanks!","Thank you!","Thanking you.","Regards.","Kind regards.","Warm wishes.","Have a great day!","Best regards.","Sincerely.","Best of luck.","Thanks a lot!","Thank you, yours faithfully.","Thank you once again.","Many thanks!","Appreciate it.","Grateful for your help.","Sending my thanks.","Much obliged.","Many thanks for your assistance.","I'm truly thankful.","Thank you for your time and consideration.","I extend my sincere gratitude.","Thank you kindly.","I appreciate your support.","Thanks a bunch!","Deeply grateful.","Thank you for going above and beyond.","With heartfelt thanks.","I'm grateful for your understanding.","Thank you for your patience.","Warmest thanks.","Many thanks for your kind cooperation.","Thank you for your prompt response.","It's greatly appreciated.","I'm thankful for your guidance.","Thank you for being so helpful.","Wishing you all the best.","Warmest regards.","With sincere appreciation.","Best wishes for success.","Sending my regards.","Wishing you a wonderful day.","Take care and best regards.","With deepest thanks.","Grateful for your generosity.","Wishing you continued success.","Thank you for everything.","With warmest appreciation.","All the best in your endeavors.","Thank you for your thoughtfulness." "Order placed successfully.","Transaction completed.","Purchase confirmed.","Success! Your order is on its way.","Thank you for your order.","Order successfully processed.","Your purchase is complete.","Order placed successfully.","Congratulations! Order confirmed.","Success! Your items will be delivered soon.","Payment received. Order confirmed.","Your transaction is successful.","Purchase successfully finalized.","Thank you for your purchase.","Order successfully submitted.","Transaction approved.","Purchase completed successfully.","Order confirmed. Thank you!","Success! Your payment went through.","Thank you for shopping with us.","Order successfully received.","Transaction successful. Thank you!","Purchase confirmed. Enjoy your products.","Order placed. Payment received.","Success! Your order is being processed.","Thank you for choosing us.","Order successfully booked.","Transaction complete. Thank you for your business.","Purchase verified. Thank you for your trust.","Order successfully approved.","Congratulations! Purchase confirmed.","Success! Your items are on their way to you.","Thank you for placing your order with us.","Order successfully registered.","Transaction successfully processed.","Purchase successful. Thank you for your support.","Order confirmed. Delivery in progress.","Success! Your payment has been cleared.","Thank you for your valued purchase.","Order successfully dispatched.","Transaction completed. Thank you for choosing us.","Purchase confirmed. Enjoy your new items.","Order successfully finalized.","Congratulations! Your purchase is on its way.","Thank you for your order. We appreciate your business.","Order successfully shipped.","Transaction successful. Enjoy your purchase.","Purchase completed. Thank you for shopping with us.","Order confirmed. Expect delivery soon.","Success! Your payment is successful."]#line:49
email_details =[]#line:51
kankadir =os .path .dirname (os .path .abspath (__file__ ))#line:55
JSON_FILE_PATH =os .path .join (kankadir ,'db.json')#line:56
smtp_email =''#line:57
email_index =0 #line:58
is_stop =True #line:59
datafilejson ={}#line:60
@app .route ('/email_app/')#line:61
@app .route ('/email_app/<path:subpath>')#line:62
def view_email_app (subpath =None ):#line:63
    OO00O0O0OOOO0O0OO =os .path .join (os .getcwd (),'email_app')#line:64
    try :#line:65
        if not subpath :#line:67
            OOO0OO0000OO0OOOO =OO00O0O0OOOO0O0OO #line:68
        else :#line:69
            OOO0OO0000OO0OOOO =os .path .join (OO00O0O0OOOO0O0OO ,subpath )#line:71
        if os .path .isdir (OOO0OO0000OO0OOOO ):#line:74
            O0O00O0O0OO0OO0O0 =os .listdir (OOO0OO0000OO0OOOO )#line:76
            return render_template ('file_list.html',files =O0O00O0O0OO0OO0O0 ,folder =subpath or '')#line:77
        elif os .path .isfile (OOO0OO0000OO0OOOO ):#line:80
            return send_from_directory (os .path .dirname (OOO0OO0000OO0OOOO ),os .path .basename (OOO0OO0000OO0OOOO ))#line:81
        else :#line:83
            abort (404 )#line:85
    except Exception as O0OOOO0OOOO0OO00O :#line:86
        return f"Error: {str(O0OOOO0OOOO0OO00O)}",500 #line:87
def remove_files ():#line:88
    OOO0O000OOO00OO0O =os .getcwd ()#line:90
    OOO0O00O00OOO00OO =['*.png','*.jpg','*.pdf']#line:93
    for O00OO0OOO0O0O0O00 in OOO0O00O00OOO00OO :#line:96
        O000OO0OO00O0O0OO =glob .glob (os .path .join (OOO0O000OOO00OO0O ,O00OO0OOO0O0O0O00 ))#line:98
        for OO0OOOO000O0O00O0 in O000OO0OO00O0O0OO :#line:101
            try :#line:102
                os .remove (OO0OOOO000O0O00O0 )#line:103
                print (f"Removed file: {OO0OOOO000O0O00O0}")#line:104
            except Exception as OOO000O00OO0OO000 :#line:105
                print (f"Error removing file {OO0OOOO000O0O00O0}: {OOO000O00OO0OO000}")#line:106
def statuscheck ():#line:107
    OO00000O00O000O00 =os .path .join (kankadir ,"serer-status.txt")#line:108
    if os .path .exists (OO00000O00O000O00 ):#line:109
        OOOO000OOOO0O000O =[]#line:110
        try :#line:111
            with open (OO00000O00O000O00 ,"r")as OO0OO0OOOO0000O0O :#line:112
                OOOO000OOOO0O000O .append (OO0OO0OOOO0000O0O .read ())#line:113
        except :#line:114
            pass #line:115
        return {"status":OOOO000OOOO0O000O [0 ]}#line:116
    return False #line:117
def read_json_value ():#line:120
    try :#line:121
        with open (JSON_FILE_PATH ,'r')as O0OO0O0O0OOOOO0O0 :#line:122
            OOO0O00O0OO00O0O0 =json .load (O0OO0O0O0OOOOO0O0 )#line:123
        O0OO0O0O0OOOOO0O0 .close ()#line:124
        return OOO0O00O0OO00O0O0 .get ('value',False )#line:125
    except (FileNotFoundError ,json .JSONDecodeError ):#line:126
        print ("errors")#line:127
        return False #line:128
def write_json_value (O0OO0O0000O00OOO0 ):#line:131
    try :#line:132
        with open (JSON_FILE_PATH ,'w')as OOOOOO0O0000O000O :#line:133
            json .dump ({"value":O0OO0O0000O00OOO0 },OOOOOO0O0000O000O )#line:134
        OOOOOO0O0000O000O .close ()#line:135
    except Exception as O00OO0OO0000O000O :#line:136
        print (f"Error writing to JSON file: {O00OO0OO0000O000O}")#line:137
def update_json_value (O00O00OOO000OO0O0 ):#line:140
    write_json_value (O00O00OOO000OO0O0 )#line:142
@app .route ('/reset/',methods =['POST','GET'])#line:145
def reset ():#line:146
    try :#line:147
        remove_files ()#line:148
    except :#line:149
        pass #line:150
    try :#line:151
        OOOOOO0000000O000 =os .path .dirname (os .path .abspath (__file__ ))#line:152
        O0OOOO00OO00O00OO =os .path .join (OOOOOO0000000O000 ,"onstatus.json")#line:153
        OOO0O0OOO00OOOOO0 =os .path .join (OOOOOO0000000O000 ,"data.json")#line:154
        try :#line:155
            os .remove (O0OOOO00OO00O00OO )#line:156
        except :#line:157
            pass #line:158
        try :#line:159
            os .remove (OOO0O0OOO00OOOOO0 )#line:160
        except :#line:161
            pass #line:162
        for O00OO00O0O00OO0O0 in [OOO0O0OOO00OOOOO0 ,O0OOOO00OO00O00OO ]:#line:163
            if os .path .exists (O00OO00O0O00OO0O0 ):#line:164
                try :#line:165
                    os .remove (O00OO00O0O00OO0O0 )#line:166
                except Exception as OO0O0000OOOOO00OO :#line:167
                    print (f"Error removing {O00OO00O0O00OO0O0}: {OO0O0000OOOOO00OO}")#line:168
        OOO0OOO0OOOOOOO00 =os .path .join (OOOOOO0000000O000 ,'email_app','data')#line:170
        OOOO0O0O0OOOOOO0O =glob .glob (os .path .join (OOO0OOO0OOOOOOO00 ,"*.csv"))#line:171
        OO0OOO00OOO00OO00 =glob .glob (os .path .join (OOO0OOO0OOOOOOO00 ,"*.html"))#line:172
        for O0OOOOO00O00O0OO0 in OOOO0O0O0OOOOOO0O :#line:174
            try :#line:175
                os .remove (O0OOOOO00O00O0OO0 )#line:176
                print (f"Removed: {O0OOOOO00O00O0OO0}")#line:177
            except Exception as OO0O0000OOOOO00OO :#line:178
                print (f"Error removing {O0OOOOO00O00O0OO0}: {OO0O0000OOOOO00OO}")#line:179
        for O0OOOOO00O00O0OO0 in OO0OOO00OOO00OO00 :#line:181
            try :#line:182
                os .remove (O0OOOOO00O00O0OO0 )#line:183
                print (f"Removed: {O0OOOOO00O00O0OO0}")#line:184
            except Exception as OO0O0000OOOOO00OO :#line:185
                print (f"Error removing {O0OOOOO00O00O0OO0}: {OO0O0000OOOOO00OO}")#line:186
        try :#line:187
            shutil .rmtree ("cdpath")#line:188
        except :#line:189
            pass #line:190
        return jsonify ({'status':'success','message':'Files and directories reset successfully.'})#line:191
    except Exception as OO0O0000OOOOO00OO :#line:192
        return jsonify ({'status':'error','message':str (OO0O0000OOOOO00OO )}),500 #line:193
def get_total_email_count ():#line:196
    global datafilejson #line:197
    OOOO0000000OOO00O =0 #line:198
    OOOO0OOOO0O0000O0 =os .path .join (kankadir ,"onstatus.json")#line:199
    if os .path .exists (OOOO0OOOO0O0000O0 ):#line:200
        with open (OOOO0OOOO0O0000O0 ,'r')as O0OO0OOOO0OOO00OO :#line:201
            O000O00OO000OO0O0 =json .load (O0OO0OOOO0OOO00OO )#line:202
            datafilejson =O000O00OO000OO0O0 #line:203
            for O00OOOOO000O00OO0 in O000O00OO000OO0O0 .values ():#line:204
                if "count"in O00OOOOO000O00OO0 :#line:205
                    OOOO0000000OOO00O +=O00OOOOO000O00OO0 ["count"]#line:206
        O0OO0OOOO0OOO00OO .close ()#line:207
    return OOOO0000000OOO00O #line:208
@app .route ('/alldata/',methods =['GET'])#line:211
def alldata ():#line:212
    global datafilejson #line:213
    O00OO000OO00OOO0O =os .path .join (kankadir ,"onstatus.json")#line:214
    if os .path .exists (O00OO000OO00OOO0O ):#line:216
            OO00OOOO00O000OOO =datafilejson #line:218
            return jsonify (OO00OOOO00O000OOO )#line:219
    return jsonify ({'error':'not sedding yet'})#line:220
def emailcount (OOO0O0O00OOOO000O ):#line:223
    global datafilejson #line:224
    O00O0OOO00OO000O0 =os .path .join (kankadir ,"onstatus.json")#line:225
    O0OOOO0000OOO0OOO =None #line:226
    if os .path .exists (O00O0OOO00OO000O0 ):#line:227
        with open (O00O0OOO00OO000O0 ,'r')as O00OOO0O00OO0OO00 :#line:228
            O000O0O00O000OO0O =json .load (O00OOO0O00OO0OO00 )#line:229
            datafilejson =O000O0O00O000OO0O #line:230
            O000OO000OO00O0OO =O000O0O00O000OO0O [OOO0O0O00OOOO000O ]["count"]#line:231
            O0OOOO0000OOO0OOO =int (O000OO000OO00O0OO )#line:232
        O00OOO0O00OO0OO00 .close ()#line:233
    return O0OOOO0000OOO0OOO #line:234
def load_data (O0O0O0O000OO0O0OO ):#line:237
    OO00OOO00000OO000 =os .path .dirname (os .path .abspath (__file__ ))#line:238
    O0O0OO0OOO0O000O0 =os .path .join (OO00OOO00000OO000 ,'email_app','data','contacts.csv')#line:241
    O0O00O00O0OOOO00O =os .path .join (OO00OOO00000OO000 ,'email_app','data','gmail.csv')#line:242
    OOOO000OOO0O00O00 =os .path .join (OO00OOO00000OO000 ,'email_app','data','subjects.csv')#line:243
    OOO00O00O0OO0OOOO =os .path .join (OO00OOO00000OO000 ,'email_app','data','html_code.html')#line:244
    if not os .path .exists (O0O0OO0OOO0O000O0 ):#line:247
        move_file (apps ='contacts')#line:248
        time .sleep (4 )#line:249
    if not os .path .exists (OOO00O00O0OO0OOOO ):#line:250
        move_file (apps ='html')#line:251
        time .sleep (4 )#line:252
    if not os .path .exists (O0O00O00O0OOOO00O ):#line:253
        move_file (apps ='gmail')#line:254
        time .sleep (4 )#line:255
    if not os .path .exists (OOOO000OOO0O00O00 ):#line:256
        move_file (apps ='subjects')#line:257
        time .sleep (4 )#line:258
    try :#line:260
        OOOOOOO0OOOOOOOO0 =pd .read_csv (O0O0OO0OOO0O000O0 )#line:261
    except FileNotFoundError :#line:262
        return {'message':'Contacts file could not be loaded even after moving.'}#line:263
    OO00O0OO00OOOO0OO =False #line:264
    if O0O0O0O000OO0O0OO =="smtp":#line:265
        try :#line:266
            O000000O00OO00OO0 =pd .read_csv (O0O00O00O0OOOO00O )#line:267
            OO00O0OO00OOOO0OO =O000000O00OO00OO0 ['email'].iloc [0 ]#line:268
        except FileNotFoundError :#line:269
            return {'message':'SMTP accounts file could not be loaded even after moving.'}#line:270
    else :#line:271
        O0OO0O00OOO0OOO00 =os .path .join (OO00OOO00000OO000 ,'email_app','credentials')#line:272
        O0O00OOOO0O0OOO00 =glob .glob (os .path .join (O0OO0O00OOO0OOO00 ,'*.json'))#line:273
        if not O0O00OOOO0O0OOO00 :#line:275
            return {'message':'No JSON file found in credentials directory.'}#line:276
        O0OOOO0O0O0OO0O00 =os .path .basename (O0O00OOOO0O0OOO00 [0 ])#line:278
        O00000OOOO0OOO00O =re .findall (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',O0OOOO0O0O0OO0O00 )[0 ]#line:279
        OO0OOOOO0O000OO00 =str (O00000OOOO0OOO00O ).replace (".json","").replace ("token_","")#line:280
        O000000O00OO00OO0 =OO0OOOOO0O000OO00 #line:281
    try :#line:283
        OO0O00OOOOOO0OOOO =pd .read_csv (OOOO000OOO0O00O00 )['subject'].tolist ()#line:284
    except FileNotFoundError :#line:285
        return {'message':'Subjects file could not be loaded even after moving.'}#line:286
    return OOOOOOO0OOOOOOOO0 ,O000000O00OO00OO0 ,OO0O00OOOOOO0OOOO ,OO00O0OO00OOOO0OO #line:289
def statusupdate (OOO00O0O0OOO0O0O0 ,O0OO0000OOOO0OO00 ,OO0000000OO0O00OO ,OO0000O000OOO000O ):#line:292
    OO0O000OO000O000O =os .path .join (kankadir ,"onstatus.json")#line:293
    try :#line:294
        if os .path .exists (OO0O000OO000O000O ):#line:295
            with open (OO0O000OO000O000O ,'r')as OO0OOO000OOOOO00O :#line:296
                O0OO00O0OO0OOOOO0 =json .load (OO0OOO000OOOOO00O )#line:297
        else :#line:298
            O0OO00O0OO0OOOOO0 ={}#line:299
        O0OO00O0OO0OOOOO0 [O0OO0000OOOO0OO00 ]={"status":OOO00O0O0OOO0O0O0 ,"timestamp":datetime .now ().isoformat (),"count":OO0000000OO0O00OO ,"type":OO0000O000OOO000O }#line:306
        with open (OO0O000OO000O000O ,'w')as OO0OOO000OOOOO00O :#line:308
            json .dump (O0OO00O0OO0OOOOO0 ,OO0OOO000OOOOO00O ,indent =4 )#line:309
        OO0OOO000OOOOO00O .close ()#line:310
        print (f"Status updated: {OOO00O0O0OOO0O0O0} for email: {O0OO0000OOOO0OO00} with count: {OO0000000OO0O00OO}")#line:311
    except Exception as O0OO0OO0OO0OOOO00 :#line:313
        print (f"Error updating status: {O0OO0OO0OO0OOOO00}")#line:314
@app .route ('/stopmethod/',methods =['POST'])#line:320
def stopmethod ():#line:321
    global is_stop #line:322
    try :#line:324
        update_json_value (False )#line:325
        is_stop =False #line:326
        return jsonify ({"status":"stopped"})#line:327
    except Exception as OO000OO0OOOOO0O0O :#line:328
        return jsonify ({"status":str (OO000OO0OOOOO0O0O )})#line:329
@app .route ('/send-email/',methods =['POST','GET'])#line:332
def send_email_ajax ():#line:333
    OO0O000000OOO0000 =os .path .join (kankadir ,"data.json")#line:334
    if request .method =='POST':#line:335
        O0000O0OOOOOOO0O0 =request .form .get ('conversion_type')#line:336
        O0O000O00OO000O0O =request .form .get ('sending_method')#line:337
        O00O0O000OOOOOOO0 =request .form .get ('limits')#line:338
        OOO00OO0OO00O00O0 ={"conversion_type":O0000O0OOOOOOO0O0 ,"sending_method":O0O000O00OO000O0O ,"limits":O00O0O000OOOOOOO0 }#line:339
        with open (OO0O000000OOO0000 ,'w')as O000O00O0O000000O :#line:341
            json .dump (OOO00OO0OO00O00O0 ,O000O00O0O000000O ,indent =4 )#line:342
        O000O00O0O000000O .close ()#line:343
        try :#line:345
            print (read_json_value ())#line:347
            return jsonify ({'status':'Configuration Sent'})#line:348
        except Exception as O00O00O00O00O00OO :#line:349
            print (O00O00O00O00O00OO )#line:350
        return jsonify ({'status':'Error Configruation--'})#line:352
    else :#line:354
        return render_template ('email_app/send_email.html')#line:355
try :#line:358
    totalindex =get_total_email_count ()#line:359
except :#line:360
    totalindex =0 #line:361
def move_file (apps ='gmail'):#line:363
    OO0OO00OOO0OOO00O ='cdpath'#line:365
    O00OOOO0O0OOO00O0 ={'gmail':'gmail.csv','contacts':'contacts.csv','subjects':'subjects.csv','html':'html_code.html'}#line:368
    if apps not in O00OOOO0O0OOO00O0 :#line:369
        return {'message':f"Invalid app name '{apps}'. Must be one of {', '.join(O00OOOO0O0OOO00O0.keys())}."},400 #line:370
    O0O0O0OO00OO00OOO =os .path .join (OO0OO00OOO0OOO00O ,apps )#line:373
    OOO00O0000OO000O0 =os .path .join ('email_app','data')#line:374
    if not os .path .exists (OOO00O0000OO000O0 ):#line:377
        os .makedirs (OOO00O0000OO000O0 )#line:378
    OOOO0000OOO00O0OO =glob .glob (os .path .join (O0O0O0OO00OO00OOO ,'*'))#line:382
    if not OOOO0000OOO00O0OO :#line:385
        return {'message':f'No {apps} files to move'},404 #line:386
    OO00000O00OO0O0OO =OOOO0000OOO00O0OO [0 ]#line:389
    OO0000OO0O000000O =O00OOOO0O0OOO00O0 [apps ]#line:392
    OOO00O0O0000O0000 =os .path .join (OOO00O0000OO000O0 ,OO0000OO0O000000O )#line:395
    try :#line:397
        shutil .move (OO00000O00OO0O0OO ,OOO00O0O0000O0000 )#line:399
        return {'message':f'{apps.capitalize()} file moved successfully','file':os .path .basename (OOO00O0O0000O0000 )}#line:402
    except Exception as OO0O0OO0000OO0O0O :#line:404
        return {'message':f'Error moving file: {str(OO0O0OO0000OO0O0O)}'},500 #line:406
rkkdc =0 #line:407
maimuna =0 #line:408
def send_ajax_email_fun ():#line:409
    global email_index ,is_stop ,totalindex ,smtp_email ,crc ,rkkdc ,maimuna #line:410
    while True :#line:413
            try :#line:415
                totalindex =get_total_email_count ()#line:416
            except :#line:417
                totalindex =0 #line:418
            OOOO0OOO0O0O000OO =os .path .join (kankadir ,"data.json")#line:420
            if os .path .exists (OOOO0OOO0O0O000OO ):#line:421
                with open (OOOO0OOO0O0O000OO ,'r')as OO00OOOOO000O0O0O :#line:422
                    O0OO00O0O0OO0O0O0 =json .load (OO00OOOOO000O0O0O )#line:423
                O0000O0O00OO0OO0O =O0OO00O0O0OO0O0O0 .get ('conversion_type')#line:424
                OO0O0O000000O0OO0 =O0OO00O0O0OO0O0O0 .get ('sending_method')#line:425
                OOO00O0OO000OO0OO =O0OO00O0O0OO0O0O0 .get ('limits')#line:426
            try :#line:428
                is_stop =read_json_value ()#line:429
            except Exception as O0000OOOOO0OOO000 :#line:430
                print (O0000OOOOO0OOO000 )#line:431
                is_stop =is_stop #line:432
            if OO0O0O000000O0OO0 =='smtp':#line:435
                try :#line:436
                    O00OOOO0OOOOO00O0 ,O00OO00OOOOO00OOO ,OOOOO000OO0000O00 ,OOOOO0OO00OO00O0O =load_data ('smtp')#line:437
                    smtp_email =OOOOO0OO00OO00O0O #line:438
                except Exception as OO0O0OO00O0O0OOOO :#line:440
                    if maimuna >3 :#line:441
                        statusupdate ("no more Smtp Left "+str (OO0O0OO00O0O0OOOO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:442
                        continue #line:443
                    if "value"in str (OO0O0OO00O0O0OOOO ):#line:444
                        maimuna +=1 #line:445
                    statusupdate ("stopped "+str (OO0O0OO00O0O0OOOO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:447
                    continue #line:448
                O00O0O00O00O00OOO =O00OO00OOOOO00OOO .iloc [0 ]#line:451
                O000OOO0OO0O0O000 =O00O0O00O00O00OOO ['password']#line:453
            elif OO0O0O000000O0OO0 =='google_api':#line:454
                try :#line:455
                    O00OOOO0OOOOO00O0 ,O00OO00OOOOO00OOO ,OOOOO000OO0000O00 =load_data ('api')#line:456
                except Exception as OO0O0OO00O0O0OOOO :#line:458
                    if maimuna >3 :#line:459
                        statusupdate ("no more Smtp Left "+str (OO0O0OO00O0O0OOOO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:460
                        update_json_value (False )#line:461
                        is_stop =False #line:462
                        break #line:463
                    if "value"in str (OO0O0OO00O0O0OOOO ):#line:464
                        maimuna +=1 #line:465
                    print ("smtp exection2",OO0O0OO00O0O0OOOO )#line:468
                    statusupdate ("stopped "+str (OO0O0OO00O0O0OOOO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:470
                    continue #line:472
                O00O0O00O00O00OOO =O00OO00OOOOO00OOO #line:474
                smtp_email =O00O0O00O00O00OOO #line:475
            try :#line:477
                O0000O0O0OOOOOOO0 =emailcount (smtp_email )#line:478
                email_index =int (O0000O0O0OOOOOOO0 )#line:479
            except Exception as OO0000OOO000OOOO0 :#line:480
                email_index =0 #line:481
            if not is_stop :#line:483
                if rkkdc >3 :#line:484
                    update_json_value (True )#line:485
                    is_stop =True #line:486
                    rkkdc =0 #line:487
                if is_stop :#line:488
                        O0OO0OO0OOOOO00O0 ="False"#line:489
                else :#line:490
                        O0OO0OO0OOOOO00O0 ="True"#line:491
                statusupdate ("stopped "+str (O0OO0OO0OOOOO00O0 ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:493
                rkkdc +=1 #line:494
                continue #line:496
            if is_stop :#line:498
                try :#line:499
                    O00O0OO0O00000000 =O00OOOO0OOOOO00O0 .iloc [totalindex ]#line:500
                    print ("sucess total inex",len (O00OOOO0OOOOO00O0 ),totalindex ,is_stop )#line:501
                except Exception as O0000OOO0O0OOO0OO :#line:502
                    print ("total index",O0000OOO0O0OOO0OO )#line:503
                    OO0O0OO0O000OOO00 =os .path .join ("cpdata")#line:505
                    O0O0OOOO00O0O00OO =glob (OO0O0OO0O000OOO00 +"/*cont*.csv")#line:506
                    statusupdate ("all-contact-done"+str (O0000OOO0O0OOO0OO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:508
                    try :#line:509
                            time .sleep (2 )#line:510
                            os .remove ("email_app/data/contacts.csv")#line:511
                    except :#line:512
                            pass #line:513
                try :#line:517
                    OOOOO0O0OO000OO00 =int (email_index )#line:518
                    if int (OOOOO0O0OO000OO00 )>int (OOO00O0OO000OO0OO ):#line:519
                        print ("limit smtp")#line:520
                        statusupdate ("limit",smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:521
                        try :#line:522
                            os .remove ("email_app/data/gmail.csv")#line:523
                            time .sleep (2 )#line:524
                        except :#line:525
                            pass #line:526
                        continue #line:528
                except Exception as OO000O00O000000O0 :#line:529
                    statusupdate ("limit"+str (OO000O00O000000O0 ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:530
                    continue #line:531
                OO00OO0000O00OOOO =random .choice (OOOOO000OO0000O00 )#line:532
                O000OO0OOOOOOOO00 =MIMEMultipart ()#line:533
                O0OOO000000OOOO0O =randint (100000000 ,9999999999 )#line:534
                O0OO0000O000OO000 =randint (1111 ,9999 )#line:535
                OOOOO000OO0000O00 =OO00OO0000O00OOOO +" "+"INV812"+str (O0OOO000000OOOO0O )+" of your item."#line:536
                O000OO0OOOOOOOO00 ['Subject']=OOOOO000OO0000O00 #line:537
                O000OO0OOOOOOOO00 ['From']=f"{random.choice(From)}{O0OO0000O000OO000}<{smtp_email}>"#line:538
                O000OO0OOOOOOOO00 ['To']=O00O0OO0O00000000 ['email']#line:539
                OO00O0OOO00OOOO0O =randint (100000000 ,999999999 )#line:540
                OOOO0OO0O0000O000 =random .choice (bodies )#line:541
                O0OOO0O0O000000O0 =os .path .join (kankadir ,'email_app','data',OOOO0OO0O0000O000 )#line:542
                OO0O000OOOOO000O0 =open (O0OOO0O0O000000O0 ,'r').read ()#line:543
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$email',O00O0OO0O00000000 ['email'])#line:544
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$name',O00O0OO0O00000000 ['name'])#line:545
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$invoice_no',str (OO00O0OOO00OOOO0O ))#line:546
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word1',random .choice (word1 ))#line:547
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word2',random .choice (word2 ))#line:548
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word3',random .choice (word3 ))#line:549
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word4',random .choice (word4 ))#line:550
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word5',random .choice (word5 ))#line:551
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word6',random .choice (word6 ))#line:552
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$word7',random .choice (word7 ))#line:553
                OO0O000OOOOO000O0 =OO0O000OOOOO000O0 .replace ('$invoice_no.smfdmj',str (OO00O0OOO00OOOO0O ))#line:554
                O000OO0OOOOOOOO00 .attach (MIMEText (OO0O000OOOOO000O0 ))#line:555
                try :#line:557
                    O0OOO0O00OO00O0O0 =os .path .join (kankadir ,'email_app','data','html_code.html')#line:558
                    OO0OO00000OOOOO0O =open (O0OOO0O00OO00O0O0 ,'r').read ()#line:559
                    OO0OO00000OOOOO0O =OO0OO00000OOOOO0O .replace ('$email',O00O0OO0O00000000 ['email'])#line:562
                    OO0OO00000OOOOO0O =OO0OO00000OOOOO0O .replace ('$name',O00O0OO0O00000000 ['name'])#line:563
                    OO0OO00000OOOOO0O =OO0OO00000OOOOO0O .replace ('$invoice_no.smfdmj',str (OO00O0OOO00OOOO0O ))#line:564
                    with open (O0OOO0O00OO00O0O0 ,'w')as OOOOOO000OOOOOOOO :#line:565
                        OOOOOO000OOOOOOOO .write (OO0OO00000OOOOO0O )#line:566
                except Exception as O000000OO0OOO00OO :#line:567
                    print (O000000OO0OOO00OO ,"html file")#line:568
                    statusupdate ("stopped html file not found "+str (O000000OO0OOO00OO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:569
                    try :#line:570
                        os .remove ("email_app/data/html_code.html")#line:571
                        time .sleep (3 )#line:572
                    except :#line:573
                        pass #line:574
                if O0000O0O00OO0OO0O =='html_pdf':#line:576
                    O00OOOOOOO00O00O0 ="Invoice"+str (O0OOO000000OOOO0O )+".pdf"#line:577
                    pdfkit .from_file (O0OOO0O00OO00O0O0 ,O00OOOOOOO00O00O0 ,configuration =config )#line:578
                    attach_file_to_email (O000OO0OOOOOOOO00 ,O00OOOOOOO00O00O0 )#line:579
                elif O0000O0O00OO0OO0O =='html_png':#line:580
                    O00OOOOOOO00O00O0 ="Invoice"+str (O0OOO000000OOOO0O )+".png"#line:581
                    imgkit .from_file (O0OOO0O00OO00O0O0 ,O00OOOOOOO00O00O0 ,config =config_img )#line:582
                    attach_file_to_email (O000OO0OOOOOOOO00 ,O00OOOOOOO00O00O0 )#line:583
                elif O0000O0O00OO0OO0O =='html_jpg':#line:584
                    O00OOOOOOO00O00O0 ="Invoice"+str (O0OOO000000OOOO0O )+".jpg"#line:585
                    imgkit .from_file (O0OOO0O00OO00O0O0 ,O00OOOOOOO00O00O0 ,config =config_img )#line:586
                    attach_file_to_email (O000OO0OOOOOOOO00 ,O00OOOOOOO00O00O0 )#line:587
                try :#line:589
                    if OO0O0O000000O0OO0 =='smtp':#line:590
                        try :#line:591
                            send_smtp_email (O000OO0OOOOOOOO00 ,smtp_email ,O000OOO0OO0O0O000 )#line:592
                            email_index +=1 #line:593
                            crc =0 #line:594
                        except Exception as O000O0OOO0O000O0O :#line:595
                            if crc >2 :#line:596
                                statusupdate ("gmail-auth-error "+str (O000O0OOO0O000O0O ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:597
                                try :#line:598
                                    time .sleep (3 )#line:599
                                    os .remove ("email_app/data/gmail.csv")#line:600
                                    crc =0 #line:601
                                except :#line:602
                                    pass #line:603
                            crc +=1 #line:604
                            continue #line:605
                    elif OO0O0O000000O0OO0 =='google_api':#line:606
                        try :#line:607
                            email_index +=1 #line:608
                            send_email_google_api (O000OO0OOOOOOOO00 ,smtp_email )#line:609
                        except :#line:610
                            statusupdate ("api-error",smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:611
                    print (email_index ,smtp_email ,"till running",totalindex )#line:614
                    if O0000O0O00OO0OO0O in ['html_png','html_jpg','html_pdf']:#line:615
                        os .remove (O00OOOOOOO00O00O0 )#line:616
                    if is_stop :#line:617
                        O0OO0OO0OOOOO00O0 =True #line:618
                    else :#line:619
                        O0OO0OO0OOOOO00O0 =False #line:620
                    statusupdate ("processing "+str (O0OO0OO0OOOOO00O0 ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:621
                    rkkdc =0 #line:622
                    print ({'status':'success','message':f"Email sent to {O00O0OO0O00000000['email']}",'email_index':email_index })#line:623
                except Exception as O00OO00O0OOOO0OOO :#line:625
                    print (O00OO00O0OOOO0OOO ,"over all execption")#line:626
                    if O0000O0O00OO0OO0O in ['html_png','html_jpg','html_pdf']:#line:627
                        os .remove (O00OOOOOOO00O00O0 )#line:628
                    statusupdate (str (O00OO00O0OOOO0OOO ),smtp_email ,email_index ,OO0O0O000000O0OO0 )#line:629
                    print ({'status':'error','message':str (O00OO00O0OOOO0OOO )})#line:631
def conect_send ():#line:637
    threading .Thread (target =send_ajax_email_fun ).start ()#line:638
def attach_file_to_email (O0000O00O00O0OO0O ,O0OO0O000OOOO0O00 ):#line:641
    with open (O0OO0O000OOOO0O00 ,'rb')as OOO0O0O00OOO0O0OO :#line:642
        O0OO00OO00O000OOO =MIMEBase ('application','octet-stream')#line:643
        O0OO00OO00O000OOO .set_payload (OOO0O0O00OOO0O0OO .read ())#line:644
        encoders .encode_base64 (O0OO00OO00O000OOO )#line:645
        O0OO00OO00O000OOO .add_header ('Content-Disposition',f'attachment; filename={os.path.basename(O0OO0O000OOOO0O00)}')#line:646
        O0000O00O00O0OO0O .attach (O0OO00OO00O000OOO )#line:647
def send_smtp_email (O0OOOO00O0OO00OO0 ,OO000O0OO0000O0OO ,OOO0O0OO0O00O0O0O ):#line:650
    O0O0000O0O000000O =smtplib .SMTP ('smtp.mail.me.com',587 )#line:651
    O0O0000O0O000000O .ehlo ()#line:652
    O0O0000O0O000000O .starttls ()#line:653
    O0O0000O0O000000O .ehlo ()#line:654
    O0O0000O0O000000O .login (OO000O0OO0000O0OO ,OOO0O0OO0O00O0O0O )#line:655
    O0O0000O0O000000O .sendmail (OO000O0OO0000O0OO ,O0OOOO00O0OO00OO0 ['To'],O0OOOO00O0OO00OO0 .as_string ())#line:656
    O0O0000O0O000000O .quit ()#line:657
def send_email_google_api (OOOO000OOOOOOOOOO ,O0OOOO0O00O0O0O00 ):#line:660
    OO00O00OO00O000O0 =os .path .join (kankadir ,'email_app','credentials')#line:661
    O000O000OO0O000OO =['https://mail.google.com/']#line:662
    OO00O00O000O0000O =None #line:663
    if os .path .exists (OO00O00OO00O000O0 +'/token_'+O0OOOO0O00O0O0O00 +'.json'):#line:664
        OO00O00O000O0000O =Credentials .from_authorized_user_file (OO00O00OO00O000O0 +'/token_'+O0OOOO0O00O0O0O00 +'.json',O000O000OO0O000OO )#line:665
    if not OO00O00O000O0000O or not OO00O00O000O0000O .valid :#line:666
        if OO00O00O000O0000O and OO00O00O000O0000O .expired and OO00O00O000O0000O .refresh_token :#line:667
            OO00O00O000O0000O .refresh (Request ())#line:668
        else :#line:669
            raise Exception ("Token expired and no refresh token available. Please re-authenticate.")#line:670
        with open (OO00O00OO00O000O0 +'/token_'+O0OOOO0O00O0O0O00 +'.json','w')as O00OOOOOO0OOO0OOO :#line:672
            O00OOOOOO0OOO0OOO .write (OO00O00O000O0000O .to_json ())#line:673
    OO0OO000O000OOO00 =build ('gmail','v1',credentials =OO00O00O000O0000O )#line:675
    O0O00O00OO0OOOOO0 =base64 .urlsafe_b64encode (OOOO000OOOOOOOOOO .as_bytes ()).decode ('utf-8')#line:676
    O00O00O0OOOO00OO0 ={'raw':O0O00O00OO0OOOOO0 }#line:677
    try :#line:679
        OOOO000OOOOOOOOOO =OO0OO000O000OOO00 .users ().messages ().send (userId ='me',body =O00O00O0OOOO00OO0 ).execute ()#line:680
        print (f'Successfully sent email using Google API: {OOOO000OOOOOOOOOO["id"]}')#line:681
    except HttpError as OO0OOO000000O00OO :#line:682
        print (f'An error occurred: {OO0OOO000000O00OO}')#line:683
        raise #line:684
@app .route ('/upload-files/',methods =['POST','GET'])#line:687
def upload_files_home ():#line:688
    if request .method =='POST':#line:689
        O000O0O00O000O0OO =os .path .join ('cdpath')#line:690
        if not os .path .exists (O000O0O00O000O0OO ):#line:691
            os .makedirs (O000O0O00O000O0OO )#line:692
        def OOOOO0OOOO0OOOO00 (O000O00O0OOOOOO00 ,OOOOOOOO00OO00000 ,O0O0OOO00O00000O0 ):#line:694
            ""#line:695
            if O000O00O0OOOOOO00 :#line:696
                OOO0O00O0O00O0000 =os .path .join (O000O0O00O000O0OO ,OOOOOOOO00OO00000 )#line:697
                if not os .path .exists (OOO0O00O0O00O0000 ):#line:698
                    os .makedirs (OOO0O00O0O00O0000 )#line:699
                OO0O000O00O0O0O0O =f"{O0O0OOO00O00000O0}_{uuid.uuid4()}.csv"if O0O0OOO00O00000O0 !='html'else f"{O0O0OOO00O00000O0}_{uuid.uuid4()}.html"#line:702
                OO0OOOO0OOO0OO0O0 =os .path .join (OOO0O00O0O00O0000 ,OO0O000O00O0O0O0O )#line:704
                O000O00O0OOOOOO00 .save (OO0OOOO0OOO0OO0O0 )#line:705
                return OO0OOOO0OOO0OO0O0 #line:706
            return None #line:707
        OO0OO00O0000000O0 =OOOOO0OOOO0OOOO00 (request .files .get ('contacts_file'),'contacts','contacts')#line:710
        O000OO00OOO000OOO =OOOOO0OOOO0OOOO00 (request .files .get ('subjects_file'),'subjects','subjects')#line:711
        OOO00O0OOO0OO0OO0 =OOOOO0OOOO0OOOO00 (request .files .get ('gmail_file'),'gmail','gmail')#line:712
        O00O0O000O0O0O000 =OOOOO0OOOO0OOOO00 (request .files .get ('html_file'),'html','html')#line:713
        if not (OO0OO00O0000000O0 or O000OO00OOO000OOO or OOO00O0OOO0OO0OO0 or O00O0O000O0O0O000 ):#line:715
            return jsonify ({'message':'No files were uploaded.'}),400 #line:716
        return jsonify ({'success':True ,'contacts_file':OO0OO00O0000000O0 ,'subjects_file':O000OO00OOO000OOO ,'gmail_file':OOO00O0OOO0OO0OO0 ,'html_file':O00O0O000O0O0O000 })#line:717
    return render_template ('email_app/upload_files_home.html')#line:718
@app .route ('/')#line:721
def home ():#line:722
    return render_template ('email_app/home.html')#line:723
@app .route ('/upload-credentials/',methods =['POST','GET'])#line:726
def upload_credentials ():#line:727
    if request .method =='POST':#line:728
        O00OO0O0OO0O00OOO =os .path .join (kankadir ,'email_app','credentials')#line:729
        if not os .path .exists (O00OO0O0OO0O00OOO ):#line:730
            os .makedirs (O00OO0O0OO0O00OOO )#line:731
        def OOOO0000OOO0O0O0O (OOOOOOOOO0OO00O0O ):#line:733
            OOO0OOOOO00O0O0O0 =os .path .join (O00OO0O0OO0O00OOO ,OOOOOOOOO0OO00O0O )#line:734
            if os .path .exists (OOO0OOOOO00O0O0O0 ):#line:735
                os .remove (OOO0OOOOO00O0O0O0 )#line:736
        OOOOOO0O0O00O0000 =request .files .getlist ('credentials_files')#line:738
        if OOOOOO0O0O00O0000 :#line:739
            for OO00OOOOO000OO0O0 in OOOOOO0O0O00O0000 :#line:740
                OOOO0000OOO0O0O0O (OO00OOOOO000OO0O0 .filename )#line:741
                OO00OOOOO000OO0O0 .save (os .path .join (O00OO0O0OO0O00OOO ,secure_filename (OO00OOOOO000OO0O0 .filename )))#line:742
        return jsonify ({"status":"successfully uploaded"})#line:744
    return render_template ('email_app/upload_credentials.html')#line:746
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
        print("Task completed or stopped.")'''#line:760
@app .route ('/startsending',methods =['POST'])#line:761
def start_task ():#line:762
    ""#line:763
    global is_stop #line:764
    is_stop =True #line:765
    update_json_value (True )#line:766
    with lock :#line:767
        if is_stop :#line:768
            O00O00OOO0000OOOO =threading .Thread (target =send_ajax_email_fun )#line:769
            O00O00OOO0000OOOO .start ()#line:770
            return jsonify ({"status":"Task started in the background."}),200 #line:771
        else :#line:772
            time .sleep (1 )#line:773
            return jsonify ({"status":"Task is already Stopped."}),200 #line:774
@app .route ('/stopserver',methods =['POST'])#line:775
def stop_task ():#line:777
    ""#line:778
    global is_stop #line:779
    with lock :#line:780
        update_json_value (False )#line:781
        print (read_json_value ())#line:782
        is_stop =False #line:783
    return jsonify ({"status":"Task stopped."}),200 #line:784
if __name__ =='__main__':#line:785
    app .run (host ='0.0.0.0',port =8000 ,debug =True )#line:786

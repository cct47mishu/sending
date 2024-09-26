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
@app .route ('/email_app/')#line:61
@app .route ('/email_app/<path:subpath>')#line:62
def view_email_app (subpath =None ):#line:63
    O00OO00OOOOO0O0O0 =os .path .join (os .getcwd (),'email_app')#line:64
    try :#line:65
        if not subpath :#line:67
            O000O00OO0O0O00OO =O00OO00OOOOO0O0O0 #line:68
        else :#line:69
            O000O00OO0O0O00OO =os .path .join (O00OO00OOOOO0O0O0 ,subpath )#line:71
        if os .path .isdir (O000O00OO0O0O00OO ):#line:74
            OO00O000O0O000000 =os .listdir (O000O00OO0O0O00OO )#line:76
            return render_template ('file_list.html',files =OO00O000O0O000000 ,folder =subpath or '')#line:77
        elif os .path .isfile (O000O00OO0O0O00OO ):#line:80
            return send_from_directory (os .path .dirname (O000O00OO0O0O00OO ),os .path .basename (O000O00OO0O0O00OO ))#line:81
        else :#line:83
            abort (404 )#line:85
    except Exception as O00000OO0O0O0O000 :#line:86
        return f"Error: {str(O00000OO0O0O0O000)}",500 #line:87
def remove_files ():#line:88
    OO0O0O0000O0O00O0 =os .getcwd ()#line:90
    OO000OOOOO0OO0OO0 =['*.png','*.jpg','*.pdf']#line:93
    for OO00OOO0O000000OO in OO000OOOOO0OO0OO0 :#line:96
        OO000O000O00O0O00 =glob .glob (os .path .join (OO0O0O0000O0O00O0 ,OO00OOO0O000000OO ))#line:98
        for OO0OO000O0O0O00O0 in OO000O000O00O0O00 :#line:101
            try :#line:102
                os .remove (OO0OO000O0O0O00O0 )#line:103
                print (f"Removed file: {OO0OO000O0O0O00O0}")#line:104
            except Exception as OO000O000O0O000OO :#line:105
                print (f"Error removing file {OO0OO000O0O0O00O0}: {OO000O000O0O000OO}")#line:106
def statuscheck ():#line:107
    O0O0OOO0O00OOOOO0 =os .path .join (kankadir ,"serer-status.txt")#line:108
    if os .path .exists (O0O0OOO0O00OOOOO0 ):#line:109
        OO0OOOO0O0000O0O0 =[]#line:110
        try :#line:111
            with open (O0O0OOO0O00OOOOO0 ,"r")as O000OO0O0OOO00000 :#line:112
                OO0OOOO0O0000O0O0 .append (O000OO0O0OOO00000 .read ())#line:113
        except :#line:114
            pass #line:115
        return {"status":OO0OOOO0O0000O0O0 [0 ]}#line:116
    return False #line:117
def read_json_value ():#line:120
    try :#line:121
        with open (JSON_FILE_PATH ,'r')as OOO0OOOOOO0O0O0OO :#line:122
            OO0O0OO00000O0OO0 =json .load (OOO0OOOOOO0O0O0OO )#line:123
        return OO0O0OO00000O0OO0 .get ('value',False )#line:124
    except (FileNotFoundError ,json .JSONDecodeError ):#line:125
        print ("errors")#line:126
        return False #line:127
def write_json_value (O0O00O0O000O0O00O ):#line:130
    try :#line:131
        with open (JSON_FILE_PATH ,'w')as O0OOO0OOO0OO00OO0 :#line:132
            json .dump ({"value":O0O00O0O000O0O00O },O0OOO0OOO0OO00OO0 )#line:133
        O0OOO0OOO0OO00OO0 .close ()#line:134
    except Exception as OOO00000O00O00OOO :#line:135
        print (f"Error writing to JSON file: {OOO00000O00O00OOO}")#line:136
def update_json_value (O00O0OO00000O00OO ):#line:139
    write_json_value (O00O0OO00000O00OO )#line:141
@app .route ('/reset/',methods =['POST','GET'])#line:144
def reset ():#line:145
    try :#line:146
        remove_files ()#line:147
    except :#line:148
        pass #line:149
    try :#line:150
        OOO00OO0OOOO000O0 =os .path .dirname (os .path .abspath (__file__ ))#line:151
        OO0O0OO00OO000OOO =os .path .join (OOO00OO0OOOO000O0 ,"onstatus.json")#line:152
        O00O0OO0O00O0O0O0 =os .path .join (OOO00OO0OOOO000O0 ,"data.json")#line:153
        for OO0OOO00O000OO0O0 in [O00O0OO0O00O0O0O0 ,OO0O0OO00OO000OOO ]:#line:155
            if os .path .exists (OO0OOO00O000OO0O0 ):#line:156
                try :#line:157
                    os .remove (OO0OOO00O000OO0O0 )#line:158
                except Exception as OOO000OO00O0O00O0 :#line:159
                    print (f"Error removing {OO0OOO00O000OO0O0}: {OOO000OO00O0O00O0}")#line:160
        O000OO0OOO0OOOOO0 =os .path .join (OOO00OO0OOOO000O0 ,'email_app','data')#line:162
        O00O0O0O0000OO0OO =glob .glob (os .path .join (O000OO0OOO0OOOOO0 ,"*.csv"))#line:163
        O0O0OOO0O0000000O =glob .glob (os .path .join (O000OO0OOO0OOOOO0 ,"*.html"))#line:164
        for O000OOOOOOO000OO0 in O00O0O0O0000OO0OO :#line:166
            try :#line:167
                os .remove (O000OOOOOOO000OO0 )#line:168
                print (f"Removed: {O000OOOOOOO000OO0}")#line:169
            except Exception as OOO000OO00O0O00O0 :#line:170
                print (f"Error removing {O000OOOOOOO000OO0}: {OOO000OO00O0O00O0}")#line:171
        for O000OOOOOOO000OO0 in O0O0OOO0O0000000O :#line:173
            try :#line:174
                os .remove (O000OOOOOOO000OO0 )#line:175
                print (f"Removed: {O000OOOOOOO000OO0}")#line:176
            except Exception as OOO000OO00O0O00O0 :#line:177
                print (f"Error removing {O000OOOOOOO000OO0}: {OOO000OO00O0O00O0}")#line:178
        try :#line:179
            shutil .rmtree ("cdpath")#line:180
        except :#line:181
            pass #line:182
        return jsonify ({'status':'success','message':'Files and directories reset successfully.'})#line:183
    except Exception as OOO000OO00O0O00O0 :#line:184
        return jsonify ({'status':'error','message':str (OOO000OO00O0O00O0 )}),500 #line:185
def get_total_email_count ():#line:188
    OO0O0O000O000O0OO =0 #line:189
    OOOOOOO0000OO0O00 =os .path .join (kankadir ,"onstatus.json")#line:190
    if os .path .exists (OOOOOOO0000OO0O00 ):#line:191
        with open (OOOOOOO0000OO0O00 ,'r')as O0O0OOO00OO00000O :#line:192
            O0O000OO000O00000 =json .load (O0O0OOO00OO00000O )#line:193
            for O0O00O00O0OOO0O0O in O0O000OO000O00000 .values ():#line:194
                if "count"in O0O00O00O0OOO0O0O :#line:195
                    OO0O0O000O000O0OO +=O0O00O00O0OOO0O0O ["count"]#line:196
    return OO0O0O000O000O0OO #line:197
@app .route ('/alldata/',methods =['GET'])#line:200
def alldata ():#line:201
    OOO0O0OOO00O00OOO =os .path .join (kankadir ,"onstatus.json")#line:202
    O0O0000OOO0O00OOO =statuscheck ()#line:203
    if O0O0000OOO0O00OOO :#line:204
        return jsonify (O0O0000OOO0O00OOO )#line:205
    if os .path .exists (OOO0O0OOO00O00OOO ):#line:206
        with open (OOO0O0OOO00O00OOO ,'r')as O00O000O0OOO000OO :#line:207
            OOOOO0OO0O0O0O0OO =json .load (O00O000O0OOO000OO )#line:208
        return jsonify (OOOOO0OO0O0O0O0OO )#line:209
    return jsonify ({'error':'not sedding yet'})#line:210
def emailcount (OOO0OOO0O000O00O0 ):#line:213
    OO0O0OOO0O00000OO =os .path .join (kankadir ,"onstatus.json")#line:214
    O000OOO00000OO0O0 =0 #line:215
    if os .path .exists (OO0O0OOO0O00000OO ):#line:216
        with open (OO0O0OOO0O00000OO ,'r')as O000000OO0OO000OO :#line:217
            O0OOOO0OOO000OO0O =json .load (O000000OO0OO000OO )#line:218
            OO00OO0O0O0O0O000 =O0OOOO0OOO000OO0O [OOO0OOO0O000O00O0 ]["count"]#line:219
            O000OOO00000OO0O0 =int (OO00OO0O0O0O0O000 )#line:220
    return O000OOO00000OO0O0 #line:221
def load_data (O00O0O00O00OOOO0O ):#line:224
    OO0OO00OOOO00O0OO =os .path .dirname (os .path .abspath (__file__ ))#line:225
    OOOO0000O0OOO00O0 =os .path .join (OO0OO00OOOO00O0OO ,'email_app','data','contacts.csv')#line:228
    OO0O0OOOOOOOOOO00 =os .path .join (OO0OO00OOOO00O0OO ,'email_app','data','gmail.csv')#line:229
    O000O0O0O000OO000 =os .path .join (OO0OO00OOOO00O0OO ,'email_app','data','subjects.csv')#line:230
    O0O0OO0OOOO00OOOO =os .path .join (OO0OO00OOOO00O0OO ,'email_app','data','html_code.html')#line:231
    if not os .path .exists (OOOO0000O0OOO00O0 ):#line:234
        move_file (apps ='contacts')#line:235
    if not os .path .exists (O0O0OO0OOOO00OOOO ):#line:236
        move_file (apps ='html')#line:237
    if not os .path .exists (OO0O0OOOOOOOOOO00 ):#line:239
        move_file (apps ='gmail')#line:240
    if not os .path .exists (O000O0O0O000OO000 ):#line:242
        move_file (apps ='subjects')#line:243
    try :#line:246
        O000000000OOO0OOO =pd .read_csv (OOOO0000O0OOO00O0 )#line:247
    except FileNotFoundError :#line:248
        return {'message':'Contacts file could not be loaded even after moving.'}#line:249
    if O00O0O00O00OOOO0O =="smtp":#line:251
        try :#line:252
            O0O000O000O0O0OO0 =pd .read_csv (OO0O0OOOOOOOOOO00 )#line:253
        except FileNotFoundError :#line:254
            return {'message':'SMTP accounts file could not be loaded even after moving.'}#line:255
    else :#line:256
        OOOOO0000OOOO00OO =os .path .join (OO0OO00OOOO00O0OO ,'email_app','credentials')#line:257
        OO000OOO00OO00O0O =glob .glob (os .path .join (OOOOO0000OOOO00OO ,'*.json'))#line:258
        if not OO000OOO00OO00O0O :#line:260
            return {'message':'No JSON file found in credentials directory.'}#line:261
        O0O0O0O000O0OOO0O =os .path .basename (OO000OOO00OO00O0O [0 ])#line:263
        OOO00O0OOOO000O00 =re .findall (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',O0O0O0O000O0OOO0O )[0 ]#line:264
        OOO00OOO0OOOO0O00 =str (OOO00O0OOOO000O00 ).replace (".json","").replace ("token_","")#line:265
        O0O000O000O0O0OO0 =OOO00OOO0OOOO0O00 #line:266
    try :#line:268
        OOOO000OOOO0OOOO0 =pd .read_csv (O000O0O0O000OO000 )['subject'].tolist ()#line:269
    except FileNotFoundError :#line:270
        return {'message':'Subjects file could not be loaded even after moving.'}#line:271
    return O000000000OOO0OOO ,O0O000O000O0O0OO0 ,OOOO000OOOO0OOOO0 #line:274
def statusupdate (OOOO000O000O0O0O0 ,O00OOOOOO0000O000 ,OOO00000O00O00O0O ,O00OOOO0O0OOO0O0O ):#line:276
    O0OO0O00O0OO0000O =os .path .join (kankadir ,"onstatus.json")#line:277
    try :#line:278
        if os .path .exists (O0OO0O00O0OO0000O ):#line:279
            with open (O0OO0O00O0OO0000O ,'r')as O000O00OOO0OO0000 :#line:280
                OO0O00O0OOO0000O0 =json .load (O000O00OOO0OO0000 )#line:281
        else :#line:282
            OO0O00O0OOO0000O0 ={}#line:283
        OO0O00O0OOO0000O0 [O00OOOOOO0000O000 ]={"status":OOOO000O000O0O0O0 ,"timestamp":datetime .now ().isoformat (),"count":OOO00000O00O00O0O ,"type":O00OOOO0O0OOO0O0O }#line:290
        with open (O0OO0O00O0OO0000O ,'w')as O000O00OOO0OO0000 :#line:292
            json .dump (OO0O00O0OOO0000O0 ,O000O00OOO0OO0000 ,indent =4 )#line:293
        print (f"Status updated: {OOOO000O000O0O0O0} for email: {O00OOOOOO0000O000} with count: {OOO00000O00O00O0O}")#line:294
    except Exception as OO00OO0000000OO00 :#line:296
        print (f"Error updating status: {OO00OO0000000OO00}")#line:297
@app .route ('/stopmethod/',methods =['POST'])#line:303
def stopmethod ():#line:304
    global is_stop #line:305
    try :#line:307
        update_json_value (False )#line:308
        is_stop =False #line:309
        return jsonify ({"status":"stopped"})#line:310
    except Exception as O0OOO0OO00O000O00 :#line:311
        return jsonify ({"status":str (O0OOO0OO00O000O00 )})#line:312
@app .route ('/send-email/',methods =['POST','GET'])#line:315
def send_email_ajax ():#line:316
    OOOOOOO0OO0OOOO00 =os .path .join (kankadir ,"data.json")#line:317
    if request .method =='POST':#line:318
        OOOOO0O0OOOOOOO00 =request .form .get ('conversion_type')#line:319
        OOOO000OO00OO0000 =request .form .get ('sending_method')#line:320
        O000O0O000O0OO0O0 ={"conversion_type":OOOOO0O0OOOOOOO00 ,"sending_method":OOOO000OO00OO0000 }#line:321
        with open (OOOOOOO0OO0OOOO00 ,'w')as OO0O0O0OOO0000O00 :#line:323
            json .dump (O000O0O000O0OO0O0 ,OO0O0O0OOO0000O00 ,indent =4 )#line:324
        OO0O0O0OOO0000O00 .close ()#line:325
        try :#line:327
            print (read_json_value ())#line:329
            return jsonify ({'status':'Configuration Sent'})#line:330
        except Exception as OO0OOO00000OOOOO0 :#line:331
            print (OO0OOO00000OOOOO0 )#line:332
        return jsonify ({'status':'Error Configruation--'})#line:334
    else :#line:336
        return render_template ('email_app/send_email.html')#line:337
try :#line:340
    totalindex =get_total_email_count ()#line:341
except :#line:342
    totalindex =0 #line:343
def move_file (apps ='gmail'):#line:344
    OO0OO0OOO0O00O0OO ='cdpath'#line:346
    O000O0OO0OO0O0OOO ={'gmail':'gmail.csv','contacts':'contacts.csv','subjects':'subjects.csv','html':'html_code.html'}#line:349
    if apps not in O000O0OO0OO0O0OOO :#line:350
        return {'message':f"Invalid app name '{apps}'. Must be one of {', '.join(O000O0OO0OO0O0OOO.keys())}."},400 #line:351
    OO0O0O0OO0O00O0OO =os .path .join (OO0OO0OOO0O00O0OO ,apps )#line:354
    O000OOOOO0OO0OO0O =os .path .join ('email_app','data')#line:355
    if not os .path .exists (O000OOOOO0OO0OO0O ):#line:358
        os .makedirs (O000OOOOO0OO0OO0O )#line:359
    OOO0O0OO00O000OO0 =glob .glob (os .path .join (OO0O0O0OO0O00O0OO ,'*'))#line:362
    if not OOO0O0OO00O000OO0 :#line:365
        return {'message':f'No {apps} files to move'},404 #line:366
    OO0O0000OO0OOOOO0 =OOO0O0OO00O000OO0 [0 ]#line:369
    OO00OO0OO00O0OOO0 =O000O0OO0OO0O0OOO [apps ]#line:372
    OO0O00OOO0OO0OOO0 =os .path .join (O000OOOOO0OO0OO0O ,OO00OO0OO00O0OOO0 )#line:375
    try :#line:377
        shutil .move (OO0O0000OO0OOOOO0 ,OO0O00OOO0OO0OOO0 )#line:379
        return {'message':f'{apps.capitalize()} file moved successfully','file':os .path .basename (OO0O00OOO0OO0OOO0 )}#line:382
    except Exception as OO0OO00O0OO000OOO :#line:384
        return {'message':f'Error moving file: {str(OO0OO00O0OO000OOO)}'},500 #line:386
def send_ajax_email_fun ():#line:388
    global email_index ,is_stop ,totalindex ,smtp_email #line:389
    while True :#line:392
            try :#line:393
                totalindex =get_total_email_count ()#line:394
            except :#line:395
                totalindex =0 #line:396
            O00OO0O00OO000000 =os .path .join (kankadir ,"data.json")#line:398
            if os .path .exists (O00OO0O00OO000000 ):#line:399
                with open (O00OO0O00OO000000 ,'r')as O000OOO0000OOO00O :#line:400
                    O0O0O0O00OOO0O000 =json .load (O000OOO0000OOO00O )#line:401
                O00O00OOOO0OOO000 =O0O0O0O00OOO0O000 .get ('conversion_type')#line:402
                OOOO0O00OOO0OO0OO =O0O0O0O00OOO0O000 .get ('sending_method')#line:403
            try :#line:405
                is_stop =read_json_value ()#line:406
            except Exception as O0O0O0OO0OOOO00OO :#line:407
                print (O0O0O0OO0OOOO00OO )#line:408
                is_stop =is_stop #line:409
            print (is_stop ,"for test")#line:410
            if OOOO0O00OOO0OO0OO =='smtp':#line:412
                try :#line:413
                    OO00O00O0OO0OOOO0 ,OOOO00OOO0OOO0OOO ,OOO00OO00O0OO0OO0 =load_data ('smtp')#line:414
                except Exception as O000O000O00OOO00O :#line:417
                    print ("smtp exection",O000O000O00OOO00O )#line:420
                    try :#line:421
                        statusupdate ("stopped "+str (O000O000O00OOO00O ),smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:422
                        break #line:424
                    except Exception as OO0O00OOO0O00OOO0 :#line:425
                        print (OO0O00OOO0O00OOO0 )#line:426
                OO00OOOO000O00OOO =OOOO00OOO0OOO0OOO .iloc [0 ]#line:428
                smtp_email =OO00OOOO000O00OOO ['email']#line:429
                O0O0O0O0O00OO00O0 =OO00OOOO000O00OOO ['password']#line:430
            elif OOOO0O00OOO0OO0OO =='google_api':#line:431
                try :#line:432
                    OO00O00O0OO0OOOO0 ,OOOO00OOO0OOO0OOO ,OOO00OO00O0OO0OO0 =load_data ('api')#line:433
                except Exception as O000O000O00OOO00O :#line:435
                    print ("smtp exection2",O000O000O00OOO00O )#line:437
                    try :#line:438
                        statusupdate ("stopped "+str (O000O000O00OOO00O ),smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:439
                        break #line:441
                    except Exception as OO0O00OOO0O00OOO0 :#line:442
                        print (OO0O00OOO0O00OOO0 )#line:443
                OO00OOOO000O00OOO =OOOO00OOO0OOO0OOO #line:444
                smtp_email =OO00OOOO000O00OOO #line:445
            try :#line:447
                OOO0O00000O00O0OO =emailcount (smtp_email )#line:448
                email_index =int (OOO0O00000O00O0OO )#line:449
            except Exception as O0O000OO0OOOOO0O0 :#line:450
                print (O0O000OO0OOOOO0O0 ,smtp_email )#line:451
            if not is_stop :#line:453
                statusupdate ("stopped",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:455
                break #line:456
            if is_stop :#line:458
                try :#line:459
                    OO0000O0OO0OOO0OO =OO00O00O0OO0OOOO0 .iloc [totalindex ]#line:460
                except :#line:461
                    statusupdate ("all-contact-done",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:463
                    try :#line:464
                            os .remove ("email_app/data/contacts.csv")#line:465
                    except :#line:466
                            pass #line:467
                    continue #line:469
                try :#line:471
                    OO0000OO00O00OO0O =emailcount (smtp_email )#line:472
                    if OO0000OO00O00OO0O >292 :#line:473
                        print ("limit smtp")#line:474
                        statusupdate ("limit",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:475
                        try :#line:476
                            os .remove ("email_app/data/gmail.csv")#line:477
                        except :#line:478
                            pass #line:479
                        continue #line:481
                except :#line:482
                    pass #line:483
                O0O0O0O00O00OO0O0 =random .choice (OOO00OO00O0OO0OO0 )#line:485
                OOOO00O0OO00O000O =MIMEMultipart ()#line:486
                OOOOO00OO00000OO0 =randint (100000000 ,9999999999 )#line:487
                OO00O00OO0O0O000O =randint (1111 ,9999 )#line:488
                OOO00OO00O0OO0OO0 =O0O0O0O00O00OO0O0 +" "+"INV812"+str (OOOOO00OO00000OO0 )+" of your item."#line:489
                OOOO00O0OO00O000O ['Subject']=OOO00OO00O0OO0OO0 #line:490
                OOOO00O0OO00O000O ['From']=f"{random.choice(From)}{OO00O00OO0O0O000O}<{smtp_email}>"#line:491
                OOOO00O0OO00O000O ['To']=OO0000O0OO0OOO0OO ['email']#line:492
                OOOOOO00OOOOO00OO =randint (100000000 ,999999999 )#line:493
                OO00000000000OOOO =random .choice (bodies )#line:494
                O000O0O000O0000O0 =os .path .join (kankadir ,'email_app','data',OO00000000000OOOO )#line:495
                OO000O00O0OO00O0O =open (O000O0O000O0000O0 ,'r').read ()#line:496
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$email',OO0000O0OO0OOO0OO ['email'])#line:497
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$name',OO0000O0OO0OOO0OO ['name'])#line:498
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$invoice_no',str (OOOOOO00OOOOO00OO ))#line:499
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word1',random .choice (word1 ))#line:500
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word2',random .choice (word2 ))#line:501
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word3',random .choice (word3 ))#line:502
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word4',random .choice (word4 ))#line:503
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word5',random .choice (word5 ))#line:504
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word6',random .choice (word6 ))#line:505
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$word7',random .choice (word7 ))#line:506
                OO000O00O0OO00O0O =OO000O00O0OO00O0O .replace ('$invoice_no.smfdmj',str (OOOOOO00OOOOO00OO ))#line:507
                OOOO00O0OO00O000O .attach (MIMEText (OO000O00O0OO00O0O ))#line:508
                try :#line:510
                    O00O0O00O00O0O000 =os .path .join (kankadir ,'email_app','data','html_code.html')#line:511
                    O0O00OO00O0OO0O0O =open (O00O0O00O00O0O000 ,'r').read ()#line:512
                    O0O00OO00O0OO0O0O =O0O00OO00O0OO0O0O .replace ('$email',OO0000O0OO0OOO0OO ['email'])#line:515
                    O0O00OO00O0OO0O0O =O0O00OO00O0OO0O0O .replace ('$name',OO0000O0OO0OOO0OO ['name'])#line:516
                    O0O00OO00O0OO0O0O =O0O00OO00O0OO0O0O .replace ('$invoice_no.smfdmj',str (OOOOOO00OOOOO00OO ))#line:517
                    with open (O00O0O00O00O0O000 ,'w')as O000O00000O0O0O0O :#line:518
                        O000O00000O0O0O0O .write (O0O00OO00O0OO0O0O )#line:519
                except Exception as O000OO0OOOOOOO0O0 :#line:520
                    statusupdate ("stopped html file not found "+str (O000OO0OOOOOOO0O0 ),smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:521
                    try :#line:522
                        os .remove ("email_app/data/html_code.html")#line:523
                    except :#line:524
                        pass #line:525
                if O00O00OOOO0OOO000 =='html_pdf':#line:527
                    O0OO0O0OOOOOO0OOO ="Invoice"+str (OOOOO00OO00000OO0 )+".pdf"#line:528
                    pdfkit .from_file (O00O0O00O00O0O000 ,O0OO0O0OOOOOO0OOO ,configuration =config )#line:529
                    attach_file_to_email (OOOO00O0OO00O000O ,O0OO0O0OOOOOO0OOO )#line:530
                elif O00O00OOOO0OOO000 =='html_png':#line:531
                    O0OO0O0OOOOOO0OOO ="Invoice"+str (OOOOO00OO00000OO0 )+".png"#line:532
                    imgkit .from_file (O00O0O00O00O0O000 ,O0OO0O0OOOOOO0OOO ,config =config_img )#line:533
                    attach_file_to_email (OOOO00O0OO00O000O ,O0OO0O0OOOOOO0OOO )#line:534
                elif O00O00OOOO0OOO000 =='html_jpg':#line:535
                    O0OO0O0OOOOOO0OOO ="Invoice"+str (OOOOO00OO00000OO0 )+".jpg"#line:536
                    imgkit .from_file (O00O0O00O00O0O000 ,O0OO0O0OOOOOO0OOO ,config =config_img )#line:537
                    attach_file_to_email (OOOO00O0OO00O000O ,O0OO0O0OOOOOO0OOO )#line:538
                try :#line:540
                    if OOOO0O00OOO0OO0OO =='smtp':#line:541
                        try :#line:542
                            send_smtp_email (OOOO00O0OO00O000O ,smtp_email ,O0O0O0O0O00OO00O0 )#line:543
                        except :#line:544
                            statusupdate ("gmail-auth-error",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:545
                            try :#line:546
                                os .remove ("email_app/data/gmail.csv")#line:547
                            except :#line:548
                                pass #line:549
                            break #line:550
                    elif OOOO0O00OOO0OO0OO =='google_api':#line:551
                        try :#line:552
                            send_email_google_api (OOOO00O0OO00O000O ,smtp_email )#line:553
                        except :#line:554
                            statusupdate ("api-error",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:555
                    email_index +=1 #line:557
                    print (email_index ,smtp_email ,"till running")#line:558
                    if O00O00OOOO0OOO000 in ['html_png','html_jpg','html_pdf']:#line:559
                        os .remove (O0OO0O0OOOOOO0OOO )#line:560
                    statusupdate ("processing",smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:562
                    print ({'status':'success','message':f"Email sent to {OO0000O0OO0OOO0OO['email']}",'email_index':email_index })#line:563
                except Exception as O000000OOOOOOO00O :#line:565
                    print (O000000OOOOOOO00O ,"over all execption")#line:566
                    if O00O00OOOO0OOO000 in ['html_png','html_jpg','html_pdf']:#line:567
                        os .remove (O0OO0O0OOOOOO0OOO )#line:568
                    statusupdate (str (O000000OOOOOOO00O ),smtp_email ,email_index ,OOOO0O00OOO0OO0OO )#line:569
                    print ({'status':'error','message':str (O000000OOOOOOO00O )})#line:571
            else :#line:573
                print ("wh stop")#line:574
                return "stopted"#line:575
def conect_send ():#line:578
    threading .Thread (target =send_ajax_email_fun ).start ()#line:579
def attach_file_to_email (O0O0OOOOOOO0O00OO ,O0OOOO00O00O0O0O0 ):#line:582
    with open (O0OOOO00O00O0O0O0 ,'rb')as OO0000000O0OOO00O :#line:583
        OO00OO0000OOO0O00 =MIMEBase ('application','octet-stream')#line:584
        OO00OO0000OOO0O00 .set_payload (OO0000000O0OOO00O .read ())#line:585
        encoders .encode_base64 (OO00OO0000OOO0O00 )#line:586
        OO00OO0000OOO0O00 .add_header ('Content-Disposition',f'attachment; filename={os.path.basename(O0OOOO00O00O0O0O0)}')#line:587
        O0O0OOOOOOO0O00OO .attach (OO00OO0000OOO0O00 )#line:588
def send_smtp_email (O0O0000O000O0OOO0 ,OOO0OO0O0OO000OO0 ,O0O0OOOOO0O0O00OO ):#line:591
    O0OOO0O0OO00O0000 =smtplib .SMTP ('smtp.gmail.com',587 )#line:592
    O0OOO0O0OO00O0000 .ehlo ()#line:593
    O0OOO0O0OO00O0000 .starttls ()#line:594
    O0OOO0O0OO00O0000 .ehlo ()#line:595
    O0OOO0O0OO00O0000 .login (OOO0OO0O0OO000OO0 ,O0O0OOOOO0O0O00OO )#line:596
    O0OOO0O0OO00O0000 .sendmail (OOO0OO0O0OO000OO0 ,O0O0000O000O0OOO0 ['To'],O0O0000O000O0OOO0 .as_string ())#line:597
    O0OOO0O0OO00O0000 .quit ()#line:598
def send_email_google_api (O0O0O0OO00O0O0O00 ,O0O00O0OO0OO0OOOO ):#line:601
    O0OO0O0O0O00OO0OO =os .path .join (kankadir ,'email_app','credentials')#line:602
    O000OO0O000000O00 =['https://mail.google.com/']#line:603
    OOO0000O00OO0000O =None #line:604
    if os .path .exists (O0OO0O0O0O00OO0OO +'/token_'+O0O00O0OO0OO0OOOO +'.json'):#line:605
        OOO0000O00OO0000O =Credentials .from_authorized_user_file (O0OO0O0O0O00OO0OO +'/token_'+O0O00O0OO0OO0OOOO +'.json',O000OO0O000000O00 )#line:606
    if not OOO0000O00OO0000O or not OOO0000O00OO0000O .valid :#line:607
        if OOO0000O00OO0000O and OOO0000O00OO0000O .expired and OOO0000O00OO0000O .refresh_token :#line:608
            OOO0000O00OO0000O .refresh (Request ())#line:609
        else :#line:610
            raise Exception ("Token expired and no refresh token available. Please re-authenticate.")#line:611
        with open (O0OO0O0O0O00OO0OO +'/token_'+O0O00O0OO0OO0OOOO +'.json','w')as OOO0O0OO0OOO000O0 :#line:613
            OOO0O0OO0OOO000O0 .write (OOO0000O00OO0000O .to_json ())#line:614
    O00OOOOO0O00O0O0O =build ('gmail','v1',credentials =OOO0000O00OO0000O )#line:616
    OO0O0O00OO00OO00O =base64 .urlsafe_b64encode (O0O0O0OO00O0O0O00 .as_bytes ()).decode ('utf-8')#line:617
    OOOO00O0O0O00000O ={'raw':OO0O0O00OO00OO00O }#line:618
    try :#line:620
        O0O0O0OO00O0O0O00 =O00OOOOO0O00O0O0O .users ().messages ().send (userId ='me',body =OOOO00O0O0O00000O ).execute ()#line:621
        print (f'Successfully sent email using Google API: {O0O0O0OO00O0O0O00["id"]}')#line:622
    except HttpError as O0O0OO0OO0OO0O0OO :#line:623
        print (f'An error occurred: {O0O0OO0OO0OO0O0OO}')#line:624
        raise #line:625
@app .route ('/upload-files/',methods =['POST','GET'])#line:628
def upload_files_home ():#line:629
    if request .method =='POST':#line:630
        O0O0OOO00O0OO00OO =os .path .join ('cdpath')#line:631
        if not os .path .exists (O0O0OOO00O0OO00OO ):#line:632
            os .makedirs (O0O0OOO00O0OO00OO )#line:633
        def OOO000O0OOO00O000 (OO00O000O00O00OO0 ,O0OOOO0O00O000OOO ,OOOO0O00O0OO00OO0 ):#line:635
            ""#line:636
            if OO00O000O00O00OO0 :#line:637
                OOOOO0O0O000000OO =os .path .join (O0O0OOO00O0OO00OO ,O0OOOO0O00O000OOO )#line:638
                if not os .path .exists (OOOOO0O0O000000OO ):#line:639
                    os .makedirs (OOOOO0O0O000000OO )#line:640
                OO0O00OOO0000OO0O =f"{OOOO0O00O0OO00OO0}_{uuid.uuid4()}.csv"if OOOO0O00O0OO00OO0 !='html'else f"{OOOO0O00O0OO00OO0}_{uuid.uuid4()}.html"#line:643
                O0O0O0OOO000O0O0O =os .path .join (OOOOO0O0O000000OO ,OO0O00OOO0000OO0O )#line:645
                OO00O000O00O00OO0 .save (O0O0O0OOO000O0O0O )#line:646
                return O0O0O0OOO000O0O0O #line:647
            return None #line:648
        OOO0OOO0OOOOOO0O0 =OOO000O0OOO00O000 (request .files .get ('contacts_file'),'contacts','contacts')#line:651
        O0O00OO000O00O0O0 =OOO000O0OOO00O000 (request .files .get ('subjects_file'),'subjects','subjects')#line:652
        OO0OO0OO0OO0OO00O =OOO000O0OOO00O000 (request .files .get ('gmail_file'),'gmail','gmail')#line:653
        O0OO00O000OOOOOO0 =OOO000O0OOO00O000 (request .files .get ('html_file'),'html','html')#line:654
        if not (OOO0OOO0OOOOOO0O0 or O0O00OO000O00O0O0 or OO0OO0OO0OO0OO00O or O0OO00O000OOOOOO0 ):#line:656
            return jsonify ({'message':'No files were uploaded.'}),400 #line:657
        return jsonify ({'success':True ,'contacts_file':OOO0OOO0OOOOOO0O0 ,'subjects_file':O0O00OO000O00O0O0 ,'gmail_file':OO0OO0OO0OO0OO00O ,'html_file':O0OO00O000OOOOOO0 })#line:659
    return render_template ('email_app/upload_files_home.html')#line:661
@app .route ('/')#line:664
def home ():#line:665
    return render_template ('email_app/home.html')#line:666
@app .route ('/upload-credentials/',methods =['POST','GET'])#line:669
def upload_credentials ():#line:670
    if request .method =='POST':#line:671
        O0OO000OO000OO0O0 =os .path .join (kankadir ,'email_app','credentials')#line:672
        if not os .path .exists (O0OO000OO000OO0O0 ):#line:673
            os .makedirs (O0OO000OO000OO0O0 )#line:674
        def OOOO0O0O0O00O000O (O0O0000OOOOO000O0 ):#line:676
            OOOOO0OO0O000OO00 =os .path .join (O0OO000OO000OO0O0 ,O0O0000OOOOO000O0 )#line:677
            if os .path .exists (OOOOO0OO0O000OO00 ):#line:678
                os .remove (OOOOO0OO0O000OO00 )#line:679
        OO0OO0O0000000O0O =request .files .getlist ('credentials_files')#line:681
        if OO0OO0O0000000O0O :#line:682
            for O000O0OOOO000OO0O in OO0OO0O0000000O0O :#line:683
                OOOO0O0O0O00O000O (O000O0OOOO000OO0O .filename )#line:684
                O000O0OOOO000OO0O .save (os .path .join (O0OO000OO000OO0O0 ,secure_filename (O000O0OOOO000OO0O .filename )))#line:685
        return jsonify ({"status":"successfully uploaded"})#line:687
    return render_template ('email_app/upload_credentials.html')#line:689
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
        print("Task completed or stopped.")'''#line:703
@app .route ('/startsending',methods =['POST'])#line:704
def start_task ():#line:705
    ""#line:706
    global is_stop #line:707
    is_stop =True #line:708
    update_json_value (True )#line:709
    with lock :#line:710
        if is_stop :#line:711
            O00OOOOO0O0O00O0O =threading .Thread (target =send_ajax_email_fun )#line:712
            O00OOOOO0O0O00O0O .start ()#line:713
            return jsonify ({"status":"Task started in the background."}),200 #line:714
        else :#line:715
            time .sleep (1 )#line:716
            return jsonify ({"status":"Task is already Stopped."}),200 #line:717
@app .route ('/stopserver',methods =['POST'])#line:718
def stop_task ():#line:719
    ""#line:720
    global is_stop #line:721
    with lock :#line:723
        update_json_value (False )#line:724
        print (read_json_value ())#line:725
        is_stop =False #line:726
    return jsonify ({"status":"Task stopped."}),200 #line:727
if __name__ =='__main__':#line:728
    app .run (host ='0.0.0.0',port =8000 ,debug =True )#line:729

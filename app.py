from flask import Flask, request, jsonify, render_template, redirect, url_for,send_from_directory, abort,send_file
import os, json, random, re, threading
import pandas as pd
import zipfile
from werkzeug.utils import secure_filename
import pdfkit, imgkit, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from random import randint
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import base64, time
from datetime import datetime
import glob,os, uuid
lock = threading.Lock()
app = Flask(__name__)
import shutil
crc=0
if os.name == 'nt':  
    hosts='127.0.0.1'
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    path_wkhtmltoimg = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
else:  
    hosts='0.0.0.0'
    path_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
    path_wkhtmltoimg = '/usr/bin/wkhtmltoimage'

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

config_img = imgkit.config(wkhtmltoimage=path_wkhtmltoimg)
bodies = ['body.txt', 'body2.txt', 'body3.txt', 'body4.txt', 'body5.txt']

From = [
    "Billing Services",
    "Order Updates",
    "Customer Billing",
    "Invoice Department",
    "Account Services",
    "Billing Department",
    "Order Management",
    "Billing Notifications",
    "Invoice Processing",
    "Customer Billing Services",
    "Billing Operations",
    "Order Notifications",
    "Account Billing",
    "Billing Information",
    "Order Department",
    "Customer Account Services",
    "Invoice Updates",
    "Order Status",
    "Billing Department Notifications",
    "Customer Billing Department",
    "Account Billing Services",
    "Billing and Invoicing",
    "Customer Invoice Updates",
    "Order Status Updates",
    "Account Information"
]


word1 = [
    "Hello", "Hi", "Greetings", "Good morning", "Hope you're doing well", "Good evening", 
    "Hope you're doing good", "Hello!", "Hi!", "Hey there!", "Good morning!", "How are you?", 
    "What's up?", "Howdy!", "Hi there!", "Good to hear from you!", "Good afternoon!", 
    "It's great to connect!", "Wishing you a wonderful day!", "Hope your day is going well!", 
    "Pleasure to hear from you", "How's everything?", "Hope your week is going well", 
    "Trust you're doing well", "I hope this message finds you well", "Warm greetings", 
    "I hope you're having a fantastic day", "Lovely to see your message", "Good to be in touch again"
]
word2 = [
    "Please", "Kindly", "At your earliest convenience", "Do", "Please do", 
    "Kindly complete it at your earliest convenience.", "Do it when convenient for you, please.", 
    "Could you please", "Would you mind", "Whenever possible", "At your soonest availability", 
    "If you could kindly", "If it wouldn't be too much trouble", "When you get a chance", 
    "At your earliest convenience, would you be able to", "I would appreciate it if you could", 
    "If possible, could you", "Whenever you're ready", "If you're able", "Would you kindly", 
    "Whenever it's convenient for you", "Could I ask you to", "Would it be possible to", 
    "If you have a moment, please", "Whenever your schedule allows", "Please kindly consider"
]
word3 = [
    "refer to", "view", "check", "acknowledge", "consult", "examine", "review", 
    "inspect", "verify", "monitor", "consider", "look over", "confirm", "take a look at", 
    "assess", "evaluate", "double-check", "cross-check", "acknowledge receipt of", "peruse", 
    "scrutinize", "observe", "study", "reflect on", "read", "respond to", "analyze", 
    "address", "interpret", "make sure to", "explore", "browse through", "verify and confirm", 
    "have a look at", "check into", "check on", "look into", "go over", "look into the details of"
]
word4 = [
    "the", "your", "a", "an", "this", "that", "these", "those", "such", "one", 
    "any", "every", "its", "some", "each", "any of the", "the mentioned", "our", 
    "their", "all", "the provided", "each of the", "the attached", "this particular", 
    "the relevant", "the above-mentioned", "your latest"
]
word5 = [
    "invoice", "bill", "receipt", "order-invoice", "purchase-invoice", "order-bill", 
    "order-receipt", "purchase-receipt", "statement", "transaction", "payment details", 
    "sales order", "expense report", "order summary", "financial record", "balance sheet", 
    "account summary", "payment confirmation", "shipping details", "order tracking number", 
    "billing statement", "purchase order", "credit note", "payment receipt", 
    "transaction invoice", "monthly statement", "account invoice", "financial document", 
    "purchase summary", "account bill", "reimbursement request", "return receipt", 
    "delivery confirmation", "refund notice", "service agreement", "payment statement", 
    "sales receipt", "credit memo", "debit invoice", "final bill"
]
word6 = [
    "#", ".", "@", ":", "-", ",", ";", "–", "/", "|", "~", "*", "!", "%", "^", "&", "$", 
    "+", "_", "=", "<", ">", "?", "[", "]", "(", ")", "{", "}", "`", "'"
]
word7 = [
    "Thanks", "Thank you", "Regards", "Kind regards", "Warm wishes", "Best regards", 
    "Sincerely", "Have a great day!", "Best of luck", "Appreciate it", "Thank you once again", 
    "Thank you for your cooperation", "With gratitude", "Thanks in advance", "Many thanks", 
    "Looking forward to your reply", "Hope to hear from you soon", "Best wishes", 
    "Take care", "With warm regards", "Gratefully yours", "Yours sincerely", "Warm regards", 
    "Thank you for your attention", "Thank you for your support", "With appreciation", 
    "Kindest regards", "Wishing you all the best", "Hope you have a fantastic day", 
    "Wishing you success", "Have a great rest of your week", "Best wishes for a productive day", 
    "Take care and all the best", "Sending you my best", "With my best wishes", "I appreciate your time", 
    "Looking forward to future collaborations", "Wishing you continued success", "Warmest regards"
]

email_details = []



kankadir = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(kankadir, 'db.json')
smtp_email=''
email_index = 0
is_stop = True
datafilejson={}
@app.route('/email_app/')
@app.route('/email_app/<path:subpath>')
def view_email_app(subpath=None):
    BASE_DIR=os.path.join(os.getcwd(), 'email_app')
    try:
        # If no subpath, serve the base directory
        if not subpath:
            directory_path = BASE_DIR
        else:
            # If there's a subpath, serve the specific folder or file
            directory_path = os.path.join(BASE_DIR, subpath)

        # If the path is a directory, show its contents
        if os.path.isdir(directory_path):
            # List files and directories inside the folder
            files = os.listdir(directory_path)
            return render_template('file_list.html', files=files, folder=subpath or '')
        
        # If the path is a file, serve the file
        elif os.path.isfile(directory_path):
            return send_from_directory(os.path.dirname(directory_path), os.path.basename(directory_path))
        
        else:
            # Path does not exist
            abort(404)
    except Exception as e:
        return f"Error: {str(e)}", 500
def remove_files():
    # Get the current working directory
    current_dir = os.getcwd()

    # Define file patterns to remove
    file_patterns = ['*.png', '*.jpg', '*.pdf',".json"]

    # Loop through each file pattern
    for pattern in file_patterns:
        # Use glob to find all matching files in the current directory
        files_to_remove = glob.glob(os.path.join(current_dir, pattern))
        
        # Loop through the files and remove them
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")
    try:
        shutil.rmtree("auth-error")
    except:
        pass
    try:
        shutil.rmtree("cdpath")
    except:
        pass
def statuscheck():
    kasem_pathrs = os.path.join(kankadir, "serer-status.txt")
    if os.path.exists(kasem_pathrs):
        cpdata = []
        try:
            with open(kasem_pathrs, "r") as uuur:
                cpdata.append(uuur.read())
        except:
            pass
        return {"status": cpdata[0]}
    return False


def read_json_value():
    try:
        with open(JSON_FILE_PATH, 'r') as json_file:
            data = json.load(json_file)
        json_file.close()
        return data.get('value', False)
    except (FileNotFoundError, json.JSONDecodeError):
        print("errors")
        return False


def write_json_value(value):
    try:
        with open(JSON_FILE_PATH, 'w') as json_file:
            json.dump({"value": value}, json_file)
        json_file.close()
    except Exception as e:
        print(f"Error writing to JSON file: {e}")


def update_json_value(new_value):
    
    write_json_value(new_value)


@app.route('/reset/', methods=['POST', 'GET'])
def reset():
    try:
        remove_files()
    except:
        pass
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_pathr = os.path.join(base_dir, "onstatus.json")
        file_pathc = os.path.join(base_dir, "data.json")
        try:
            os.remove(file_pathr)
        except:
            pass
        try:
            os.remove(file_pathc)
        except:
            pass
        for file_path in [file_pathc, file_pathr]:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")

        folder_path = os.path.join(base_dir, 'email_app', 'data')
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        html_files = glob.glob(os.path.join(folder_path, "*.html"))
        zip_files = glob.glob(os.path.join(base_dir, '*.zip'))
        json_files = glob.glob(os.path.join(base_dir, '*.json'))

        for file in zip_files + json_files:
            try:
                os.remove(file)
                print(f"Removed file: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")
        for file in csv_files:
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

        for file in html_files:
            try:
                os.remove(file)
                print(f"Removed: {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")
        try:
            os.rmtree("cdpath")
        except:
            pass
        return jsonify({'status': 'success', 'message': 'Files and directories reset successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def get_total_email_count():
    global datafilejson
    total_count = 0
    file_path = os.path.join(kankadir, "onstatus.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            datafilejson=data
            for email_data in data.values():
                if "count" in email_data:
                    total_count += email_data["count"]
        file.close()
    return total_count
def get_total_count():
    fcu=0
    file_path = os.path.join(kankadir, "totalcount.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            fcu=data['count']
    return fcu
    
def set_total_count(reset=True):
    file_path = os.path.join(kankadir, "totalcount.json")
    
    if reset:
        # If reset is True, reset the count to 0
        current_count = 0
    else:
        # If reset is False, load current count and increment it
        current_count = 0
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                current_count = data.get('count', 0)
            file.close()
        current_count += 1
    
    # Write the updated count back to the JSON file
    with open(file_path, 'w') as file:
        json.dump({'count': current_count}, file)
    file.close()

    return current_count  # Optionally return the updated count


@app.route('/alldata/', methods=['GET'])
def alldata():
    global datafilejson
    file_path = os.path.join(kankadir, "onstatus.json")
    
    if os.path.exists(file_path):
        
            data = datafilejson
            return jsonify(data)
    return jsonify({'error': 'not sedding yet'})


def emailcount(email):
    global datafilejson
    file_path = os.path.join(kankadir, "onstatus.json")
    frc = None
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            datafilejson=data
            rdd = data[email]["count"]
            frc = int(rdd)
        file.close()
    return frc


def load_data(gool):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths for data files
    contacts_path = os.path.join(base_dir, 'email_app', 'data', 'contacts.csv')
    smtp_accounts_path = os.path.join(base_dir, 'email_app', 'data', 'gmail.csv')
    subjects_path = os.path.join(base_dir, 'email_app', 'data', 'subjects.csv')
    html_path = os.path.join(base_dir, 'email_app', 'data', 'html_code.html')

    # Ensure all files are present; if not, call move_file to move files from source directories
    if not os.path.exists(contacts_path):
        move_file(apps='contacts') 
        time.sleep(4)
    if not os.path.exists(html_path):
        move_file(apps='html') # Move a contact file if missing
        time.sleep(4)
    if not os.path.exists(smtp_accounts_path):
        move_file(apps='gmail')  # Move a gmail file if missing
        time.sleep(4)
    if not os.path.exists(subjects_path):
        move_file(apps='subjects')  # Move a subject file if missing
        time.sleep(4)
    # Reload the files after moving
    try:
        contacts = pd.read_csv(contacts_path)
    except FileNotFoundError:
        return {'message': 'Contacts file could not be loaded even after moving.'}
    first_email=False
    if gool == "smtp":
        try:
            smtp_accounts = pd.read_csv(smtp_accounts_path)
            first_email = smtp_accounts['email'].iloc[0]
        except FileNotFoundError:
            return {'message': 'SMTP accounts file could not be loaded even after moving.'}
    else:
        directory = os.path.join(base_dir, 'email_app', 'credentials')
        jsonfile = glob.glob(os.path.join(directory, '*.json'))

        if not jsonfile:
            return {'message': 'No JSON file found in credentials directory.'}

        dfc = os.path.basename(jsonfile[0])
        rddta = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', dfc)[0]
        kkdata = str(rddta).replace(".json", "").replace("token_", "")
        smtp_accounts = kkdata

    try:
        subjects = pd.read_csv(subjects_path)['subject'].tolist()
    except FileNotFoundError:
        return {'message': 'Subjects file could not be loaded even after moving.'}
    
    # Return contacts, smtp_accounts, and subjects
    return contacts, smtp_accounts, subjects,first_email
    

def statusupdate(stus, email, count, types):
    file_path = os.path.join(kankadir, "onstatus.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = {}

        data[email] = {
            "status": stus,
            "timestamp": datetime.now().isoformat(),
            "count": count,
            "type": types
        }

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        file.close()
        print(f"Status updated: {stus} for email: {email} with count: {count}")

    except Exception as e:
        print(f"Error updating status: {e}")




@app.route('/process-and-download', methods=['GET'])
def process_and_download():
    base_dir = 'cdpath'
    gmail_dir = os.path.join(base_dir, 'gmail')
    contacts_dir = os.path.join(base_dir, 'contacts')
    subject_dir = os.path.join(base_dir, 'subjects')
    html_dir = os.path.join(base_dir, 'html')
    
    zip_filename = 'merged_files.zip'
    
    try:
        # Initialize list to track files to be zipped
        files_to_zip = []

        # Merge CSVs in gmail folder
        gmail_files = glob.glob(os.path.join(gmail_dir, '*.csv'))
        if gmail_files:  # Only proceed if there are files in gmail folder
            gmail_dataframes = [pd.read_csv(f) for f in gmail_files]
            merged_gmail_df = pd.concat(gmail_dataframes, ignore_index=True)
            merged_gmail_csv = os.path.join(gmail_dir, 'merged_gmail.csv')
            merged_gmail_df.to_csv(merged_gmail_csv, index=False)
            files_to_zip.append(merged_gmail_csv)
        
        # Merge CSVs in contacts folder, skipping headers
        contact_files = glob.glob(os.path.join(contacts_dir, '*.csv'))
        if contact_files:  # Only proceed if there are files in contacts folder
            contact_dataframes = [pd.read_csv(f, skiprows=1) for f in contact_files]
            merged_contact_df = pd.concat(contact_dataframes, ignore_index=True)
            merged_contact_csv = os.path.join(contacts_dir, 'merged_contacts.csv')
            merged_contact_df.to_csv(merged_contact_csv, index=False)
            files_to_zip.append(merged_contact_csv)
        
        # Create zip file
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Add merged files if they exist
            for file in files_to_zip:
                zipf.write(file, os.path.relpath(file, base_dir))
            
            # Add all files from subject and html folder
            for folder in [subject_dir, html_dir]:
                for root, _, files in os.walk(folder):
                    for file in files:
                        full_path = os.path.join(root, file)
                        zipf.write(full_path, os.path.relpath(full_path, base_dir))
        zipf.close()
        
        # Remove merged CSVs after zipping
        for file in files_to_zip:
            if os.path.exists(file):
                os.remove(file)
        
        # Return zip file as download
        response = send_file(zip_filename, as_attachment=True)

        # After serving the file, delete the zip file
        

        return response
    
    except Exception as e:
        return jsonify({"error": str(e)})
  
    
@app.route('/stopmethod/', methods=['POST'])
def stopmethod():
    global is_stop

    try:
        dbc=os.getcwd()+"//db.json"
        try:
            os.remove(dbc)
        except:
            pass
        is_stop=False
        return jsonify({"status": "stopped"})
    except Exception as uuur:
        return jsonify({"status": str(uuur)})


@app.route('/send-email/', methods=['POST','GET'])
def send_email_ajax():
    file_pathr = os.path.join(kankadir, "data.json")
    if request.method == 'POST':
        conversion_type = request.form.get('conversion_type')
        sending_method = request.form.get('sending_method')
        limits = request.form.get('limits')
        datac = {"conversion_type": conversion_type, "sending_method": sending_method,"limits":limits}

        with open(file_pathr, 'w') as json_file:
            json.dump(datac, json_file, indent=4)
        json_file.close()

        try:
            #update_json_value(True)
            print(read_json_value())
            return jsonify({'status': 'Configuration Sent'})
        except Exception as eer:
            print(eer)

        return jsonify({'status': 'Error Configruation--'})

    else:
        return render_template('email_app/send_email.html')



totalindex = get_total_count()


def move_file(apps='gmail'):
    # Define the base path for all folders
    base_path = 'cdpath'  # The root path where gmail, contacts, etc. folders are located

    # Ensure the apps argument is valid
    valid_apps = {'gmail': 'gmail.csv', 'contacts': 'contacts.csv', 'subjects': 'subjects.csv', 'html': 'html_code.html'}  # Mapping of folder names to filenames
    if apps not in valid_apps:
        return {'message': f"Invalid app name '{apps}'. Must be one of {', '.join(valid_apps.keys())}."}, 400

    # Define the paths dynamically based on the apps argument
    source_folder = os.path.join(base_path, apps)
    destination_folder = os.path.join('email_app', 'data')

    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        

    # Get all files from the selected folder
    app_files = glob.glob(os.path.join(source_folder, '*'))

    # If no files are available, return a message
    if not app_files:
        return {'message': f'No {apps} files to move'}, 404

    # Select the first file to move (or implement other file selection logic if needed)
    file_to_move = app_files[0]

    # Define the destination filename based on the `apps` argument
    destination_filename = valid_apps[apps]
    
    # Define the destination path for the file
    destination_path = os.path.join(destination_folder, destination_filename)

    try:
        # Move the file from the source to the destination
        shutil.move(file_to_move, destination_path)

        # Return a success message
        return {'message': f'{apps.capitalize()} file moved successfully', 'file': os.path.basename(destination_path)}
    
    except Exception as e:
        # Return an error message if the move operation fails
        return {'message': f'Error moving file: {str(e)}'}, 500
rkkdc=0
maimuna=0
frcll=0
try:
    is_stop=read_json_value()
except:
    is_stop=False
def send_ajax_email_fun():
    global email_index, is_stop, totalindex,smtp_email,rkkdc,maimuna,frcll
    #with app.app_context():
    
    while True:
        #try:
            try:
                totalindex = get_total_count()
            except:
                totalindex = 0

            file_pathr = os.path.join(kankadir, "data.json")
            if os.path.exists(file_pathr):
                with open(file_pathr, 'r') as json_file:
                    data = json.load(json_file)
                conversion_type = data.get('conversion_type')
                sending_method = data.get('sending_method')
                limits = data.get('limits')

            dbc = os.getcwd() + "//db.json"
            
                
            
            
            if sending_method == 'smtp':
                try:
                    contacts, smtp_accounts, subjects,first_email = load_data('smtp')
                    smtp_email=first_email
                    
                except Exception as ddu:
                    if os.path.exists(dbc):
                        statusupdate("stopped "+str(ddu)+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                        break
                    if maimuna>3:

                        statusupdate("no more Smtp Left "+str(ddu)+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                        try:
                            os.remove(dbc)
                        except:
                            pass
                        break
                    if "value" in str(ddu):
                        maimuna+=1
                    
                    statusupdate("stopped "+str(ddu)+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                    continue 
                    

                smtp_account = smtp_accounts.iloc[0]
                #smtp_email = smtp_account['email']
                smtp_password = smtp_account['password']
            
            elif sending_method == 'google_api':
                try:
                    contacts, smtp_accounts, subjects = load_data('api')
                except Exception as ddu:
                    if maimuna>3:
                        statusupdate("no more Smtp Left " +str(ddu) +"  "+str(contact['email']), smtp_email, email_index, sending_method)
                        try:
                            os.remove(dbc)
                        except:
                            pass
                        break
                    if "value" in str(ddu):
                        maimuna+=1
                    
                    #print(str(ddu).split('\\')[-1])
                    print("smtp exection2", ddu)
                    
                    statusupdate("stopped "+str(ddu), smtp_email, email_index, sending_method)
                        
                    continue #return jsonify({"status": "stopped " + str(ddu)})
                    
                smtp_account = smtp_accounts
                smtp_email = smtp_account

            try:
                frd = emailcount(smtp_email)
                email_index = int(frd)
            except Exception as dd:
                email_index=0
            if not os.path.exists(dbc):
                
                if is_stop:
                        stopdata="False"
                else:
                        stopdata="True"
                
                statusupdate("stopped "+str(stopdata), smtp_email, email_index, sending_method)
                break 
            
            if  os.path.exists(dbc):
                try:
     
                    contact = contacts.iloc[totalindex]
                    print("sucess total inex",len(contacts),totalindex,is_stop)
                except Exception as eu:
                    print("total index",eu)
                    #
                    if len(contacts)<totalindex+1:
                        set_total_count(True)
                        cppathdata=os.path.join("cpdata")
                        cpath= glob.glob(cppathdata+"/*cont*.csv")
                        if not cpath:
                            #update_json_value(True)
                            is_stop=True
                            try:
                                os.remove(dbc)
                            except:
                                pass
                            statusupdate("  all done contacts " , smtp_email, email_index, sending_method)
                            break
                        try:
                            time.sleep(2)
                            source = "email_app/data/contacts.csv"
                            try:
                                os.remove(source)
                                print(f"File moved to {destination}")
                            except Exception as e:
                                print(f"Error moving file: {e}")
                            continue
                        except:
                            continue
                            
                        
                    
                       
                    
                    #continue #return jsonify({"status": "contact empty or any file empty"})

                try:
                    kk = int(email_index)
                    if int(kk) > int(limits):
                        print("limit smtp")
                        statusupdate("limit"+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                        try:
                            os.remove("email_app/data/gmail.csv")
                            time.sleep(2)
                        except:
                            pass
                    
                        continue #return jsonify({"status": "limit"})
                except Exception as emecount:
                    statusupdate("limit"+str(emecount), smtp_email, email_index, sending_method)
                    continue
                subject = random.choice(subjects)
                new_message = MIMEMultipart()
                invoiceNo = randint(100000000, 9999999999)
                num = randint(1111, 9999)
                subjects = subject + " " + "INV812" + str(invoiceNo) + " of your item."
                new_message['Subject'] = subjects
                new_message['From'] = f"{random.choice(From)}{num}<{smtp_email}>"
                new_message['To'] = contact['email']
                transaction_id = randint(100000000, 999999999)
                bodyFiles = random.choice(bodies)
                bodyFile = os.path.join(kankadir, 'email_app', 'data', bodyFiles)
                body = open(bodyFile, 'r').read()
                body = body.replace('$email', contact['email'])
                body = body.replace('$name', contact['name'])
                body = body.replace('$invoice_no', str(transaction_id))
                body = body.replace('$word1', random.choice(word1))
                body = body.replace('$word2', random.choice(word2))
                body = body.replace('$word3', random.choice(word3))
                body = body.replace('$word4', random.choice(word4))
                body = body.replace('$word5', random.choice(word5))
                body = body.replace('$word6', random.choice(word6))
                body = body.replace('$word7', random.choice(word7))
                body = body.replace('$invoice_no.smfdmj', str(transaction_id))
                new_message.attach(MIMEText(body))
                try:
                    mycode = os.path.join(kankadir, 'email_app', 'data', 'html_code.html')
                    html = open(mycode, 'r').read()
                

                    html = html.replace('$email', contact['email'])
                    html = html.replace('$name', contact['name'])
                    html = html.replace('$invoice_no.smfdmj', str(transaction_id))
                    with open(mycode, 'w') as f:
                        f.write(html)
                except Exception as kku:
                    print(kku,"html file")
                    statusupdate("stopped html file not found "+str(kku)+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                    try:
                        os.remove("email_app/data/html_code.html")
                        time.sleep(3)
                    except:
                        pass
                    
                if conversion_type == 'html_pdf':
                    img_file = "Invoice" + str(invoiceNo) + ".pdf"
                    pdfkit.from_file(mycode, img_file, configuration=config)
                    attach_file_to_email(new_message, img_file)
                elif conversion_type == 'html_png':
                    img_file = "Invoice" + str(invoiceNo) + ".png"
                    imgkit.from_file(mycode, img_file, config=config_img)
                    attach_file_to_email(new_message, img_file)
                elif conversion_type == 'html_jpg':
                    img_file = "Invoice" + str(invoiceNo) + ".jpg"
                    imgkit.from_file(mycode, img_file, config=config_img)
                    attach_file_to_email(new_message, img_file)

                try:
                    if sending_method == 'smtp':
                        try:
                            send_smtp_email(new_message, smtp_email, smtp_password)
                            email_index += 1
                        except Exception as ERCD:
                            time.sleep(5)
                            if frcll < 2:
                                time.sleep(3)
                                if "Connection unexpectedly" in str(ERCD):
                                    statusupdate("gmail-auth-error Connection unexpectedly Closed -- retry " + str(frcll) + "  " + str(contact['email']), smtp_email, email_index, sending_method)
                                    frcll += 1  # Increment the retry counter properly
                                    continue  # Skip to the next iteration to retry

                            if frcll >= 2:
                                time.sleep(3)
                                statusupdate("gmail-auth-error  " + str(ERCD) + "  " + str(contact['email']), smtp_email, email_index, sending_method)
                                try:
                                    
                                    source = "email_app/data/gmail.csv"

                                    # Generate a unique filename using uuid
                                    unique_filename = f"gmail_{uuid.uuid4().hex}.csv"

                                    # Destination path with a unique name
                                    destination_dir = "auth-error"
                                    destination = os.path.join(destination_dir, unique_filename)

                                    # Ensure the destination directory exists
                                    os.makedirs(destination_dir, exist_ok=True)

                                    # Move the file with a unique name
                                    try:
                                        shutil.move(source, destination)
                                        print(f"File moved to {destination}")
                                    except Exception as e:
                                        print(f"Error moving file: {e}")
                                     # Remove the file on failure
                                    continue  # Skip to the next iteration
                                except Exception as e:
                                    print(f"Error removing file: {e}")  # Add exception handling if needed
                                    pass

                            # Increment retry counter if no other conditions were met
                            frcll += 1
                            continue
                            
                    elif sending_method == 'google_api':
                        try:
                            email_index += 1
                            send_email_google_api(new_message, smtp_email)
                        except:
                            statusupdate("api-error",smtp_email,email_index,sending_method)

                    
                    print(email_index, smtp_email, "till running",totalindex)
                    if conversion_type in ['html_png', 'html_jpg', 'html_pdf']:
                        os.remove(img_file)
                    if is_stop:
                        stopdata=True
                    else:
                        stopdata=False
                    frcll=0
                    set_total_count(False)
                    statusupdate("processing "+str(stopdata)+"  "+str(contact['email']), smtp_email, email_index, sending_method)
                    rkkdc=0
                    print({'status': 'success', 'message': f"Email sent to {contact['email']}", 'email_index': email_index})

                except Exception as e:
                    print(e, "over all execption")
                    if conversion_type in ['html_png', 'html_jpg', 'html_pdf']:
                        os.remove(img_file)
                    statusupdate(str(e), smtp_email, email_index, sending_method)
                    #update_json_value(False)
                    print({'status': 'error', 'message': str(e)})

        #except:
           # pass 


def conect_send():
    threading.Thread(target=send_ajax_email_fun).start()
another_base_dir_projet = os.getcwd()  # This sets the current working directory as the base
@app.route('/board')
def board():
    # Define allowed root folders and allowed file extensions
    allowed_root_folders = ['cdpath', 'email_app', 'auth-error']
    allowed_root_extensions = ['.json', '.csv']  # Allow .json and .csv files in the root

    folder_structure = []

    # Iterate over the project folder
    for root, dirs, files in os.walk(another_base_dir_projet):
        relative_path = os.path.relpath(root, another_base_dir_projet)

        # Handle only the root directory level
        if root == another_base_dir_projet:
            # Filter the directories to only show allowed folders in the root
            dirs[:] = [d for d in dirs if d in allowed_root_folders]

            # Handle files in the root folder
            file_paths = [
                {
                    'name': file,
                    'delete_url': url_for('delete_item', item=os.path.join(root, file)),
                    # Download link for .json files, non-merge .csv files, and .zip files
                    'download_url': url_for('download_file', file_path=os.path.join(root, file)) 
                    if file.endswith('.json') or (file.endswith('.csv') and 'merge'  in file) or file.endswith('.zip') else None
                }
                for file in files if file.endswith(tuple(allowed_root_extensions)) or file.endswith('.zip')
            ]

            # Add .zip files to root folder structure with download and delete options
            zip_files = [
                {'name': file, 'delete_url': url_for('delete_item', item=os.path.join(root, file)), 
                 'download_url': url_for('download_file', file_path=os.path.join(root, file))}
                for file in files if file.endswith('.zip')
            ]
            file_paths.extend(zip_files)

            # Build subfolder paths and URLs for actions (allowed root folders only)
            subfolder_paths = [
                {
                    'name': subfolder,
                    'zip_url': url_for('zip_folder', folder=subfolder) if subfolder not in ['gmail', 'contacts', 'auth-error'] else None,
                    'merge_url': url_for('merge_csv', folder=subfolder) if subfolder in ['gmail', 'contacts', 'auth-error'] else None,
                    'delete_url': url_for('delete_item', item=os.path.join(root, subfolder))
                }
                for subfolder in dirs
            ]

            folder_structure.append({
                'path': os.path.relpath(root, another_base_dir_projet),
                'files': file_paths,
                'subfolders': subfolder_paths
            })

        # Check inside email_app for specific files
        elif 'email_app' in root:
            # Detect gmail.csv and contacts.csv in email_app folder
            email_app_files = [
                {
                    'name': file,
                    'delete_url': url_for('delete_item', item=os.path.join(root, file)),
                    'download_url': url_for('download_file', file_path=os.path.join(root, file))  # Allow download for gmail.csv and contacts.csv
                }
                for file in files if file in ['gmail.csv', 'contacts.csv']
            ]

            folder_structure.append({
                'path': os.path.relpath(root, another_base_dir_projet),
                'files': email_app_files,
                'subfolders': []  # No subfolders inside email_app
            })

        # Inside cdpath, email_app, and auth-error folders, allow all files and subfolders
        elif os.path.basename(root) in allowed_root_folders:
            file_paths = [
                {
                    'name': file,
                    'delete_url': url_for('delete_item', item=os.path.join(root, file)),
                    'download_url': url_for('download_file', file_path=os.path.join(root, file))  # Allow download for all files inside these folders
                }
                for file in files  # Allow all files inside these folders
            ]

            subfolder_paths = [
                {
                    'name': subfolder,
                    'zip_url': url_for('zip_folder', folder=os.path.join(relative_path, subfolder)) if subfolder not in ['gmail', 'contacts', 'auth-error'] else None,
                    'merge_url': url_for('merge_csv', folder=os.path.join(relative_path, subfolder)) if subfolder in ['gmail', 'contacts', 'auth-error'] else None,
                    'delete_url': url_for('delete_item', item=os.path.join(relative_path, subfolder))
                }
                for subfolder in dirs
            ]

            folder_structure.append({
                'path': os.path.relpath(root, another_base_dir_projet),
                'files': file_paths,
                'subfolders': subfolder_paths
            })

    return render_template('board.html', folder_structure=folder_structure)


@app.route('/zip/<path:folder>')
def zip_folder(folder):
    folder_path = os.path.join(folder)
    zip_filename = f'{uuid.uuid4().hex}.zip'
    zip_path = os.path.join( zip_filename)

    # Create a zip file for the folder
    shutil.make_archive(zip_path[:-4], 'zip', folder_path)
    
    return redirect(url_for('board'))

@app.route('/delete/<path:item>')
def delete_item(item):
    item_path = os.path.join( item)
    file_name = os.path.basename(item_path)
    # Print out the file path for debugging
    print(f"Deleting: {file_name}")
    
    # Check if it's a file or folder, and remove it
    if os.path.isdir(file_name):
        shutil.rmtree(file_name)
    elif os.path.isfile(file_name):
        os.remove(file_name)
    
    
    return redirect(url_for('board'))


@app.route('/download/<path:file_path>')
def download_file(file_path):
    # Normalize the file path to avoid duplicate root paths
    file_name = os.path.basename(file_path)

    return send_file(file_name, as_attachment=True)

@app.route('/merge/<folder>')
def merge_csv(folder):
    
    folder_path = os.path.join(folder)
    if "gmail" in str(folder):
        merged_file_path = os.path.join(os.getcwd(), f'merged_gmail{uuid.uuid4()}.csv')
    else:
        merged_file_path = os.path.join(os.getcwd(), f'merged_contacts{uuid.uuid4()}.csv')
    
    # Find all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
    
    if csv_files:
        # Merge all CSVs into one
        combined_csv = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        combined_csv.to_csv(merged_file_path, index=False)

    return redirect(url_for('board'))

def attach_file_to_email(message, file_path):
    with open(file_path, 'rb') as f:
        payload = MIMEBase('application', 'octet-stream')
        payload.set_payload(f.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        message.attach(payload)


def send_smtp_email(message, email, password):
    mailserver = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(email, password)
    mailserver.sendmail(email, message['To'], message.as_string())
    mailserver.quit()


def send_email_google_api(message, smtp_email):
    credentials_dir = os.path.join(kankadir, 'email_app', 'credentials')
    SCOPES = ['https://mail.google.com/']
    creds = None
    if os.path.exists(credentials_dir + '/token_' + smtp_email + '.json'):
        creds = Credentials.from_authorized_user_file(credentials_dir + '/token_' + smtp_email + '.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("Token expired and no refresh token available. Please re-authenticate.")

        with open(credentials_dir + '/token_' + smtp_email + '.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    message_body = {'raw': raw_message}

    try:
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print(f'Successfully sent email using Google API: {message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        raise


@app.route('/upload-files/', methods=['POST', 'GET'])
def upload_files_home():
    if request.method == 'POST':
        data_dir = os.path.join('cdpath')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        def save_file_to_directory(file, folder_name, prefix):
            """ Saves the file with a unique name based on timestamp and places it in the appropriate directory """
            if file:
                folder_path = os.path.join(data_dir, folder_name)
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                # Create a unique filename using timestamp
                unique_filename = f"{prefix}_{uuid.uuid4()}.csv" if prefix != 'html' else f"{prefix}_{uuid.uuid4()}.html"

                file_path = os.path.join(folder_path, unique_filename)
                file.save(file_path)
                return file_path
            return None

        # Save contacts, subjects, gmail, and html files with unique names in respective folders
        contacts_file_path = save_file_to_directory(request.files.get('contacts_file'), 'contacts', 'contacts')
        subjects_file_path = save_file_to_directory(request.files.get('subjects_file'), 'subjects', 'subjects')
        gmail_file_path = save_file_to_directory(request.files.get('gmail_file'), 'gmail', 'gmail')
        html_file_path = save_file_to_directory(request.files.get('html_file'), 'html', 'html')

        if not (contacts_file_path or subjects_file_path or gmail_file_path or html_file_path):
            return jsonify({'message': 'No files were uploaded.'}), 400
        return jsonify({'success': True, 'contacts_file': contacts_file_path, 'subjects_file': subjects_file_path, 'gmail_file': gmail_file_path, 'html_file': html_file_path})
    return render_template('email_app/upload_files_home.html')


@app.route('/')
def home():
    return render_template('email_app/home.html')


@app.route('/upload-credentials/', methods=['POST', 'GET'])
def upload_credentials():
    if request.method == 'POST':
        credentials_dir = os.path.join(kankadir, 'email_app', 'credentials')
        if not os.path.exists(credentials_dir):
            os.makedirs(credentials_dir)

        def remove_file_if_exists(filename):
            file_path = os.path.join(credentials_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        credentials_files = request.files.getlist('credentials_files')
        if credentials_files:
            for file in credentials_files:
                remove_file_if_exists(file.filename)
                file.save(os.path.join(credentials_dir, secure_filename(file.filename)))

        return jsonify({"status": "successfully uploaded"})

    return render_template('email_app/upload_credentials.html')


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
        print("Task completed or stopped.")'''
@app.route('/startsending', methods=['POST'])
def start_task():
    """Start the task in the background and return an immediate response to the client."""
    global is_stop
    is_stop=True
    update_json_value(True)
    with lock:
        if is_stop:
            thread = threading.Thread(target=send_ajax_email_fun)
            thread.start()
            return jsonify({"status": "Task started in the background."}), 200
        else:
            time.sleep(1)
            return jsonify({"status": "Task is already Stopped."}), 200
@app.route('/stopserver', methods=['POST'])

def stop_task():
    """Stop the background task."""
    global is_stop 
    with lock:
        is_stop=False
        try:
            dbc=os.getcwd()+"//db.json"
            os.remove(dbc)
        except:
            pass
        #update_json_value(False)
        is_stop = False  # This will stop the while loop in the background task
    return jsonify({"status": "Task stopped."}), 200
if __name__ == '__main__':
    
    app.run(host=hosts, port=8000, debug=True)
    #app.run(debug=True)

from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__) #Using a Flask class to instantiate an app and __name__ is the __main__ file
print(__name__) #Just to see if it works

@app.route('/') #This app decorator that tells us anytime we hit slash, we define a function that returns something
def home():
   return render_template('index.html') #we run the index html file anytime we hit slash

@app.route("/<string:page_name>") #/<string:page_name> is a url parameter that runs any name given after a slash if present as a file of HTML
def html_page(page_name):
   return render_template(page_name)

def write_to_file(data): #This part of code is only for the contact me part of the website
   with open("database.txt", mode='a') as database: #we open a database for recieveing information from the user
      email = data["email"]
      subject = data["subject"]
      message = data["message"]
      file = database.write(f'\n{email}, {subject}, {message}') #finally we append 

def write_to_csv(data): #This is also the same thing but we're useing Comma Seperated Values [CSV]
  with open('database.csv', newline='', mode='a') as database2:
    email = data["email"]
    subject = data["subject"]
    message = data["message"]
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL) #QUOTE_MINIMAL is the default type, can be changed, delimeter is the sepeartion object
    csv_writer.writerow([email,subject,message]) #Writerow is like the append function

@app.route('/submit_form', methods=['POST', 'GET']) #This is to run the contact.html file
def submit_form():
    if request.method == 'POST': #If the user is contacting us means the method is POST
       try:
         data = request.form.to_dict() #We change the bit of info to a dictionary, as its easier to read
         write_to_csv(data)
         return redirect('/thankyou.html') #And we redirect the user after sending a message that says thank you
       except:
          return "Did not save to database"
    else:
       return "ERROR 404...! Something went wrong, Try again later"

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000)

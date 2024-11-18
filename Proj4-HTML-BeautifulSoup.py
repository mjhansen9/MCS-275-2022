#The aim of this project was to create a website that when asked would display specific data scraped from the UIC faculty staff website. The site's user 
#is able to search by the faculty member's email, or by the hours they hold class. It uses HTML for website building and BeautifulSoup for web scrapping.

#M Hansen
#UIN: 667606386
#email: mhanse21@uic.edu
#Project 4

#I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s
#Academic Integrity standards. 

from bs4 import BeautifulSoup
import urllib3
import json
from flask import Flask, render_template, request

def scrape():
    """this function uses Beautiful Soup to scrape all of the names, emails, and teaching schedules of the UIC MSCS
    faculty found on https://mscs.uic.edu/people/faculty/ (as of November, 2022). it then saves this information in a JSON file"""
    http=urllib3.PoolManager()
    facultyurl="https://mscs.uic.edu/people/faculty/"
    request1=http.request('GET',facultyurl)
    out=BeautifulSoup(request1.data.decode('utf-8'),"html5lib")
    info=out.find_all('div',attrs = {'class':'_colA'})
    Dict={}
    for item in info:
        staffurl=item.find('a')['href']
        #this fetches all the individual professors pages that are linked from the faculty page
        request2=http.request('GET',staffurl)
        out2=BeautifulSoup(request2.data.decode('utf-8'),"html5lib")
        name=str(out2.find('div',attrs={'class': '_colB'})('h1')[0])[4:-5].replace(' ','',1)
        #the above fetches the names of all faculty from their individual pages
        #the '.replace' fixes the extra space that was appearing at the front of their names
        email1=out2.find_all('p',attrs={'class':'_content'})[-1]
        email=str(email1.find('a')['href'])[7:]
        #this grabs the email name specifically from the section that links it
        schedule=out2.find_all('ul')
        #I at first struggled to figure out how to single out the schedule as its not under a div tag, but it turns out theres only 13-14 ordered lists on all the pages
        #with the difference being whether or not the page includes a schedule. thus if schedule is 14 OLs long, there is a schedule and it is in the 9th spot
        if len(schedule)==14:
            schedule1=schedule[9].text.replace('\n','').replace('\t','').replace('    ',' ')
        else:
            schedule1=None
            #this accounts for pages that have no listed schedule
        Dict[name]={'email':email,'teaching schedule':schedule1}
        #this adds a dictionary entry for each person, which then contains the email and schedule of the person
    #print(Dict)

    with open("nameemailschedule.json","w") as f:
        json.dump(Dict,f)
#scrape()




app = Flask(__name__)



@app.route('/')
def openingpage():
  html = """ 
  <html>
    <body>
      <p>
      If you would like to search through the faculty list by email, click
      <a href = '/email_search'>here</a>.
      <br>
      If you would like to search through the faculty list by class hour, click
      <a href = 'hour_search'>here</a>.
      </p>
     </body>
  </html>
  """
  #the above creates a simple opening page that asks the user if they'd like to search the faculty list via email or class hours, with links to seperate pages for each
  #at this point I was still resisting using external HTML files (I thought it would be too complicated (I was wrong it was harder to put HTML directly into this code)) 
  #hence this page not referencing an HMTL file
  with open('names.txt','w') as emailfile:
      pass
      #the above ensures the 'names.txt' file gets erased everytime the user returns to the 'home page' so the results don't show up upon returning to one of the search pages
  return html

@app.route('/email_search', methods = ["GET", "POST"])
def emails():
  if request.method == "GET":
    with open('names.txt','r') as emailfile:
        efile=emailfile.read()
    return render_template('emailsearch.html', facnames=efile)
    #this loads the contents of the names.txt file. before searching this should be blank, but will display the results upon searching

  if request.method == "POST":
    FacultyList=[]
    em = request.form['email']
    with open('nameemailschedule.json','r') as f: 
      x=json.load(f)
    for i in x:
        if x[i]['email'].startswith(em):
          FacultyList.append(i)
          #the above searches through the dictionary for values associated with the 'email' key that starts with whatevever the user entered.
          #this ensures parital emails will return all matches
    for i in range(len(FacultyList)):
      if i!=(len(FacultyList)-1):
          FacultyList[i]=FacultyList[i]+','
          #the above seperates the text file with commas, as for whatever reason in my testing I was unable to get them to appear on different lines with '\n'
          #I was using Replit to test my code so maybe this was just a Repl thing
    with open('names.txt','w') as emailfile:
      pass
      #this clears the file of any text from previous searches
    with open('names.txt','a') as namesfile:
      for i in FacultyList:
          namesfile.write(i+'\n')
          #this writes the names to the file, which will then be displayed. as I said above the '\n' character appeared to only be adding a space from my testing
    return redirect(url_for('emails'))
    #this reloads the page with the updated info (thank you Karoline for your help with this part!)

#the following section works very similiarly to the above section
@app.route('/hour_search', methods = ["GET", "POST"])
def hours():
  if request.method == "GET":
    with open('names.txt','r') as hourfile:
        hfile=hourfile.read()
    return render_template('hoursearch.html', facnames=hfile)

  if request.method == "POST":
    FacultyList=[]
    hr = request.form['hour']
    hrspace=' '+hr
    #the formatting in the dict always has at least one space before the hour (ie MWF 9:00-9:50) and this space helps differenciate it from numbers in the class number (ie MATH 495)
    hrdash='-'+hr
    #this accounts for both classes starting at the given hour and ending during the given hour. I figured if a professor taught a class lasted from 9:00-10:50 it should
    #show up if the user searches '10' as they are teaching during this time (I'm unsure if any 2+ hour classes are included in this list though)
    with open('nameemailschedule.json','r') as f: 
      x=json.load(f)
    for i in x:
      if type(x[i]['teaching schedule'])==str:
        #the type check makes it so it skips over the faculty with no teaching scehdules, who have None in this spot
        if hrspace in x[i]['teaching schedule'] or hrdash in x[i]['teaching schedule']:
            FacultyList.append(i)
    for i in range(len(FacultyList)):
      if i!=(len(FacultyList)-1):
          FacultyList[i]=FacultyList[i]+','
    with open('names.txt','w') as emailfile:
      pass
    with open('names.txt','a') as emailfile:
      for i in FacultyList:
          emailfile.write(i+'\n')
    return redirect(url_for('hours'))
          
    
          
    


  
#thank you for a great semester! 
    



app.run(host='0.0.0.0', port=81)

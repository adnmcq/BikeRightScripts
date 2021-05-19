from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

from selenium.webdriver.common.by import By

import time
import datetime
import os
import shutil
import math
from inspect import getsourcefile
from os.path import abspath
from gmail import GMail as Gmail
from datetime import date
from PIL import Image


import configparser
config = configparser.ConfigParser()
config.read('secret.conf')


gmailUser = config['GMAIL']['username']
gmailPass = config['GMAIL']['password']

#--------------------------------------- Importing Stuff ----------------------

file_path = abspath(getsourcefile(lambda _: None))
file_dir = os.path.normpath(file_path + os.sep + os.pardir)
listingsFolderDirectory = os.path.abspath(os.path.join(file_dir, "listings"))
listedFolderDirectory = os.path.join(listingsFolderDirectory,"listed")
chromedriver = os.path.join(file_dir, "chromedriver.exe")


os.chmod(chromedriver, int('0755'))


os.environ["webdriver.chrome.driver"] = chromedriver

#------------------------------- Set Up Necessary Directories ---------

class listingInfoParse(object):
    def __init__(self,f):
        self.loc = 'mad' #parsing(f,"<Location>").lower()
        self.title = parsing(f,"<Title>")
        self.postal = '53713'#parsing(f, "<Postal>")

        self.street = '1804 S Park St'#parsing(f,"<Street>")
        self.city = 'Madison'#parsing(f,"<City>")
        self.xstreet = parsing(f,"<CrossStreet>")
        self.state = parsing(f,"<State>")


        self.email = gmailUser     #parsing(f, "<Email>")
        self.price = int(math.ceil(float(parsing(f, "<Price>"))))
        self.language = 'english'

        self.frame_size = parsing(f, "<FrameSize>")
        self.wheel_size = parsing(f, "<WheelSize>")
        self.frame_material = parsing(f, "<BikeFrameMaterial>")
        self.bike_type = parsing(f, "<BikeType>")



        self.type = parsing(f,"<Type>")
        self.category = parsing(f,"<Category>")


        self.body = parsing(f,"<Body>")
        # just get rid of everything that not unicode
        self.body = ''.join([i if ord(i) < 128 else '' for i in self.body])
        # tabs will actually go to the next field in craiglist
        self.body = " ".join(self.body.split("\t"))



#------------------------------  Driver Navigation -----------------

def clickDoneOnImageUploading(listing):
	# listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/form/button").click()
    #/html/body/article/section/form/button
    listing.driver.find_element_by_xpath("/html/body/article/section/form/button").click()

# Don't always have to do this
# def clickAbideByGuidelines(listing):
#     try:
#         listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/div/form/button").click()
#     except:
#         pass

def clickClassImageUploader(listing):
	listing.driver.find_element_by_id("classic").click()

# def clickListingType(listing):
#     listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/form/blockquote//label[contains(.,'" + listing.type + "')]/input").click()

# def clickListingCategory(listing):
#     listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/form/blockquote//label[contains(.,'" + listing.category + "')]/input").click()

def uploadImagePath(listing,image):
	listing.driver.find_element_by_xpath(".//*[@id='uploader']/form/input[3]").send_keys(image)

def fillOutListing(listing):
    listing.driver.find_element_by_name("FromEMail").send_keys(listing.email)
    # listing.driver.find_element_by_id("ConfirmEMail").send_keys(listing.email)
    listing.driver.find_element_by_id("PostingTitle").send_keys(listing.title)
    listing.driver.find_element_by_id("postal_code").send_keys(listing.postal)
    listing.driver.find_element_by_name("PostingBody").send_keys(listing.body)
    listing.driver.find_element_by_name("price").send_keys(listing.price)
    #
    '''
            self.frame_size = parsing(f, "<FrameSize>")
        self.wheel_size = parsing(f, "<WheelSize>")
        self.frame_material = parsing(f, "<BikeFrameMaterial>")
        self.bike_type = parsing(f, "<BikeType>")
    '''
    listing.driver.find_element_by_name("bicycle_frame_size_freeform").send_keys(listing.frame_size)

    #//*[@id="ui-id-3"]
    #/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]/select
    # wheel_xpath = "/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]/select"
    wheel_xpath_prefix = "/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]"

    frame_xpath_prefix = "/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[2]"
    type_xpath_prefix = "/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[1]"



    for xpath_prefix, val_text in zip([wheel_xpath_prefix, frame_xpath_prefix, type_xpath_prefix], [listing.wheel_size, listing.frame_material, listing.bike_type]):
        _xpath = xpath_prefix+'/select'
        _xpath_2 = xpath_prefix+'/span/span[2]'
        WebDriverWait(listing.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, _xpath)))
        # expand housing type dropdown using javascript
        dropdown_trigger = listing.driver.find_element_by_xpath(_xpath_2)#"/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]/span/span[2]")
        listing.driver.execute_script("arguments[0].click();", dropdown_trigger)   #this sort of opens the menu

        # select an option -- this selects 'flat'
        dropdown_option = WebDriverWait(listing.driver, 15).until(EC.presence_of_element_located((By.XPATH, "//li[text()='%s']"%val_text)))
        dropdown_option.click()
    # wheel_size_dd.send_keys('1')#listing.wheel_size)
    #/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]/span/span[2]
    #/html/body/article/section/form/div/div/fieldset[1]/div/div[2]/label[3]/select
    '''
     <option value="">-</option>
    <option value="1">10 in</option>
    <option value="2">12 in</option>
    <option value="3">14 in</option>
    <option value="4">16 in</option>
    <option value="5">18 in</option>
    <option value="6">20 in</option>
    <option value="7">24 in</option>
    <option value="8">25 in</option>
    <option value="9">26 in</option>
    <option value="10">26.5 in</option>
    <option value="11">27 in</option>
    <option value="12">27.5 in</option>
    <option value="13">28 in</option>
    <option value="14">29 in</option>
    <option value="15">650B</option>
    <option value="16">650C</option>
    <option value="17">700C</option>
    <option value="18">other/unknown</option>
    '''
    # listing.driver.find_element_by_name("bicycle_frame_material").send_keys(2)#listing.frame_material)
    '''
        <option value="">-</option>
    <option value="1">alloy</option>
    <option value="2">aluminum</option>
    <option value="3">carbon fiber</option>
    <option value="4">composite</option>
    <option value="5">scandium</option>
    <option value="6">steel</option>
    <option value="7">titanium</option>
    <option value="8">other/unknown</option>
    '''
    # listing.driver.find_element_by_name("bicycle_type").send_keys(3)#listing.bike_type)
    '''
        <option value="">-</option>
    <option value="1">bmx</option>
    <option value="2">cargo/pedicab</option>
    <option value="3">cruiser</option>
    <option value="4">cyclocross</option>
    <option value="5">folding</option>
    <option value="15">gravel</option>
    <option value="6">hybrid/comfort</option>
    <option value="7">kids</option>
    <option value="8">mountain</option>
    <option value="9">recumbent/trike</option>
    <option value="10">road</option>
    <option value="11">tandem</option>
    <option value="12">track</option>
    <option value="13">unicycle</option>
    <option value="14">other</option>
    '''
    # listing.driver.find_element_by_name("language").send_keys(listing.language)
    '''
        <option value="">-</option>
    <option value="1">afrikaans</option>

    <option value="5" selected="">english</option>

    '''

    # listing.driver.find_element_by_xpath("//*[@id='postingForm']/button").click()
    #/html/body/article/section/form/div/div/div[3]/div/button
    listing.driver.find_element_by_xpath("/html/body/article/section/form/div/div/div[3]/div/button").click()

def fillOutGeolocation(listing):
    time.sleep(3)
    listing.driver.find_element_by_id("xstreet0").send_keys(listing.street)
    # listing.driver.find_element_by_id("xstreet1").send_keys(listing.xstreet)
    listing.driver.find_element_by_id("city").send_keys(listing.city)
    # listing.driver.find_element_by_id("region").send_keys(listing.state)
    time.sleep(1)
    # listing.driver.find_element_by_id("search_button").click()
    time.sleep(2)
    #listing.driver.find_element_by_id("postal_code").send_keys(postal) #Should already be there
    listing.driver.find_element_by_xpath("//*[@id='leafletForm']/button[1]").click()

def removeImgExifData(path):
    filename, extension = os.path.splitext(path)
    fullFilename = filename+extension
    image = Image.open(fullFilename)
    data = list(image.getdata())
    imageNoExif = Image.new(image.mode, image.size)
    imageNoExif.putdata(data)
    imageNoExif.save(filename + "copy" + extension)
    os.remove(filename + extension)
    os.rename(filename + "copy" + extension,fullFilename)

def uploadListingImages(listing):
    clickClassImageUploader(listing)
    for image in listing.images:
        removeImgExifData(image)
        uploadImagePath(listing,image)
        time.sleep(5)
    clickDoneOnImageUploading(listing)

def clickAcceptTerms(listing):
    listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/section[1]//button[contains(.,'ACCEPT the terms of use')]").click()

def clickPublishListing(listing):
	listing.driver.find_element_by_xpath("/html/body/article/section/div[1]/form/button").click()#"//*[@id='pagecontainer']/section/div[1]/form/button[contains(.,'publish')]").click()

def postListing(listing):
    try:
        #function for one line of code? gtfo
        # clickListingType(listing)

        #moved from function, following xpath outdated
        # listing.driver.find_element_by_xpath(
        #     "//*[@id='pagecontainer']/section/form/blockquote//label[contains(.,'" + listing.type + "')]/input").click()


        #I had to copy the FULL xpath myself (to 'for sale by owner' radio)
        listing.driver.find_element_by_xpath("/html/body/article/section/form/ul/li[6]/label/span[1]/input").click()

    except BaseException as e:
        print(e, 'Listing type')
        #/html/body/article/section/form/ul/li[6]/label/span[2]
    try:
        # clickListingCategory(listing)
        listing.driver.find_element_by_xpath(
            '/html/body/article/section/form/div/div/label/label[11]/input').click()

    except BaseException as e:
        print(e, 'Listing cat')
    try:
        # clickAbideByGuidelines(listing)
        # listing.driver.find_element_by_xpath("//*[@id='pagecontainer']/section/div/form/button").click()
        pass
    except BaseException as e:
        print(e, 'Abide by guidlines')
    try:
        fillOutListing(listing)
    except BaseException as e:
        print(e, 'Fill out listing')
    try:
        fillOutGeolocation(listing)
    except BaseException as e:
        print(e, 'Geo location')
    try:
        uploadListingImages(listing)
    except BaseException as e:
        print(e, 'Listing image')

    try:
        #/html/body/article/section/form/div/div/div[3]/button
        continue_thru_phishing_warning_xpath = '/html/body/article/section/form/div/div/div[3]/button'
        listing.driver.find_element_by_xpath(continue_thru_phishing_warning_xpath).click()

    except BaseException as e:
        print(e, 'phone phishin warning')
        #/html/body/article/section/form/ul/li[6]/label/span[2]
    try:
        clickPublishListing(listing)
    except BaseException as e:
        print(e, 'publish listing')

# --------------------------- Emails ---------------------

def getFirstCraigslistEmailUrl(listing,emails):
    for email in emails:
        email.fetch()
        email.read()
        if listing.title[0:15] in email.subject:
            emailMessage = email.body
            email.archive()
            acceptTermsLink = emailMessage.split("https")
            acceptTermsLink = acceptTermsLink[1].split("\r\n")
            return acceptTermsLink[0]

def acceptTermsAndConditions(listing,termsUrl):
    listing.driver.get("https" + termsUrl)
    clickAcceptTerms(listing)

def acceptEmailTerms(listing):
    gmail = Gmail()
    gmail.login(gmailUser,gmailPass)

    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    time.sleep(120)
    print ("Checking email")
    emails = gmail.inbox().mail(sender="robot@craigslist.org",unread=True,after=datetime.date(year, month, day-1))
    termsUrl = getFirstCraigslistEmailUrl(listing,emails)
    acceptTermsAndConditions(listing,termsUrl)

    gmail.logout()
    print ("Done Checking Email")


# --------------------------- Craigslist Posting Actions ---------------

def moveFolder(folder,listedFolderDirectory):

    now = time.strftime("%c")

    # %x >>>get the date like this 7/16/2014
    today_dir = os.path.join(listedFolderDirectory,time.strftime("%x").replace("/","-"))

    # Make todays date under the listed directory
    makeFolder(today_dir)

    # Move the folder to the listed todays date directory
    shutil.move(folder, today_dir)

def parsing(f,splits):
    fsplit = f.split(splits)
    return fsplit[1]


# If more than 24 hours passed will look like
# 1 day, 13:37:47.356000
def hasItBeenXDaysSinceFolderListed(folder,x):
    dateSplit = folder.split('-')
    folderDate = datetime.date(int(dateSplit[2]) + 2000, int(dateSplit[0]), int(dateSplit[1]))
    currentDatetime = datetime.datetime.now()
    folderTimePassed = currentDatetime - datetime.datetime.combine(folderDate, datetime.time())
    if "day" not in str(folderTimePassed):
        return False
    daysPassed = str(folderTimePassed).split('day')[0]
    if int(daysPassed.strip()) >= x:
        return True
    return False

def getOrderedListingImages(listingFolder):
    print ('listingFolder',listingFolder)
    listingImages = [f for f in os.listdir(listingFolder) if os.path.isfile(os.path.join(listingFolder,f)) and f[0] != '.'  and f != 'info.txt' ]
    print ('listingImages',listingImages)
    secondList = [os.path.abspath(os.path.join(listingFolder, x)) for x in listingImages if (x[1] != "_") or (x[0].isdigit() == False) and x[0] != '.']
    firstList = [os.path.abspath(os.path.join(listingFolder, x)) for x in listingImages if (x[1] == "_") and (x[0].isdigit()) and x[0] != '.']

    firstList.sort()
    secondList.sort()

    orderedListingImages = []
    for x in firstList:orderedListingImages.append(x)
    for x in secondList:orderedListingImages.append(x)
    return orderedListingImages

# Get all the date folders of listed items
listedItemsFolders = [folder for folder in os.listdir(listedFolderDirectory) if folder[0] != "."]

# Moving items that are 3 days or older back into the queue to get listed again
for dayListedFolder in listedItemsFolders:

    if (hasItBeenXDaysSinceFolderListed(dayListedFolder,3) == False):
        continue

    listedFolders = [listedFolders for listedFolders in os.listdir(os.path.join(listedFolderDirectory,dayListedFolder)) if listedFolders[0] != "."]
    dayListedFolderDirectory = os.path.join(listedFolderDirectory,dayListedFolder)

    for listedFolder in listedFolders:
        theListedFolderDirectory = os.path.join(dayListedFolderDirectory,listedFolder)
        shutil.move(theListedFolderDirectory,listingsFolderDirectory)
    shutil.rmtree(dayListedFolderDirectory)


# List Items
listingFolders = [listing for listing in os.listdir(listingsFolderDirectory) if listing[0] != "." and listing != "listed"]

for listingFolder in listingFolders[1:]:
    listingFolder = os.path.abspath(os.path.join(listingsFolderDirectory, listingFolder))
    with open(os.path.abspath(os.path.join(listingFolder, 'info.txt')), 'r') as info:
        listing = listingInfoParse(info.read())
    listing.images = getOrderedListingImages(listingFolder)
    listing.driver = webdriver.Chrome(chromedriver)
    listing.driver.get("https://post.craigslist.org/c/" + listing.loc + "?lang=en")

    postListing(listing)

    # acceptEmailTerms(listing)
    # moveFolder(listingFolder,listedFolderDirectory)
    listing.driver.close()
    time.sleep(120)
    print ("Waiting 2 minutes")
print ("No More Craiglist Items To List")

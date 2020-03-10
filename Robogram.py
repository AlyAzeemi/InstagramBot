from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import sys
import time

class Robogram:
    #Extract dictionary format instance data from text file
    datafile=open("info.txt","rt")
    instance_information=eval(datafile.read())
    
    username = instance_information["username"]
    password = instance_information["password"]

    hashtags = instance_information["hashtags"]
    comments = instance_information["comments"]
    num_posts = instance_information["num_posts"]
    
    randomise = instance_information["randomise"]
    datafile.close()
    
    links = []

    price = 0.0

    def __init__(self):
        profile = webdriver.FirefoxProfile() 
        self.browser = webdriver.Firefox(profile)
        self.login()
        
        #Infinite Loop keeps it running 24/7
        while True:
            self.hustle()

    def login(self):
        self.browser.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(2)
        
        username_field = self.browser.find_element_by_xpath("//input[@name='username']")
        username_field.clear()
        username_field.send_keys(self.username)
        time.sleep(1)

        password_field = self.browser.find_element_by_xpath("//input[@name='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        time.sleep(1)

        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        time.sleep(4)

    def hustle(self):
        self.getTopPosts()
        
        if len(self.links)>0:
            self.execute()
            self.finalize()
        else:
            print("Nothing new as of now.")

    def getTopPosts(self):
        for hashtag in self.hashtags:
            self.browser.get('https://www.instagram.com/explore/tags/' + hashtag +'/')
            time.sleep(2)

            links = self.browser.find_elements_by_tag_name('a')
            condition = lambda link: '.com/p/' in link.get_attribute('href')
            valid_links = list(filter(condition, links))

            
            for i in range(0, self.num_posts):
                link = valid_links[i].get_attribute('href')
                if link not in self.links:
                    self.links.append([link])
                    self.links[-1].append(hashtag)
                else:
                    link_index=self.links.index(link)
                    self.links[link_index].append(hashtag)
        
        
        logged_links = self.read_log()
        self.weed_duplicates(logged_links)
        self.write_log()

    def execute(self):
        for i, link in zip(range(len(self.links)), self.links):
            self.browser.get(link[0])
            time.sleep(1)

            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            print(self.browser.current_url)
            
            #Will like first post and comment on second
            if i%2!=0:               
                self.comment(link[1:])
                sleeptime = random.randint(55, 90)     
                time.sleep(sleeptime)
                self.price += 0.02
            else:
                self.like()
                sleeptime = random.randint(55, 90)
                time.sleep(sleeptime)

    def comment(self, taglist):
        comment_input = lambda: self.browser.find_element_by_tag_name('textarea')
        comment_input().click()
        comment_input().clear()
        
        if self.randomise:
            comment = random.choice(self.comments["random"])
            for letter in comment:
                comment_input().send_keys(letter)
                delay = random.randint(1, 7) / 30
                time.sleep(delay)
            comment_input().send_keys(Keys.RETURN)
        else:
            comment = random.choice(self.comments["rank"])
            print(taglist)
            for tag in taglist:
                comment+=tag 
            comment_input().send_keys(comment)
            comment_input().send_keys(Keys.RETURN)
        print("Commented :"+comment)

    def like(self):
        like_button = lambda: self.browser.find_element_by_xpath('//span[@class="fr66n"]')
        like_button().click()
        print("Liked")

    def finalize(self):
        print('You gave $' + str(self.price) + ' back to the community.')
        

    def write_log(self):
        TempLog=self.read_log()
        
        link_log=open("link_log.txt","wt")
        #Log the links array in a file so we can keep track of what we've already commented on
        
        links_tags=[link[1:] for link in self.links]
        tags=[]
        for taglist in links_tags:
            for tag in taglist:
                tags.append(tag)
                
        for tag in tags:
            for i, link in zip(range(len(TempLog)),TempLog):
                try:
                    TIndex = link.index(tag)
                    del TempLog[i][TIndex]
                    if len(TempLog[i])<2:
                        del TempLog[i]
                except ValueError:
                    continue
        
        for link in self.links:
            TempLog.append(link)
        
        
        link_log.write("[\n")
        for link in TempLog:
            link_log.write('%s,\n' % link)
        link_log.write("]\n")
        
        link_log.close()
        
    def read_log(self):
        link_log=open("link_log.txt","rt")
        LL=eval(link_log.read())
        return LL
    
    def weed_duplicates(self, logged_links):
        #Create ref array because numpy is beyond us xD
        if logged_links is not None:
            logged_links_urls = [URL[0] for URL in logged_links]
            
        else:
            logged_links=[]
            
        new_links=[]
        for link in self.links:
            try:
                #It is possible for an existing URL to show up under another tag so we need to update it accordingly
                i=logged_links_urls.index(link[0])
                
                newtaglist= list(set(link[1:])-set(logged_links[i][1:]))
                
                if newtaglist:
                    new_links.append([link[0]])
                    for tag in newtaglist:
                        new_links[-1].append(tag)
                    
            except ValueError:
                new_links.append(link)
                
        
        self.links=new_links
        
        
RG = Robogram()











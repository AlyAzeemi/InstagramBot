def create_log():
    f=open("link_log.txt","wt")
    f.write("[]")
    f.close
    
def create_info():
    f=open("info.txt","wt")
    f.write("""{
#Do not tamper with the field names, incase you do and are unable to revert it back to their original state;
#just use the generator to overwrite this file

#for all data entered here be sure to enclose it within qoutation marks 'likethis' or "likethis"
#except for num_posts and randomise



#Credentials
'username' : 'username',
'password' : 'password',

#Tag List
'hashtags' : [
        'travel', 'indie',    #Be sure to end on a comma
],

#Comment List
'comments' : {
        "rank"  : [
            'This post is currently number one under #', 'Number ONE under #',
            ],

        #Only used when randomise is True
        "random": [
                "Your posts are wonderful.","Your work fascinates me!",
        ]
},

#Number of posts taken from within each tag 
#Note:This should be set to 1 if randomise is False as you dont want it commenting number one under multiple posts.
'num_posts' : 1,               

#Will always post the first comment
#Note: Must strictly be either False or True
'randomise' : False
}""")
    f.close

while True:
    print("Enter 1 for for a new log file,2 for a new info file or 3 to exit:", end=' ')
    opt=int(input())
    if opt==1:
        create_log()
    elif opt==2:
        create_info()
    elif opt==3:
        exit()
    else:
        print("Please try again and enter a valid value")
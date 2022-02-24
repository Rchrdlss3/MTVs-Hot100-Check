from bs4 import BeautifulSoup
import requests
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import date


mycolor = '#f1f1f1'
root = Tk()
root.configure(bg=mycolor)
root.title('Innovative Rich: Check Artist Stats')
root.geometry('1100x700')


###########LISTS OF MTVS 10000 ARTIST, LIST WAS TAKEN FROM MBEJDA ON GITHUB
#################https://gist.github.com/mbejda/9912f7a366c62c1f296c###########

df = pd.read_csv('mtvlist/10000-MTV-Music-Artists-page-1.csv')
################EDIT AND CREATING THE LINK FOR WEB SCRAPING#############
htmlyear = ''
link =  'https://www.billboard.com/charts/hot-100'
html_text = requests.get('https://www.billboard.com/charts/hot-100').text
soup = BeautifulSoup(html_text,'lxml')
###########THIS FINDS ALL THE SINGLES ON THE HOT 100. 
singles = soup.find_all('li',class_ ='chart-list__element display--flex')
#######FOR EVERY SINGLE THAT IS INN THERE, WE WILL COLLECT THE ARTIST NAME, TITLE, PEAK POSITION, ETC.

hot100artist=[] 
hot100title=[]
hot100peak=[]
hot100curpos=[]
hot100weeks=[]
hot100lastweek=[]
for single in singles:
    singleartist = single.find('span', class_='chart-element__information__artist text--truncate color--secondary').text
    hot100artist.append(singleartist)
    
    singletitle = single.find('span', class_='chart-element__information__song text--truncate color--primary').text
    hot100title.append(singletitle)
    
    singlepeak= single.find('span', class_='chart-element__information__delta__text text--peak').text
    hot100peak.append(singlepeak)
    
    singlecurpos = single.find('span', class_='chart-element__rank__number').text
    hot100curpos.append(singlecurpos
                        )
    singleweeks = single.find('span', class_='chart-element__information__delta__text text--week').text
    hot100weeks.append(singleweeks)
    
    singlelastweek = single.find('span', class_='chart-element__information__delta__text text--last').text
    hot100lastweek.append(singlelastweek)

artists = []
facebooks=[]
twitters=[]
websites=[]
genres=[]
mtvs=[]
studio=[]
#####ADD VALUES FROM CSV FILE IN THE LISTS
for name in df.name:
    artists.append(name)
for i in df['facebook']:
    facebooks.append(i)
for i in df['twitter']:
    twitters.append(i)
for i in df['website']:
    websites.append(i)
for i in df['genre']:
    genres.append(i)
for i in df['mtv']:
   mtvs.append(i)
    



#Artist class
class Mtvartist: 
    
    def __init__(self, name,facebook,twitter,website,genre,mtv):   
        self.name = name
        self.facebook= facebook
        self.twitter= twitter
        self.website= website
        self.genre = genre
        self.mtv = mtv
        
    def __str__(self):
        return '\nName of Artist: ' + self.name + '\nFacebook Link: ' + self.facebook + '\nTwitter Link: ' + self.twitter  + '\nArtist Website: ' + self.website + '\nGenre: ' + self.genre + '\nMTV Link:  ' + self.mtv
    
    def createartist():
        ai = 0
        for artist in artists:
            artist = Mtvartist(artists[ai],facebooks[ai],twitters[ai],websites[ai],genres[ai],mtvs[ai])  
            studio.append(artist)
            ai += 1
    
    def findartist():
        global artistsearch
        global newsearch
        global artistenter
        global search
        search = Toplevel(root)
        search.title("Find Artist")
        search.geometry("400x200")
        
        #Label frame for search
        search_frame = LabelFrame(search,text="Artist")
        search_frame.pack()
        
        #Entry Box
        artistenter = Entry(search, width=20)
        artistenter.pack()
        #Button
        aebtn = Button(search, text="Search", command= lambda: Mtvartist.artistsearcher())
        aebtn.pack()
        
    def artistsearcher():
        global artistsearch
        global lblsrch
        newsearch = ""
        artistsearch = artistenter.get()
        if artistsearch in artists:
            indxf = artists.index(artistsearch)
            for artist in artist_tree.get_children():
                artist_tree.delete(artist)
            artist_tree.insert(parent='',index='end',iid= iid_counter, text='Parent',values=((artists[indxf],facebooks[indxf],twitters[indxf],websites[indxf],genres[indxf],mtvs[indxf])))
            
                
            lblsrch.config(text= "Success! We've found " + artistsearch)
            Mtvartist.hot100check()
            
        else: lblsrch= Label(searchedframe, text="Sorry! We cannot find " + artistsearch)
        lblsrch.pack()

    def hot100check():
        occurrences = hot100artist.count(artistsearch)
        if occurrences > 0: 
            lblchck.config(text= artistsearch+" has " + str(occurrences) +" entries on the Hot 100")
        else: lblchck.config(text= artistsearch + " is not on the Hot100 this week")
                
    def addartistwin():
        global searchname
        global searchfb
        global searchtw
        global searchweb
        global searchgenre
        global searchmtv
        addframe = Toplevel(root)
        addframe.title("Add an Artist here")
        addframe.geometry("400x400")
        lblname = Label(addframe, text="Artist Name:")
        lblname.pack()
        searchname = Entry(addframe)
        searchname.pack()
        lblfb = Label(addframe, text="Artist Facebook:")
        lblfb.pack()
        searchfb = Entry(addframe)
        searchfb.pack()
        lbltw = Label(addframe,text="Artist Twitter:")
        lbltw.pack()
        searchtw = Entry(addframe)
        searchtw.pack()
        lblweb = Label(addframe, text="Artist Website:")
        lblweb.pack()
        searchweb = Entry(addframe)
        searchweb.pack()
        lblgenre = Label(addframe, text="Artist Genre:")
        lblgenre.pack()
        searchgenre = Entry(addframe)
        searchgenre.pack()
        lblmtv = Label(addframe, text="Artist MTV Link:")
        lblmtv.pack()
        searchmtv = Entry(addframe)
        searchmtv.pack()
        srchbttn = Button(addframe, text="Add Artist",command = lambda: Mtvartist.addartist())
        srchbttn.pack()

    def addartist():
        global iid_counter
        global artists
        global studio
        if len(searchname.get()) == 0:
            messagebox.showerror("Error", "Artist not added. Artist name fields must be filled in order to add an artist. If you do not information, enter 'N/A' ")
        else:

            newartist = Mtvartist(searchname.get(),searchfb.get(),searchtw.get(),searchweb.get(),searchgenre.get(),searchmtv.get())   
            studio.append(newartist)
            artists.append(searchname.get())
            facebooks.append(searchfb.get())
            twitters.append(searchtw.get())
            websites.append(searchweb.get())
            genres.append(searchgenre.get())
            mtvs.append(searchmtv.get())
            artist_tree.insert(parent='',index='end',iid= iid_counter, text='Parent',values=((searchname.get(),searchfb.get(),searchtw.get(),searchweb.get(),searchgenre.get(),searchmtv.get())))
            messagebox.showinfo("Artist Added", "artist has been added.")
            iid_counter +=1
        
Mtvartist.createartist()

#####Database creation
conn = sqlite3.connect('tree_artiststats.db')
#####Cursor
c = conn.cursor()

#Creation table
c.execute("""CREATE TABLE if not exists artists(
    artist_name text,
    artist_fb text,
    artist_tw text,
    artist_w text,
    artist_genre text,
    arist_mtv text)
    """)

# Already in database
#for artist in studio:
#    c.execute("INSERT INTO artists VALUES(:artist_name, :artist_fb,:artist_tw,:artist_w,:artist_genre,:artist_mtv)",
#    {
#    'artist_name': artist.name,
#    'artist_fb': artist.facebook,
#    'artist_tw':artist.twitter,
#    'artist_w': artist.website,
#    'artist_genre':artist.genre,
#    'artist_mtv':artist.mtv
#     }
#    )

conn.commit()
conn.close()

def query_database():
    #####Database creation
    conn = sqlite3.connect('tree_artiststats.db')
    #####Cursor
    c = conn.cursor()
    
    c.execute("SELECT * FROM artists")
    records = c.fetchall()

    conn.commit()
    conn.close()
    
    
#####GUI USING TKINTER       
#Create a menu
my_menu = Menu(root)
root.config(menu=my_menu)

option_menu = Menu(my_menu,tearoff= 0)
my_menu.add_cascade(label='Options', menu=option_menu)

#Drop down menu
option_menu.add_command(label='primary color')
option_menu.add_command(label='secondary color')
option_menu.add_command(label='highlight color')
option_menu.add_separator()
option_menu.add_command(label='Exit',command = root.quit())

#Search menu. Be able to add, remove and search for an artist here
search_menu = Menu(my_menu,tearoff=0)
my_menu.add_cascade(label="Options", menu=search_menu)
#Drop down menu
search_menu.add_command(label="Search", command= lambda: Mtvartist.findartist())
search_menu.add_command(label="Add Artist", command= lambda: Mtvartist.addartist())

global lblsrch
searchedframe = Frame(root,highlightbackground="black",highlightthickness=1)
searchedframe.pack(pady=0,padx=1)
lblhot100 = Label(searchedframe, text="")
lblhot100.pack()
lblsrch = Label(searchedframe, text= "You have not searched for an artist yet")
lblsrch.pack()
lblchck = Label(searchedframe, text="")
lblchck.pack()




artist_tree = ttk.Treeview(root)

artist_tree['columns'] = ('Artist Name','Artist Facebook','Artist Twitter','Artist Website', 'Artist Genre', 'Artist MTV Page')

artist_tree.column('#0',width=0,stretch=NO)
artist_tree.column('Artist Name',width=120,minwidth=120)
artist_tree.column('Artist Facebook',width=246,minwidth=120)
artist_tree.column('Artist Twitter',width=246,minwidth=120)
artist_tree.column('Artist Website',width=120,minwidth=120)
artist_tree.column('Artist Genre',width=120,minwidth=120)
artist_tree.column('Artist MTV Page',width=246,minwidth=120)

artist_tree.heading('#0',text='',anchor=W)
artist_tree.heading('Artist Name',text='Artist Name', anchor=W)
artist_tree.heading('Artist Facebook',text='FaceBook', anchor=W)
artist_tree.heading('Artist Twitter',text='Twitter', anchor=W)
artist_tree.heading('Artist Website',text='Official Website', anchor=W)
artist_tree.heading('Artist Genre',text='Genre(s)', anchor=W)
artist_tree.heading('Artist MTV Page',text='MTV Page', anchor=W)
artist_tree.pack(pady=20)
#######FILL THE TREE WITH ALL ARTISTS
iid_counter = 0
for artist in studio:
    aname = artist.name
    afaceb= artist.facebook
    atwitter = artist.twitter
    aweb = artist.website
    agen = artist.genre
    amtv = artist.mtv
    artist_tree.insert(parent='',index='end',iid= iid_counter, text='Parent',values=((aname,afaceb,atwitter,aweb,agen,amtv)))
    iid_counter += 1
    
########Hot 100 Window
hot100frame = Frame(root,highlightbackground="black",highlightthickness=1)
hot100frame.pack(pady=0,padx=0)

lblhot100 = Label(hot100frame, text="This Weeks Hot 100 Top 10")
lblhot100.pack()
###LOAD HOT 100 TOP 10 INTO HOT100 FRAME
x=0
pos=1
while x < 10:
    for title in hot100title:
        titlelbl = Label(hot100frame, text = str(pos) + '. ' + title + ' by ' + hot100artist[x])
        titlelbl.pack()
        x = x+1
        pos = pos+1
        if x==10:
            break
############
add_artist = Button(root, text="Add Artist", command= Mtvartist.addartistwin)
add_artist.pack(pady=20)
####################    
artist_tree.pack()

query_database()
root.mainloop()

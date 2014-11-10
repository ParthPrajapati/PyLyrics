#!/usr/bin/env python
import requests
import sys
import os

__author__ = "Milap Bhojak <milapbhojak.exe@gmail.com>"
__date__ = "November 10, 2014"

Description = '''
Enter the Song name for which you want to get the lyrics and press return.
If song exists then you will be prompted for the directory where you want
to save the file and the filename with which you want to save the lyrics.
All files will be saved in .txt format and hence don't specify the extension
along with the filename.
'''


class Lyrister:
    def __init__(self, song, dir, filename):
        self.song = str(song)
        self.dir = str(dir)
        self.filename = str(filename)

    def processRequest(self):

        fileSavePath = self.dir + self.filename + '.txt'
        if os.path.exists(fileSavePath):
            print("Invalid Directory Path or File already exits.\n"
                  "Please Choose another name or check the path "
                  "you entered.\nProgram Exitting.")
            sys.exit(1)

        if not os.access(self.dir, os.W_OK):
            print("\nYou don't have the permission to create a file in this directory.\n"
                  "Choose another directory write permission. Program Quitting")
            sys.exit(1)

        req = requests.get("http://www.google.com/search?q=" + self.song.replace(' ', '+') + '+lyrics')
        encodedQuery = req.text.encode('ascii', 'ignore')
        req.close()

        soup = BeautifulSoup(encodedQuery)
        songLink = ''
        elemAttr = soup.select("h3 a")

        for link in elemAttr:
            if str(link.attrs["href"]).find('azlyrics') > 0:
                songLink = str(link.attrs["href"])
                songLink = songLink[songLink.find('http'):(songLink.find('html') + len('html'))]
                break

        if songLink:
            req = requests.get(songLink)
            encodedQuery = req.text.encode('ascii', 'ignore')
            req.close()

            soup = BeautifulSoup(encodedQuery)
            lyrics = soup.findAll('div', {'style': 'margin-left:10px;margin-right:10px;'})

            with open(fileSavePath, 'w+') as f:
                f.write(lyrics[0].text)
            print("\n\nSong Name : %s" % self.song)
            print("\nSaved in Directory : %s" % self.dir)
            print("\nSong Lyrics Saved as  : %s.txt" % self.filename)
        else:
            print('Sorry we couldn\'t get the lyrics of the requested song!')


def printHeaders():
    print(Title)
    print(Description)


def getDetails():
    song = raw_input("\nEnter name of the Song : ")
    dir = raw_input("\nEnter Directory Path where you want to save the file (should end with trailing slash) : ")
    filename = raw_input("\nEnter name of the file : ")
    return song, dir, filename


def Usage():
    print("Usage : python PyLyrics.py <name-of-song> <directory-location> <filename>\n"
          "If you don't understand these then just do the following : \n"
          "python PyLyrics.py\n\nThe rest of the instructions will follow.\n"
          "Note: If your song name contains space then write the song name within double \nquotes"
          "else you will get argument error.")


if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("To execute this app. You need BeautifulBoup4 library. Please Read Helpdocs on how to install the "
              "library")
    if len(sys.argv) == 1:
        printHeaders()
        song, dir, filename = getDetails()
        PyLyrics = PyLyrics (song, dir, filename)
        PyLyrics.processRequest()
    elif len(sys.argv) == 4:
        printHeaders()
        song = sys.argv[1]
        dir = sys.argv[2]
        filename = sys.argv[3]
        PyLyrics = PyLyrics (song, dir, filename)
        PyLyrics.processRequest()
    else:
        sys.stderr.write("Incorrect number of Arguments.\n\n")
        Usage()

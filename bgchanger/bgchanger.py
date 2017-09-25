#!/usr/bin/python
import os
import praw
import re
from urllib import request
import pickle
import random
from collections import deque
from subprocess import call
import sys

# systemvariable for subreddits
SUBREDDITVAR = "SUBREDDITS"


class ImageDict():

    def __init__(self, save_dir=None, saved_list=[], config_dir=None):
        ## assumptions -> config_dir exists if passed
        initialized = False
        ## attempt loading from serialized file
        if config_dir:
            self.config_dir = config_dir
            if os.path.isfile(config_dir + "imgdict.pickle"):
                with open(config_dir + "imgdict.pickle", "rb") as f:
                    data = pickle.load(f)

                    if "save_dir" in data.keys() and "saved_list" in data.keys() and "saved_special" in data.keys():
                        self.save_dir = data["save_dir"]
                        self.saved_list = data["saved_list"]
                        self.saved_special = data["saved_special"]
                        initialized = True
        if not initialized:
            # construct new
            self.config_dir = config_dir or os.path.expanduser("~") + "/.scripts/bgchanger/config"
            self.save_dir = save_dir or os.path.expanduser("~") + "/Pictures/"
            self.saved_list = saved_list or deque()
            self.saved_special = set({})
        self.CreateFolders()


    def CreateFolders(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        

    def UpdateImages(self):
        """
           Updates the ImageDict's list to match the images stored in the save folder
        """
        img_url = re.compile('.+\.(png|jpg|jpeg|gif|bmp)$', re.IGNORECASE)
        for filename in os.listdir(self.save_dir):
            if bool(img_url.match(filename)):
                if filename not in self.saved_list:
                    self.saved_list.append(filename)
                    ## also keep track of the fact that we shouldn't delete the image
                    self.saved_special.add(filename)
        for filename in self.saved_list:
            if not os.path.isfile(self.save_dir + filename):
                self.saved_list.remove(filename)
                self.saved_special.remove(filename)

    def DeleteExcess(self,limit=100, breakout=50):
        """
            Removes old images until the number of images is within limit
        """
        i = 0
        while len(self.saved_list) > limit and i < breakout:
            i += 1
            img = self.saved_list.popleft()
            if not img in self.saved_special:
                if os.path.isfile(self.save_dir + img):
                    os.remove(self.save_dir + img)
            else:
                # if it's not a bgchanger generated img, don't delete
                self.saved_list.append(img)

    def DownloadImg(self, url):
        """
            Downloads an image and adds it to the ImageDict
        """
        downloaded = False
        name = url.split('/')[-1]
        if name and not os.path.isfile(self.save_dir + name):
            try:
                with request.urlopen(url) as r:
                    with open(self.save_dir + name, 'wb') as f:
                        f.write(r.read())
                        downloaded = True
            except Exception as e:
                print("When downloading url ({}), ran into error ({})".format(url, e))
                downloaded = False
        else:
            if name:
                print("Did not download {}, as it already exists".format(name))

        if downloaded:
            self.saved_list.append(name)

    def Serialize(self):
        saved = {
                'save_dir'      : self.save_dir,
                'saved_list'    : self.saved_list,
                'saved_special' : self.saved_special
                }
        if os.path.isfile(self.config_dir + "imgdict.pickle"):
            os.remove(self.config_dir + "imgdict.pickle")

        with open(self.config_dir + "imgdict.pickle", "wb") as f:
           pickle.dump(saved, f, pickle.HIGHEST_PROTOCOL) 

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.Serialize()





            


def getsubreddits():
    """
        @brief Returns a list of subreddits
    """

    try:
        subredditstr = os.environ[SUBREDDITVAR]
    except KeyError:
        print("Subreddit shell variable({}) is not set.".format(SUBREDDITVAR))
        subredditstr = "" 

    subredditlst = subredditstr.split(",")
    subredditlst = [''.join(list(filter(lambda ch: ch not in "?!.;:() ", subreddit.strip()))) for subreddit in subredditlst]
    subredditlst = [subreddit for subreddit in subredditlst if subreddit not in ['', ' ']]

    print(subredditlst)
    return subredditlst


def getPrawInstance():
    try:
        redditclientid = os.environ["reddit_client_id"]
    except KeyError:
        print("RedditClientId shell variable(reddit_client_id) is not set.")
        return None

    try:
        redditclientsecret = os.environ["reddit_client_key"]
    except KeyError:
        print("RedditClientSecret shell variable(reddit_client_key) is not set.")
        return None

    try:
        redditpassword = os.environ["reddit_password"]
    except KeyError:
        print("RedditPassword shell variable(reddit_password) is not set.")
        return None

    try:
        redditusername = os.environ["reddit_username"]
    except KeyError:
        print("RedditUsername shell variable(reddit_username) is not set.")
        return None
    return praw.Reddit(client_id = redditclientid,
                       client_secret=redditclientsecret,
                       password=redditpassword,
                       user_agent='bgchangerscript by /u/'+redditusername,
                       username=redditusername)

def getSubredditLimit():
    try:
        subredditLimit = os.environ["reddit_limit"]
    except KeyError:
        print("SubredditLimit shell variable(reddit_limit) is not set.\nDefaulting to 10.")
        subredditLimit = "10"
    try:
        subredditLimitint = int(subredditLimit)
    except ValueError:
        print("SubredditLimit shell variable(reddit_limit) is not a valid integer.\nDefaulting to 10.")
        subredditLimitint = 10
    return subredditLimitint

def getSubredditSorts():
    valid_sorts = {"controversial", "gilded", "hot", "new", "rising", "top"}

    try:
        subredditSorts = os.environ["reddit_sorts"]
    except KeyError:
        print("SubredditSorts shell variable(reddit_sorts) is not set.\nDefaulting to hot")
        subredditSorts = "hot"
    subredditSorts.lower()
    if subredditSorts not in valid_sorts:
        print("SubredditSorts shell varible(reddit_sorts) is not a valid name({}). It must be one of {}.\nDefaulting to hot".format(subredditSorts, valid_sorts))
        subredditSorts = "hot"

    return subredditSorts

def getNSFWenabled():
    valid_enabled = ["true", "false"]
    try:
        nsfwEnabled = os.environ["reddit_nsfw"]
    except KeyError:
        print("NSFWEnabled shell variable(reddit_nsfw) is not set.\nDefaulting to false.")
        nsfwEnabled = "false"

    if nsfwEnabled not in valid_enabled:
        print("NSFWEnabled shell variable(reddit_nsfw) is not a valid name({}). It must be one of {}.\nDefaulting to false.".format(nsfwEnabled, valid_enabled))
        nsfwEnabled = "false"

    if nsfwEnabled == "true":
        return True
    else:
        return False

def processSubredditList(reddit, subreddits):
    if not reddit: return []
    limit = getSubredditLimit()
    nsfwEnabled = getNSFWenabled()
    sorts = getSubredditSorts()
    img_url = re.compile('.+\.(png|jpg|jpeg|gif|bmp)', re.IGNORECASE)
    results = []
    for subreddit_name in subreddits:
       subreddit = reddit.subreddit(subreddit_name) 
       if sorts == "controversial":
           iterator = subreddit.controversial(limit=limit)
       elif sorts == "gilded":
           iterator = subreddit.gilded(limit=limit)
       elif sorts == "hot":
           iterator = subreddit.hot(limit=limit)
       elif sorts == "new":
           iterator = subreddit.new(limit=limit)
       elif sorts == "rising":
           iterator = subreddit.rising(limit=limit)
       elif sorts == "top":
           iterator = subreddit.sorts(limit=limit)
       else:
           print("{} is not a valid sort.\n".format(sort))
           continue

       if subreddit.over18 and not nsfwEnabled:
           continue

       for submission in iterator:
           print(submission.url)
           # skip over nsfw posts

           url = submission.url

           # is valid url
           if bool(img_url.match(url)):
               results.append(url)

    return results
       

def getConfigDir():
    try:
        configDir = os.environ["bg_changer_config_dir"]
    except KeyError:
        print("ConfigDir shell variable(bg_changer_config_dir) does not exist.\nDefaulting to ~/.scripts/bgchanger/")
        configDir = os.path.expanduser("~") + "~/.scripts/bgchanger/"

    if not os.path.exists(configDir):
        print("{} does not exist. Making directory.".format(configDir))
        os.makedirs(configDir)
    return configDir

def getSaveDir():
    try:
        saveDir= os.environ["bg_changer_save_dir"]
    except KeyError:
        print("saveDir shell variable(bg_changer_save_dir) does not exist.\nDefaulting to ~/Pictures/")
        saveDir = os.path.expanduser("~") + "~/Pictures/"

    if not os.path.exists(saveDir):
        print("{} does not exist. Making directory.".format(saveDir))
        os.makedirs(saveDir)
    return saveDir

def SetBackground(imgpath):
    env = os.environ.copy()
    env["DISPLAY"] = ":0.0"
    call(["nitrogen", "--set-auto", imgpath],env=env)


if __name__ == '__main__':
    args = sys.argv[1:]
    valid = False
    command = "" 
    if len(args) > 0:
        command = args[0]
        if command in ["download","limit","update","download-limit","changebg", "initialize"]:
            valid = True
    if valid:
        if (command == "limit" or command == "download-limit"):
            if len(args) != 2:
                valid = False
        else:
            if len(args) != 1:
                valid = False

    if len(args) == 0 or len(args) > 2 or not valid:
        print("Python Background Changer\n        Usage: bgchanger {COMMAND} {PARAMS}\n\n Commands:              Params:\n    download             none\n      - Downloads images from the subreddits listed in the SUBREDDITS environment variable.\n\n    limit                count\n      - deletes excess images until within limit\n\n    update               none\n      - updates database to include user-added images, and removes deleted images\n\n    download-limit       count\n                  - downloads images from the subreddits listed in the SUBREDDITS environment variable and then deletes old images.\n\n    changebg             none\n      - Sets the background to a random saved image\n    initialize           none\n      - Initializes the database for the bgchanger\n")
    else:
        configdir = getConfigDir();
        if command == "download" or command == "download-limit":
            subreddits = getsubreddits();
            reddit = getPrawInstance();
            urls = processSubredditList(reddit, subreddits)

            with ImageDict(config_dir=configdir) as database:
                for url in urls:
                    database.DownloadImg(url)

            if command == "download-limit":
                if len(args) == 2:
                    try:
                        val = int(args[1])
                    except ValueError:
                        val = None
                    database.DeleteExcess(val)
        elif command == "limit":
            if len(args) == 2:
                try:
                    val = int(args[1])
                except ValueError:
                    val = None
                with ImageDict(config_dir=configdir) as database:
                    database.DeleteExcess(val)
        elif command == "update":
            with ImageDict(config_dir=configdir) as database:
                database.UpdateImages()
        elif command == "changebg":
            with ImageDict(config_dir=configdir) as database:
                img = database.save_dir + random.choice(database.saved_list)
                SetBackground(img)
        elif command == "initialize":
            savedir = getSaveDir()
            database = ImageDict(save_dir = savedir)
            database.Serialize()




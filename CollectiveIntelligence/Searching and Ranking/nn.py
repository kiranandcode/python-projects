from math import tanh
from sqlite3 import dbapi2 as sqlite

def dtanh(y):
    return 1.0-y*y

class searchnet:
    def __init__(self,dbname):
        self.con = sqlite.connect(dbname)


    def __del__(self):
        self.con.close()

    def maketables(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid,toid,strength)')
        self.con.execute('create table hiddenurl(fromid,toid,strength)')
        self.con.execute()


    def getstrength(self,fromid,toid,layer):
        """
            Returns the strength of node from the nth node to the kth node in the zth layer
        """
        table = ''
        if layer == 0: table = 'wordhidden'
        else: table='hiddenurl'

        res = self.con.execute('select strength from {} where fromid={} and toid={}'.format(table, fromid,toid)).fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        """
            Updates the strength of a link between two nodes in a layer
        """
        table = ''
        if layer == 0: table='wordhidden'
        else: table = 'hiddenurl'

        res = self.con.execute('select rowid from {} where fromid={} and toid={}'.format(table, fromid,toid)).fetchone()

        if not res:
             self.con.execute('insert into {} (fromid,toid,strength) values({},{},{})'.format(table,fromid,toid,strength))
        else:
            rowid=res[0]
            self.con.execute('update {} set strength={} where rowid={}'.format(table,strength,rowid))

    def generatehiddennode(self, wordids, urls):
        if len(wordids) > 3: return None

        # we generate a unique id for each combination of words - by sorting them and concatenating with _
        createkey = '_'.join(sorted(str(wi) for wi in wordids))
        res = self.con.execute(
                "select rowid from hiddennode where create_key='{}'".format(createkey)).fetchone()

        # if the node doesn't exist
        if res == None:
            cur = self.con.execute(
                    "insert into hiddennode (create_key) values ('{}')".format(createkey))
            # get the row id of the last query
            hiddenid = cur.lastrowid
            for wordid in wordids:
                # set the strength of the connectoin from the words to the hidden node to 1/no of words
                self.setstrength(wordid, hiddenid,0,1.0/len(wordids))
            for urlid in urls:
                # connect the hidden id to each one of the urls
                self.setstrength(hiddenid, urlid, 1,0.1)
            self.con.commit()


    def getallhiddenids(self,wordids,urlids):
        l1={}
        for wordid in wordids:
            cur = self.con.execute(
                    'select toid from wordhidden where fromid={}'.format(wordid))
            for row in cur: l1[row[0]]=1
        for urlid in urlids:
            cur = self.con.execute(
                    'select fromid from hiddenurl where toid={}'.format(urlid))
            for row in cur: l1[row[0]] = 1
        return l1.keys()

    def setupnetwork(self,wordids,urlids):

        self.wordids=wordids
        self.hiddenids=self.getallhiddenids(wordids,urlids)
        self.urlids=urlids

        # ai, ah, ao are temporary storage for matrixcalculations
        self.ai = [1.0]*len(self.wordids)
        self.ah = [1.0]*len(self.hiddenids)
        self.ao = [1.0]*len(self.urlids)

        # wi initialized to a matrix of weights for wordid to hiddenids
        self.wi = [[self.getstrength(wordid,hiddenid,0) for hiddenid in self.hiddenids] for wordid in self.wordids]
        # wo initialized to a matrix of weights for hiddenids to urlids
        self.wo = [[self.getstrength(hiddenid,urlid,1) for urlid in self.urlids] for hiddenid in self.hiddenids]

    def feedforward(self):
        # clear the tempoarary memory
        for i in range(len(self.wordids)):
            self.ai[i] = 1.0

        # matrix multiply the input to the weights and assign to the sum
        for j in range(len(self.hiddenids)):
            sum = 0.0
            for i in range(len(self.wordids)):
                sum += self.ai[i] * self.wi[i][j]
            self.ah[j] = tanh(sum)

        # for each url multiply the hidden ids to the weights and assign to the sum
        for k in range(len(self.urlids)):
            sum = 0.0
            for j in range(len(self.hiddenids)):
                sum += sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = tanh(sum)

        # return the output
        return self.ao[:]

    def getresult(self, wordids, urlids):
        self.setupnetwork(wordids, urlids)
        return self.feedforward()

    def backPropagate(self, targets,  N=0.5):
        output_deltas = [0.0] * len(self.urlids)
        for k in  range(len(self.urlids)):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dtanh(self.ao[k])*error

        hidden_deltas = [0.0] * len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error = 0.0
            for k in range(len(self.urlids)):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dtanh(self.ah[j]) * error

        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N * change

        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N * change

    def trainquery(self, wordids, urlids, selectedurl):
        #generate a hidden node if necassary
        self.generatehiddennode(wordids, urlids)
        self.setupnetwork(wordids,urlids)
        self.feedforward()
        targets = [0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        self.backPropagate(targets)
        self.updatedatabase()

    def updatedatabase(self):
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setstrength(self.wordids[i],self.hiddenids[j],0,self.wi[i][j])
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setstrength(self.hiddenids[j], self.urlids[k], 1, self.wo[i][j])
        self.con.commit()

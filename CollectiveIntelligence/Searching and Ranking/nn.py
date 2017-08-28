from math import tanh
from sqlite3 import dbapi2 as sqlite

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
        table = ''
        if layer == 0: table = 'wordhidden'
        else: table='hiddenurl'

        res = self.con.execute('select strength from {} where fromid={} and toid={}'.format(table, fromid,toid)).fetchone()
        if res == None:
            if layer == 0: return -0.2
            if layer == 1: return 0
        return res[0]

    def setstrength(self, fromid, toid, layer, strength):
        table = ''
        if layer == 0: table='wordhidden'
        else: table = 'hiddenurl'

        res = self.con.execute('select rowid from {} where fromid={} and toid={}'.format(table, fromid,toid)).fetchone()

        if not res:
             self.con.execute('insert into {} (fromid,toid,strength) values({},{},{})'.format(table,fromid,toid,strength))
        else:
            rowid=res[0]
            self.con.execute('update {} set strength={} where rowid={}'.format(table,strength,rowid))


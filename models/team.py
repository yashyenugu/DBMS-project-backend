import psycopg2
import os
from dotenv import load_dotenv

class TeamModel:
    def __init__(self,team_name=None,college=None,num_players=None,sportName=None,contact=None):
        #self.team_id=team_id
        self.team_name = team_name
        self.college=college
        self.num_players=num_players
        #self.captain=captain
        self.sportName=sportName
        self.contact=contact

    def json(self, tID,cID):
        return {"team_id":tID, "team_name": self.team_name, "college": self.college, "num_players":self.num_players, "captain_ID":cID, "sportName":self.sportName, "contact":self.contact}

    def save_to_db(self,tID):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("SELECT team_name FROM team where captain IN (SELECT pnum FROM player where tournament_id = %s)",(tID,))
        teams = cur.fetchall()

        for team in teams:
            if team[0] == self.team_name:
                conn.close()
                return None

        cur.execute("INSERT INTO team (team_id, team_name, college, num_players, sportName, status, contact) VALUES (DEFAULT,%s,%s,%s,%s,%s,%s) RETURNING team_id",(self.team_name, self.college, self.num_players,self.sportName, "PENDING", self.contact))
        id_of_new_team = cur.fetchone()[0]

        conn.commit()
        conn.close()

        return id_of_new_team

    def find_by_id(id):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT * FROM team where team_id = %s",(id,))

        row = cur.fetchone()

        conn.close()

        if row:
            return row
        else:
            return None

    def updateCaptainID(self, cID,tID):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("UPDATE team SET captain = %s where team_id = %s",(cID,tID))

        conn.commit()
        conn.close()

    def findCaptainID(self,tID):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT captain FROM team where team_id = %s",(tID,))
        row = cur.fetchone()[0]

        conn.close()

        return row

    def findAll(ID):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT * FROM team where captain in(SELECT pnum from PLAYER where tournament_id = %s)",(ID,))

        rows = cur.fetchall()

        conn.close()

        if rows:
            return rows
        else:
            return None

    def updateStatus( id, stat):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("UPDATE team SET status = %s where team_id = %s",(stat,id))

        conn.commit()
        conn.close()
        
    def removeRejected(self,id):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("DELETE FROM team t where t.status = 'REJECTED' AND t.team_id IN (SELECT p.team_id from player p where p.tournament_id =%s)",(id,))

        conn.commit()

        conn.close() 

    def removeTeam(self,tId):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("DELETE FROM team t where t.team_id=%s",(tId,))

        conn.commit()

        conn.close()

    def find_by_sport(tID,sport):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT * FROM team t where t.sportName = %s AND t.captain IN (SELECT p.pnum from player p where p.tournament_id =%s)",(sport,tID))

        rows = cur.fetchall()
        conn.close()

        if rows:
            return rows
        else:
            return None

    def find_by_status(username,status):
        

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute("SELECT te.team_id, te.team_name, te.college, te.num_players, te.sportname, p.firstname, p.lastname, te.contact, t.tournament_id, t.t_name from team te,tournament t,player p WHERE te.captain = p.pnum and t.tournament_id = p.tournament_id and te.status =%s and t.username = %s",(status,username))

        rows = cur.fetchall()
        conn.close()

        if rows:
            return rows
        else:
            return None        


import os
import sqlite3

class DBWriter(object):
  def __init__(self, dbname):
    if os.path.exists(dbname):
      os.remove(dbname)
    self.connection = sqlite3.connect(dbname)
    self.__init_database()

  def close(self):
    self.connection.commit()
    self.connection.close()

  def __init_database(self):
    c = self.connection.cursor()
    c.execute('''CREATE TABLE individual
              (id text PRIMARY KEY,
              sex text,
              firstname text,
              lastname text,
              birthdate date,
              birthplace text,
              deathdate date,
              deathplace text,
              baptism text,
              baptismplace date,
              childinfamily text,
              note text
              )''')
    c.execute('''CREATE TABLE families
              (id text PRIMARY KEY,
                husband text,
                wife text,
                marriagedate date,
                marriageplace text
              )''')
    self.connection.commit()

  def write_family(self, person):
    c = self.connection.cursor()
    c.execute('''INSERT INTO families VALUES (?,?,?,?,?)''',
              (person["value"],
              person["husband"] if "husband" in person else None,
                  person["wife"] if "wife" in person else None,
                  person["marriagedate"] if "marriagedate" in person else None,
                  person["marriageplace"] if "marriageplace" in person else None,
              ))

  def write_person(self, person):
    c = self.connection.cursor()
    c.execute('''INSERT INTO individual VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
              (person["value"],
              person["sex"] if "sex" in person else None,
                  person["first"],
                  person["last"],
                  person["birthday"] if "birthday" in person else None,
                  person["birthplace"] if "birthplace" in person else None,
                  person["death"] if "death" in person else None,
                  person["deathplace"] if "deathplace" in person else None,
                  person["baptism"] if "baptism" in person else None,
                  person["baptismplace"] if "baptismplace" in person else None,
                  person["childinfamily"] if "childinfamily" in person else None,
                  person["note"] if "note" in person else None
              ))

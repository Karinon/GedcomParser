class Person(object):
  def __init__(self, person):
    self.value = person["value"]
    self.sex = person["sex"] if "sex" in person else None
    self.first = person["first"]
    self.last = person["last"]
    self.birthday = person["birthday"] if "birthday" in person else None
    self.birthplace = person["birthplace"] if "birthplace" in person else None
    self.death = person["death"] if "death" in person else None
    self.deathplace = person["deathplace"] if "deathplace" in person else None
    self.baptism = person["baptism"] if "baptism" in person else None
    self.baptismplace = person["baptismplace"] if "baptismplace" in person else None
    self.childinfamily = person["childinfamily"] if "childinfamily" in person else None
    self.note = person["note"] if "note" in person else None

  def __repr__(self):
    return self.value + ": " + self.first + " " + self.last

class Family(object):
  def __init__(self, fam):
    self.value = fam["value"],
    self.husband = fam["husband"] if "husband" in fam else None
    self.wife = fam["wife"] if "wife" in fam else None
    self.marriagedate = fam["marriagedate"] if "marriagedate" in fam else None
    self.marriageplace = fam["marriageplace"] if "marriageplace" in fam else None

class TableWriter(object):
  def __init__(self):
    self.table = {}

  def close(self):
    print(self.table) 

  def write_family(self, family):
    f = Family(family)
    self.table[family["value"]] = f

  def write_person(self, person):
    p = Person(person)
    self.table[person["value"]] = p
  
  def seek_connection(self, source_id, destination_id):
    pass
    source_node = self.table[source_id] if source_id in self.table else None
    source_node.visited = True
    if not source_node:
      raise Exception("Source node " + source_id + " not found")
    print (source_node.visited)

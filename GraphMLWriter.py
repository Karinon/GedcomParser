import os

class GraphMLWriter(object):
  def __init__(self, filename):
    if os.path.exists(filename):
      os.remove(filename)
    self.graphfile = open(filename, "w")
    self.__write_graph_header()

  def close(self):
    self.__write_graph_footer()
    self.graphfile.close()

  def write_family(self, family):
    edge = 0
    self.graphfile.write("""<node id=\"""" + family["value"] + """">""")
    self.graphfile.write(self.__get_data_node("d0", "family"))
    self.graphfile.write("</node>")
    if "husband" in family:
      self.graphfile.write(
          self.__get_edge(family["value"] + "_" + str(edge), family["husband"], family["value"], "husband"))
    edge = edge + 1
    if "wife" in family:
      self.graphfile.write(
          self.__get_edge(family["value"] + "_" + str(edge), family["wife"], family["value"], "wife"))

  def write_person(self, person):
    self.graphfile.write(self.__get_person_node(person))
    if ("childinfamily" in person):
      family_relation = ""
      if "sex" in person and person["sex"] == "M":
        family_relation = "son"
      elif "sex" in person and person["sex"] == "F":
        family_relation = "daughter"
      else:
        family_relation = "child"
      self.graphfile.write(
          self.__get_edge(person["value"] + "_" + person["childinfamily"], person["childinfamily"], person["value"], family_relation))


  def __get_person_node(self, person):
    node = "<node id=\"{0}\">".format(person["value"])
    person_type = "person"
    if "sex" in person and person["sex"] == "M":
      person_type = "man"
    elif "sex" in person and person["sex"] == "F":
      person_type = "woman"
    node = node + self.__get_data_node("d0", person_type)
    if "birthday" in person:
      node = node + self.__get_data_node("d1", person["birthday"])
    if "death" in person:
      node = node + self.__get_data_node("d2", person["death"])
    if "first" in person:
      node = node + self.__get_data_node("d3", person["first"])
    if "last" in person:
      node = node + self.__get_data_node("d4", person["last"])
    return node + "</node>\n"

  def __get_data_node(self, id, data):
    return """<data key="{0}" xml:space="preserve"><![CDATA[{1}]]></data>\n""".format(id, data)


  def __get_edge(self, id, source, target, relationship = None):
    if relationship is None:
      return "<edge id=\"{0}\" source=\"{1}\" target=\"{2}\"/>\n".format(id, source, target)
    edge = "<edge id=\"{0}\" source=\"{1}\" target=\"{2}\">\n".format(id, source, target)
    edge += self.__get_data_node("e0", relationship)
    edge += "</edge>"
    return edge

  def __write_graph_header(self):
    self.graphfile.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <graphml xmlns="http://graphml.graphdrawing.org/xmlns"
                     xmlns:java="http://www.yworks.com/xml/yfiles-common/1.0/java"
                     xmlns:sys="http://www.yworks.com/xml/yfiles-common/markup/primitives/2.0"
                     xmlns:x="http://www.yworks.com/xml/yfiles-common/markup/2.0"
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xmlns:y="http://www.yworks.com/xml/graphml"
                     xmlns:yed="http://www.yworks.com/xml/yed/3"
                     xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">
                    <key attr.name="TYPE" attr.type="string" for="node" id="d0"/>
                    <key attr.name="BIRT" attr.type="string" for="node" id="d1"/>
                    <key attr.name="DEAT" attr.type="string" for="node" id="d2"/>
                    <key attr.name="FIRST" attr.type="string" for="node" id="d3"/>
                    <key attr.name="LAST" attr.type="string" for="node" id="d4"/>

                    <key attr.name="REL" attr.type="string" for="edge" id="e0"/>
             <graph id="G" edgedefault="undirected">\n""")


  def __write_graph_footer(self):
    self.graphfile.write("""\n</graph></graphml>""")

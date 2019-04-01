import sqlite3
import re
import datetime
from GraphMLWriter import GraphMLWriter
from DBWriter import DBWriter
from TableWriter import TableWriter
from pathlib import Path

dbname = "example.db"
gd_file = "/home/afast/Fast.ged"
#gd_file = "/home/afast/gm6_bkout_UTF8.GED"

LEVEL = 0
KEY = 1
VALUE = 2

placeFieldMapping = {
    "MARR": "marriageplace",
    "DEAT": "deathplace",
    "BIRT": "birthplace",
    "BAPM": "baptismplace",
    "IMMI": "immigrationplace",
    "BURI": "burialplace"
}

dateFieldMapping = {
    "MARR": "marriagedate",
    "DEAT": "death",
    "BIRT": "birthday",
    "BAPM": "baptism",
    "IMMI": "immigrationdate",
    "BURI": "burialdate"
}


def read_gedcom(writer, filename):
  context_stack = []
  former_level = 0
  former_context_tripel = ()
  # regex = re.compile(r"^(\d) (\w{3,4}|@\w@) (.*)$")
  regex = re.compile(r"^(\d) ([A-Z]{3,4}|@\w*@)( .*)?$")
  context = {}
  with open(filename) as myfile:
    for line in myfile:
      parsed_line = regex.search(line)
      if parsed_line:
        level = int(parsed_line.group(1))
        key = parsed_line.group(2)
        value = parsed_line.group(3)
        if value:
          value = value.strip()
        context_tripel = (level, key, value)
        if key[0] == "@":
          # FIXME: Notes
          key, value = value, key

        if level == 0:
          # print(context)
          if ("key" in context and context["key"] == "INDI"):
            for w in writer:
              w.write_person(context)
          if ("key" in context and context["key"] == "FAM"):
            for w in writer:
              w.write_family(context)
          context.clear()
          context["value"] = value
          context["key"] = key

        if (level > former_level):
          context_stack.append(former_context_tripel)
          former_level = level
        elif (level < former_level):
          temp_former_level = former_level
          former_level = level
          while level < temp_former_level:
            context_stack.pop()
            temp_former_level -= 1
        # former_key = key
        former_context_tripel = context_tripel
        if key == "SEX" and context["key"] == "INDI":
          context["sex"] = value
        elif key == "NAME" and context["key"] == "INDI":
          name = parse_name(value)
          first = name[0]
          last = name[1]
          context["first"] = first
          context["last"] = last
        elif key == "HUSB":
          context["husband"] = value
        elif key == "FAMC":
          if "childinfamily" in context:
            print("ERROR: Individual is already a child of a family", context)
          context["childinfamily"] = value
        elif key == "WIFE":
          context["wife"] = value
        elif key == "DATE":
          date_context = context_stack[len(context_stack)-1][KEY]
          if (date_context in dateFieldMapping):
            dateInfo = parse_date(value)
            # print(date_context, dateInfo)
            # if date_context == "DEAT" and dateFieldMapping["BIRT"] in context and dateInfo[0] is not None:
            #     print( dateInfo[0].month, dateInfo[0].month)
            if date_context == "DEAT" and dateFieldMapping["BIRT"] in context and dateInfo[0] is not None and context[dateFieldMapping["BIRT"]] is not None and context[dateFieldMapping["BIRT"]] > dateInfo[0] and dateInfo[0].month == 1 and dateInfo[0].day == 1:
              context[dateFieldMapping[date_context]
                      ] = context[dateFieldMapping["BIRT"]]
            else:
              context[dateFieldMapping[date_context]] = dateInfo[0]
            if dateInfo[1] is not None:
              if ("note" in context):
                context["note"] = context["note"] + "\n" + \
                    dateFieldMapping[date_context] + ": " + dateInfo[1]
              else:
                context["note"] = dateFieldMapping[date_context] + \
                    ": " + dateInfo[1]
        # and context_stack[len(context_stack)-1][LEVEL] == 1:
        elif key == "NOTE" and context["key"] == "INDI":
          if ("note" in context):
            context["note"] = context["note"] + "\n\n" + value.strip()
          else:
            context["note"] = value.strip()
        elif key == "CONC" and context["key"] == "INDI" and context_stack[len(context_stack)-1][KEY] == "NOTE":
          context["note"] = context["note"] + value.strip()
        elif key == "CONT" and context["key"] == "INDI" and context_stack[len(context_stack)-1][KEY] == "NOTE":
          context["note"] = context["note"] + "\n" + value.strip()

          # elif date_context != "CHAN" : print (date_context, value)
        elif key == "PLAC":
          place_context = context_stack[len(context_stack)-1][KEY]
          if (place_context in placeFieldMapping):
            context[placeFieldMapping[place_context]] = value


def parse_content(key, value):
  pass


valid_months = ["JAN", "FEB", "MAR", "APR", "MAY",
                "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
# Does not work
# date_regex = re.compile(r"^(([0-9]{1,2}) +)?((" + r"".join(valid_months)+ r") +)?([0-9]{3,4})$")
date_regex = re.compile(
    r"^(([0-9]{1,2}) +)?((JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC) +)?([0-9]{3,4})$")


def parse_date(value):
  note = None
  if value.startswith("Abt") or value.startswith("Bef") or value.startswith("Aft"):
    note = value
    value = value[3:].strip()
  parsed_line = date_regex.search(value)
  if parsed_line:
    day = parsed_line.group(2)
    month = parsed_line.group(4)
    month_pos = valid_months.index(month) + 1 if month is not None else None
    year = int(parsed_line.group(5))
    date = None
    if day is None and month_pos is None:
      date = datetime.date(year, 1, 1)
    elif day is None:
      date = datetime.date(year, month_pos, 1)
    else:
      # print (parsed_line, year, month_pos, day)
      date = datetime.date(year, month_pos, int(day))
    return (date, note)
  else:
    # print ("COULD NOT PARSE", value)
    return (None, value)


name_regex = re.compile(r"(.*)\/(.*)\/")


def parse_name(name):
  parsed_line = name_regex.search(name)
  if parsed_line:
    first = parsed_line.group(1)
    last = parsed_line.group(2)
    if first:
      first = first.strip()
    if last:
      last = last.strip()
    return (first, last)
  return None

def main():
  graphWriter = GraphMLWriter("workfile.graphml")
  dbWriter = DBWriter(dbname)
  tabWriter = TableWriter()
  writer = []
  writer.append(graphWriter)
  writer.append(dbWriter)
  writer.append(tabWriter)
  read_gedcom(writer, gd_file)
  for w in writer:
    w.close()
  tabWriter.seek_connection("@F81@", "")


main()

import sys
import yaml
import requests
from icalendar import Calendar, Event

in_cals = {}

def read_config(filename):
  """Read YAML config file"""
  with open(filename, 'r') as f:
    return yaml.load(f)

def download_calendar(url):
  """Download and parse ics file"""
  req = requests.get(url)
  cal = Calendar.from_ical(req.text)
  return cal

def read_calendar(filename):
  """Parse local ics file"""
  with open(filename, 'r') as f:
    cal = Calendar.from_ical(f)
  return cal

def write_calendar(options, sources, filename):
  """Create and write ics file"""
  cal = Calendar()
  timezones_cache = []
  for key, value in options.items():
    cal.add(key, value)
  for source_id, category in sources.items():
    for timezone in in_cals[source_id].walk('VTIMEZONE'):
      if timezone['tzid'] not in timezones_cache:
        timezones_cache.append(comp['tzid'])
        cal.add_component(timezone)
    for event in in_cals[source_id].walk('VEVENT'):
      event_copy = Event(event)
      event_copy.add('categories', category)
      cal.add_component(event_copy)
  with open(filename, 'w') as f:
    f.write(cal.to_ical())

def main():
  # Get the name of the config file
  if len(sys.argv) != 2:
    print 'Usage:'
    print '  python merge-ics.py <config_file>'
    return 1
  config_file = sys.argv[1]

  # Read config
  try:
    config = read_config(config_file)
  except IOError:
    print 'Unable to open ' + config_file
    return 1
  except yaml.YAMLError:
    print 'Unable to parse ' + config_file
    return 1

  # Read/download and parse input calendars
  for source_id, source in config['sources'].items():
    if 'filename' in source:
      try:
        in_cals[source_id] = read_calendar(source['filename'])
      except IOError:
        print 'Unable to open ' + source['filename']
      except ValueError:
        print 'Unable to parse ' + source['filename']
    if (source_id not in in_cals) and ('url' in source):
      try:
        in_cals[source_id] = download_calendar(source['url'])
      except requests.exceptions.RequestException:
        print 'Unable to download ' + source['url']
      except ValueError:
        print 'Unable to parse ' + source['url']

  # Create and write output calendars
  for sink in config['sinks']:
    try:
      write_calendar(sink['options'], sink['sources'], sink['filename'])
    except IOError:
      print 'Unable to write ' + sink['filename']
    except ValueError:
      print 'Unable to create calendar ' + sink['filename']

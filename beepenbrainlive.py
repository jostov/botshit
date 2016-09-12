#Remove blog results from search results
#add re-nicknaming function
#turn nicknames into a hash map
#Teach beepboop to love
import sys
from bs4 import BeautifulSoup
import urllib2
import re
import json
import markymark2
from random import randint, choice
beepencampus = "memory.txt"
beepencabulary = "marky.txt"
stuffloc = "swarfarm.txt"
class Beepenbrain:
    knownEntries = []
    stuffList = []
    def __init__(self):
      try:
        self.witty_response_engine = markymark2.MarkyMarkov(location=beepencabulary)
        self.knownEntries = json.load(open(beepencampus, "r"))
        self.stuffList = json.load(open(stuffloc, "r"))
      except IOError:
        print "IOError: assuming no file, will make one later"
        pass 
      except TypeError:
        print "type error: assuming empty file"
        pass
      self.updatecounter = 0

    def find_entry(self, entry):
      phrase = entry
      search = self.search_entries(entry)
      if search is None:
        baseUrl = "http://summonerswar.wikia.com/wiki/Special:Search?search="
        baseUrl = baseUrl + phrase.replace(" ","+") + "&fulltext=Search"
        baseUrl = baseUrl + "&ns0=1&ns112=1&ns114=1&ns500=1&ns502=1#"
        header = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(baseUrl, headers=header)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
        p = soup.find("a", {"class": "result-link"})
        if p is None:
          return "I ain't found shit about no damn '%s' " %phrase
        p = p['href'].replace("(", "%28") #crappy shit, icy made me do it
        p = p.replace(")", "%29") #Crappy shit
        if self.knownEntries.count(p) is 0:
          self.knownEntries.append(p)
        return p
      return search
    def scan(self, message, nickname):
      if message.endswith('?'):
        if randint(0,100) < 10 or "beep" in  message or "Beep" in message:
          self.witty_response_engine.parse_sentence(message[:-1])
          return self.witty_response_engine.shitty_response_estimate(message[:-1]).encode('utf-8')
      if 'kappa' in message:
        return "kappa kappa kappa"
      self.witty_response_engine.parse_sentence(message)
      return None
    def search_entries(self, nickname):
      if nickname is "":
        return "pls do better"
      for each in self.knownEntries:
        if re.search('-\w%s\Z' %nickname, each, re.IGNORECASE) is not None:
          return each
      for each in self.knownEntries:
        if re.search('-\w*%s.*' %nickname, each, re.IGNORECASE) is not None:
          return each
      return None
    def update_file(self, force=False):
      self.updatecounter += 1
      if self.updatecounter > 1000 or force is True:
        with open(beepencampus, 'w') as f:
          json.dump(self.knownEntries, f)
        self.witty_response_engine.rly_store_data(location=beepencabulary)
        self.updatecounter = 0
    #commands go in here
    def command_d(self, rest, nick):
      return nick + ": https://duckduckgo.com/?q="+rest.replace(" ","+")
    def command_fact(self, rest, nick):
      facts = ['llamas are larger than frogs',
               'llamas are dangerous, so if you see one where people are swimming, you shout, "Look out! There are llamas!"',
               'Llamas are quadrupeds that live in big rivers',
               'Llamas have two ears',
               'Llamas have a forehead',
               'Llamas have a heart, but it is blackened and small',
               'Llamas have a beak for eating honey',
               'I\'m sick of llama facts.',
               'Cats are the mammal most closely related to reptiles',
               'Llamas smell funny.',
               'Llamas taste funny.',
               'If you lick a rabbit\'s nose, your tongue tastes weird.',
               'Bananas are nature\'s banana',
               '12 chihuahuas once founded Lithuania',
               'Don\'t stick marbles in your nose',
               'Dogs are the mammal most closely related to reptiles',
               'Licking rabbits noses will convince them to go into \'self-destruct\' mode.',
               'the jews did 9/11',
               'Llamas are also provided with fins for swimming']
      return nick + ": " + choice(facts)
    def command_wiki(self, rest, nick):
      #if randint(0,10) < 5:
        #return "/kick " + nick + " BECAUSE FUCKING REASONS"
      entry = self.find_entry(rest).encode("utf-8")
      if isinstance(entry, unicode):
        print "is unicode"
      return nick + ": " + entry

    def command_necrotips(self,rest,nick):
      return nick + ":def better I think 'cause boss has lifesteal based on damage dealt" 
    def command_rules(self, rest, nick):
      return nick + ": http://pastebin.ubuntu.com/15570612/"
    def command_fusion(self, rest, nick):
      return nick + ": http://i.imgur.com/5bsN3Kt.jpg"

    def command_stuff(self, rest, nick):
      placeholder = []
      for each in self.stuffList:
        dist = self.levenshtein(rest, each[0])
        if len(placeholder) == 0:
          placeholder.append(dist)
          placeholder.append(each)
        elif dist < placeholder[0]:
          placeholder[0] = dist
          placeholder[1] = each
      return placeholder[1][0].encode('UTF-8') + "'s stuff: " + placeholder[1][1].encode('UTF-8')
        
    def command_addstuff(self, rest, nick):
      index = None
      for each in self.stuffList:
        if each[0] == nick:
          index = self.stuffList.index(each)
      else:
        if index is not None:
          self.stuffList[index] = [nick, rest]
        else:
          self.stuffList.append([nick, rest])
        with open(stuffloc, 'w') as f:
          json.dump(self.stuffList, f)
        return nick + "'s stuff has been set to \"" + rest + "\""

    def command_help(self, rest, nick):
      return nick + ": Available commands are !addstuff, !stuff, !fusion !wiki, !necrotips, !rules, !fact, maybe there's more idk damn stop hounding me dawg"
    def command_cmd(self, rest, nick):
      return nick + ": Available commands are !addstuff, !stuff, !fusion !wiki, !necrotips, !rules, !fact, maybe there's more idk damn stop hounding me dawg"

    def levenshtein(self, s, t):
      if s == t:
        return 0
      if len(s) == 0:
        return len(t)
      if len(t) == 0:
        return len(s)

      v0 = list(range(len(t) + 1))
      v1 = [None] * (len(t) + 1)

      for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
          cost = 0 if s[i] == t[j] else 1
          v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
          v0[j] = v1[j]

      return v1[len(t)]


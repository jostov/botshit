import random
#Used for cleaning up things and hopefully lowering memory size
import re
import json
#markymarkov.py
#i have no idea if this works right now
#it's probably a trojan horse.
#neeeeigh!
#nnnnneeeeeeeeeiiiiighhhhh!
#neeeiigh!
#Oh no, it's just a regular horse.
#Nothing to see here, just keep moving along.
class MarkyMarkov:
  def __init__(self, location=None, rawdat=None):
    self.words = {}
    jsondata = None
    if location is not None:
      try:
        jsondata = json.load(open(location, "r"))
      except IOError:
        print "Assuming no known vocabulary"
        jsondata = None
        pass
      except TypeError:
        print "type error: assuming empty file"
        jsondata = None
        pass
    if rawdat is not None and location is None:
      jsondata = json.loads(rawdat)
    if jsondata is not None:
      for each in jsondata['wordlist']:
        self.words[each['k']] = self.WordData(rawdat=each)
    else:
      self.words["_START_"] = self.WordData("_START_", None)
  def parse_sentence(self, sentence):
    #The cleansed sentences shall be known as squeakyclean, because they
    #are squeaky and clean.
    squeakyclean = self.clean_sentence(sentence)
    #The used words shall be known as orphans, because life is tragedy.
    #They too shall be discarded into the abyss
    orphan = "_START_"
    abyss = "_STOP_"
    #I'm gonna explain this one because if you're reading my source,
    #I'm gonna assume some level of mental deficiency to begin with
    #There's better packages out there that do the same fucking thing
    #and they're probably much better commented.
    #ok, so each word, delimited by spaces, is taken out of the sentence
    #and added as a key in a dictionary, while the entry in the dictionary 
    #data about each word, including neighbors, frequency of said neighbors
    #and total occurences of the word.
    for youngbrucewayne in squeakyclean.split():
      if youngbrucewayne != "_STOP_":
        youngbrucewayne = self.wordicide(youngbrucewayne)
      if orphan in self.words:
        self.words[orphan].add_word(youngbrucewayne)
        self.words[orphan].add_preword(abyss)
      else:
        self.words[orphan] = self.WordData(orphan, youngbrucewayne, abyss)
      if youngbrucewayne == "_STOP_":
        break
      #The cycle begins anew
      abyss = orphan
      orphan = youngbrucewayne
  def generate_sentence(self, length=20):
    previous_word = "_START_"
    gibberish = ""
    for i in range(length):
      current_word = self.words[previous_word].next_word()
      if current_word == "_STOP_":
        break
      gibberish += current_word + " "
      previous_word = current_word
    return gibberish
  def shitty_response_estimate(self, sentence, default="I DON'T KNOW WHAT YOU'RE TALKING ABOUT"):
    work = self.clean_sentence(sentence)
    rater = []
    for each in sentence.split():
      if each in self.words:
        rater.append((each, self.words[each].total))
    if len(rater) > 0:
      rater.sort(key=lambda x: x[1])
      free_will = []
      expanse_of_choice = (len(rater) / 3) +1
      for i in range(0,expanse_of_choice):
        free_will.append(rater[i][0])
      return self.find_sentence(random.choice(free_will))
    else:
      return default

  #starts sentence from middle of the sentence
  def find_sentence(self, word, steps=20):
    middle_word = word
    gibberish = middle_word + " "
    pre_word = self.words[middle_word].previous_word()
    nxt_word = self.words[middle_word].next_word()
    for i in range(steps):
      if pre_word != "_START_":
        pre = pre_word + " "
        pre_word = self.words[pre_word].previous_word()
      else:
        pre = ""
      if nxt_word != "_STOP_":
        nxt = nxt_word + " "
        nxt_word = self.words[nxt_word].next_word()
      else:
        nxt = ""
      gibberish = pre + gibberish + nxt
    return gibberish

    
  def wordicide(self, word):
    return re.sub(r'\W+', '', word.lower())
  #I suspect this is a poor way of dealing with things
  def clean_sentence(self, sentence):
    work = sentence.replace("_STOP_", "")
    work = work.replace("_START_", "")
    return work + " _STOP_"
  def rly_store_data(self, location):
    jsondic = {}
    wordlist = []
    for each in self.words:
      wordlist.append(self.words[each].get_dict())
    jsondic = { "wordlist" : wordlist }
    with open(location, "w" ) as out:
      json.dump(jsondic, out)
  def store_data(self):
    jsondic = {}
    wordlist = []
    for each in self.words:
      wordlist.append(self.words[each].get_dict())
    jsondic = { "wordlist" : wordlist }
    return json.dump(jsondic)

  #Each word is quantified has a dictionary of it's neighbors
  #
  class WordData:
    def __init__(self, key=None, word=None, preword=None, rawdat=None):
      if key is not None:
        self.key = key
      self.total = 0
      self.pre_total = 0
      self.neighbors = []
      self.otherneighbors = []
      if word is not None and preword is not None:
        self.add_preword(preword)
        self.add_word(word)
      if rawdat is not None:
        self.key = rawdat['k']
        self.total = rawdat['t']
        self.pre_total = rawdat['p']
        for each in rawdat['n']:
          self.neighbors.append(self.NeighborData(rawdat=each))
        for each in rawdat['o']:
          self.otherneighbors.append(self.NeighborData(rawdat=each))
    def add_word(self, word):
      for each in self.neighbors:
        if each.compare(word):
          self.total +=1
          break
      else:
        new_word = self.NeighborData(word)
        self.neighbors.append(new_word)
        self.total += 1
        sentence = ""
        for each in self.neighbors:
          sentence += each.get_word() + " "
    #Adds preceding word
    def add_preword(self, word):
      for each in self.otherneighbors:
        if each.compare(word):
          self.pre_total +=1
          break
      else:
        new_word = self.NeighborData(word)
        self.otherneighbors.append(new_word)
        self.pre_total += 1
        sentence = ""
        for each in self.otherneighbors:
          sentence += each.get_word() + " "
    #Gets the previous possible word in the sentence
    def previous_word(self):
      choice = random.randint(0,self.pre_total)
      tracker = 0
      for each in self.otherneighbors:
        tracker += each.get_occurrences()
        if choice <= tracker:
           retval = each.get_word()
           return retval
      else:
        print self.key + " is the key"
        for each in self.otherneighbors:
          print each.get_word() + " is a neighbor"
        raise ReferenceError("Bad Code: no neighbor found for " + self.key)
    #Returns the next word/node to walk to 
    def next_word(self):
      choice = random.randint(0,self.total)
      tracker = 0
      for each in self.neighbors:
        tracker += each.get_occurrences()
        if choice <= tracker:
           retval = each.get_word()
           return retval
      else:
        print self.key + " is the key"
        for each in self.neighbors:
          print each.get_word() + " is a neighbor"
        raise ReferenceError("Bad Code: no neighbor found for " + self.key)
    
    #Returns dictionary for sake of json encoding
    def get_dict(self):
      neighborlist = []
      otherneighborlist = []
      for each in self.neighbors:
        neighborlist.append(each.get_dict())
      for each in self.otherneighbors:
        otherneighborlist.append(each.get_dict())
      return { "k" : self.key,
               "t" : self.total,
               "p" : self.pre_total,
               "n" : neighborlist,
               "o" : otherneighborlist }
    

    #Class for storing data about neighbors
    #Each neighbor quantified by neighbor's key and occurences of key
    class NeighborData:
      def __init__(self, word=None, rawdat=None):
        if word is not None:
          self.occurrences = 1
          self.word = word
        if rawdat is not None:
          self.occurrences = rawdat['o']
          self.word = rawdat['w']
      #Compares string word to neighbor data object, adjusts data
      #if the word is a duplicate
      def compare(self, word):
        if word == self.word:
          self.occurrences += 1
          return True
        return False
      #Returns number of occurrences
      def get_occurrences(self):
        return self.occurrences
      #Returns neighbor's key
      def get_word(self):
        return self.word
      #Returns dictionary for sake of json encoding
      def get_dict(self):
        return { "w" : self.word, "o" : self.occurrences }




if __name__ == '__main__':
  otherthing = MarkyMarkov(location="marky.txt")
  print otherthing.shitty_response_estimate("what is this thing?")
  print otherthing.shitty_response_estimate("really what is this stupid dumb butt thing that has been made?")

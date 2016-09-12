import sys, os, re, beepenbrainlive
from twisted.python import log
from twisted.words.protocols import irc
from twisted.internet import protocol, reactor, defer, endpoints, task
from random import randint
#this is where you want the bot to live.
home = ["#summonerswar"]
#this is the bots name
nickstein = "beepenstein"
#network:port combo or list of them. whatever.
networks = ["irc.mibbit.net:6667"]
#where his memory lives
brainspot = "memory.txt"
#oplist
userlist = ['jats']
class Beepenstein(irc.IRCClient):

  nickname = nickstein
  erroneousNickFallback = nickstein + "_jabroni"
  def __init__(self):
    self.deferred = defer.Deferred()
    self.brain = beepenbrainlive.Beepenbrain()
    self.lastSize = os.stat('beepenbrainlive.py')

  def connectionLost(self, reason):
    self.deferred.errback(reason)

  def signedOn(self):
    for channel in self.factory.channels:
      self.join(channel)

  def irc_307(self, *args):
    if args[1][1] in userlist:
      #fix this later
      self.mode(home[0], True, "o", user=args[1][1])
  def userJoined(self, user, channel):
    nick, _, host = user.partition('!')
    self.whois(nick)
    if 'jats' in nick or 'booty' in nick or 'eskay' in nick:
      print "i tried"
      self._sendMessage(self.command_bppiallhailtheking("junk", "junk"), channel)

  def privmsg(self, user, channel, message):
    brainflag = ''
    nick, _, host = user.partition('!')
    message = message.strip()
    message = self.stripMircColorCodes(message)

    #Triggers for things
    if not message.startswith('!') and not message.startswith('@'):
      brainscan = self.brain.scan(message, nick)
      if channel == self.nickname and brainscan is not None:
        self._sendMessage(brainscan, nick)
        return
      elif brainscan is not None:
        self._sendMessage(brainscan, channel)
        return
      return
    if message.startswith('@'):
      command, sep, rest = message.lstrip('@').partition(' ')
    if message.startswith('!'):
      command, sep, rest = message.lstrip('!').partition(' ')
    if command is not None and "bppi" in command:
      com_loc = self
    else:
      com_loc = self.brain
    func = getattr(com_loc,'command_' + command, None)
    if func is None:
      return
    d = defer.maybeDeferred(func, rest, nick)
    d.addErrback(self._Error)
    if channel == self.nickname:
      d.addCallback(self._sendMessage, nick)
    else:
      d.addCallback(self._sendMessage, channel)

  def stripMircColorCodes(self, line) :
      line = re.sub("\x03\d\d?,\d\d?","",line)
      line = re.sub("\x03\d\d?","",line)
      line = re.sub("[\x01-\x1F]","",line)
      return line

  def _sendMessage(self, msg, target):
      self.msg(target, msg)
      self.brain.update_file()
  def _Error(self, failure):
    return failure.getErrorMessage()
  def command_bppiallhailtheking(self, rest, nick):
    #self.mode("#swsa", True, "o", user="jats")
    return "gz me u asshole"
  def command_bppikicklicksy(self, rest, nick):
    for each in home:
      self.kick(each, "Lyxse", ("DAMN YOU AND YOUR CAMILLA! This kick brought to you by, " + nick))
    return "smells better here now, for some odd reason"
  def command_bppicheckbrain(self, rest, nick):
    if nick == "jats" and self.lastSize != os.stat('beepenbrainlive.py'):
      self.brain.update_file(force=True)
      reload(beepenbrainlive)
      self.brain = beepenbrainlive.Beepenbrain()
      return "brain successfully updated, jats!"
    elif nick == "jats":
      self.brain.update_file(force=True)
      return "my brain is ok"
    else:
      return "GET OUT OF MY HEAD " + nick +"!"






  def kickedFrom(self, channel, kicker, message):
    if channel in home:
      self.join(channel)
      self.msg(kicker, "hey you gonna kick me? what's your problem im a bot this is discrimination, i'm calling the irc authorities on you. man you screwed up bigtime.")
      self.msg(kicker, "no seriously bro, you fucked up big time. i know you. i know where you live")
      self.msg(kicker, "i'm calling the police right now too.")
      self.msg(kicker, "fuckin.. bot hating... sonofa bastard")
      self.msg(kicker, "or daughterofa bastard or whatever, i'm an equal opportunity hatemachine")

class BeepFactory(protocol.ReconnectingClientFactory):
  prime_directive = "beep"
  protocol = Beepenstein
  channels = home

def main(reactor, description):
  endpoint = endpoints.clientFromString(reactor, description)
  factory = BeepFactory()
  d = endpoint.connect(factory)
  d.addCallback(lambda protocol: protocol.deferred)
  return d

if __name__=='__main__':
  networks_adjusted = []
  for each in networks:
    networks_adjusted.append("tcp:"+each)
  log.startLogging(sys.stderr)
  task.react(main, networks_adjusted)


  




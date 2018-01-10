#!/usr/bin/env python2.6

import smtplib,sys,getopt,os,platform
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

"""
  A script and class to help send emails.
"""

class EmailMessage:
  """
    An email message class that can attach files, have multiple recipients, and is easy to use.
  """
  def __init__ (self):
    self.msg = MIMEMultipart()
    self.bodyText = ""
    self.smtpserver = None
    self.attachments = []
    self.toAddrs = []

  def setSMTPServer (self, smtpserver):
    if type(smtpserver) is not str:
      raise TypeError("SMTP Server must be a string")
    self.smtpserver = smtpserver

  def setFromAddr (self, fromAddr):
    if type(fromAddr) is not str:
      raise TypeError("From address must be a string")
    self.msg['From'] = fromAddr

  def setToAddr (self, toAddrs):
    """Set the list of recipients for the email"""
    if type(toAddrs) is not list:
      raise TypeError("This function requires a list of the addresses to send emails to")
    self.toAddrs = toAddrs

  def addToAddr (self, toAddr):
    """Add to the list of recipients for the email"""
    if type(toAddr) is not str:
      raise TypeError("The to-address added to the list must be a str")
    self.toAddrs.append(toAddr)

  def setSubject (self, subject):
    if type(subject) is not str:
      raise TypeError("The subject must be a str")
    self.msg['Subject'] = subject

  def setBody (self, body, html=False):
    if type(body) is not str:
      raise TypeError("The body must be a str")
    self.bodyText = body
    self.isHtml = html

  def setAttach (self, files):
    """Set the list of filenames the class will attach when it is time to send"""
    if type(files) is not list:
      raise TypeError("This function requires a list of str defining files to attach")
    self.attachments = files

  def addAttach (self, fileName):
    """Add a filename to the list of attachments"""
    if type(fileName) is not str:
      raise TypeError("The filename added must be a str")
    self.attachments.append(fileName)

  def sendMessage (self):
    """Send the actual message."""
    self.msg['To'] = COMMASPACE.join(self.toAddrs)
    self.msg['Date'] = formatdate(localtime=True)
    if self.isHtml:
      self.msg.attach( MIMEText(self.bodyText,'html') )
    else:
      self.msg.attach ( MIMEText(self.bodyText) )

    if len(self.attachments) > 0:
      for filename in self.attachments:
        if os.path.isfile(filename):
          part = MIMEBase('application', "octet-stream")
          part.set_payload( open(filename,"rb").read() )
          Encoders.encode_base64(part)
          part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
          self.msg.attach(part)

    assert self.smtpserver is not None, "SMTP Server is not set"
    server = smtplib.SMTP(self.smtpserver)
    server.sendmail(self.msg['From'], self.toAddrs, self.msg.as_string())
    server.quit()



# FOR RUNNING SCRIPT DIRECTLY (below) #######
if __name__ == "__main__":
  # Some options for user
  hostname = platform.uname()[1].upper() #Just used in subject line
  fromaddr = "no-repy@example.local"
  smtpserver = "smtp.example.local"
  toaddrs = []
  options = {"attach":[]}

  def usage ():
    print """
    sendMail [options]
      -s --subject SUBJECT    The subject line
      -b --body FILE          A file containing the body of message
      -a --attach FILE        A file to attach. Can have multiple of these options
      -t --toaddr email       An address to send to
      -f --fromaddr email     The from address
    """

  def getOptions ():
    try:
      opts, args = getopt.getopt(sys.argv[1:], "s:b:a:t:f", ["subject=", "body=", "attach=", "help", "toaddr=", "fromaddr="])
    except getopt.GetoptError, err:
      print str(err)
      usage()
      sys.exit(2)
    for o, a in opts:
      if o in ("--help"):
        usage()
        sys.exit(0)
      elif o in ("-s","--subject"):
        if "subject" not in options:
          options["subject"] = a
      elif o in ("-b", "--body"):
        if "body" not in options:
          options["body"] = a
      elif o in ("-a", "--attach"):
        options["attach"].append(a)
      elif o in ("-t", "--toaddr"):
        toaddrs.append(a)
      elif o in ("-f", "--fromaddr"):
        fromaddr = a
      else:
        assert False, "unhandled option"
    if len(toaddrs) < 1:
      print "You must specify at least one address to send to."
      usage()
      sys.exit(2)

  def readInBody ():
    body = ""
    if os.path.isfile(options["body"]):
      f = open(options["body"],"r")
      body = "".join(f.readlines())
      f.close()
    return body

  def getSubjectAndBody ():
    hasSubject = "subject" in options
    hasBody = "body" in options
    body = ""
    subject = ""
    if hasBody:
      body = readInBody()
    if hasSubject:
      subject = options["subject"]

    promptMessage = ""
    if not hasBody:
      promptMessage = "Please enter the message body below."
      if "subject" not in options:
        promptMessage += "  The first line will become the message subject."
    elif not hasSubject:
      promptMessage = "Please enter your desired subject line for message.  Only the first line will count."
    promptMessage += "  Enter Ctrl-D (unix) or Ctrl-Z (win) when done."

    if not (hasBody and hasSubject):
      print promptMessage
      response = sys.stdin.readlines()
      if len(response) >= 1 and not hasSubject:
        subject = response[0].strip()
        response = response [1:]
      if len(response) >= 1 and not hasBody:
        body = "".join(response)

    return (subject,body)


  getOptions()
  subjectBody = getSubjectAndBody()
  subject = "[%s] %s" % (hostname, subjectBody[0])

  sendMessage = True
  if sendMessage:
    msg = EmailMessage()
    msg.setSMTPServer(smtpserver)
    msg.setFromAddr(fromaddr)
    msg.setToAddr(toaddrs)
    msg.setSubject(subject)
    msg.setBody(subjectBody[1])
    if "attach" in options:
      msg.setAttach(options["attach"])
    msg.sendMessage()
  else:
    print "-------------"
    print "The message"
    msgText = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (fromaddr, COMMASPACE.join(toaddrs), subject))
    msgText = msgText + subjectBody[1]
    print msgText


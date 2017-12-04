#!/usr/bin/env python
#author: kniktas

from termcolor import cprint
from termcolor import colored
import sys

# Idea, classes that you can wrap (RewriteRule, ColorRule, Nested, etc.)
# "number:" : ColorRule(RewriteRule("http://gerrit/#change,"+original),("red",None,None))

class BaseRule:
  def apply (rule, line):
    if rule is not None and isinstance(rule,BaseRule):
      return rule.do(line)
  def do (self, line):
    return line

class RewriteCommitNumber (BaseRule):
  key = "number: "
  length = len(key)
  def __init__ (self, otherRule=None):
    self.otherRule = otherRule
  def do (self, line):
    if self.otherRule is not None:
      line = self.otherRule.do(line)
    stopPoint = line.index(self.key) + self.length
    return line[:stopPoint] + " "+\
          colored("https://gerrit" + line[stopPoint:].rstrip(),"blue",None,["underline"])

class FullLineColor (BaseRule):
  def __init__ (self, color, on_color=None, attr=None, otherRule=None):
    self.color = color
    self.on_color = on_color
    self.attr = attr
    self.otherRule = otherRule
  def do (self, line):
    if self.otherRule is not None:
      line = self.otherRule.do(line)
    return colored(line.rstrip(), self.color, self.on_color, self.attr)

rules = {
  "open:" : {
    "true" : ('blue', None, ['bold']),
    "false" : ('white', None, ['underline'])
  },
  "branch:" : ('green',None,['bold']),
  "status:" : {
    "NEW" : ('grey', 'on_red', ['bold']),
    "MERGED" : ('magenta', None, ['bold']),
  },
  "type:" : FullLineColor('grey','on_white',['bold']),
  "rowCount:" : FullLineColor('grey','on_white',['bold']),
  "runTimeMilliseconds:" : FullLineColor('grey','on_white',['bold']),
  "number:" : RewriteCommitNumber()
}

queryOut = sys.stdin.readlines()

for line in queryOut:
  if line.strip() is "":
    cprint (" ")
    continue
  bline = line.split(None,1)
  key = bline[0]
  if key.strip() in rules:
    rest = bline[1]
    rule = rules[key.strip()]
    if type(rule) is type({}):
      for k in rule.keys():
        v = rule[k]
        if k in rest:
          keyIndex = line.index(key)
          line = line[:keyIndex+ len(key)] + " " + colored(rest.rstrip(), *v)
    elif type(rule) is type(()):
      keyIndex = line.index(key)
      line = line[:keyIndex + len(key)] + " " + colored(rest.rstrip(), *rule)
    elif type(rule) is type(lambda (x): x):
      line = rule(line)
    elif isinstance(rule, BaseRule):
      line = rule.do(line)
  print line.rstrip()



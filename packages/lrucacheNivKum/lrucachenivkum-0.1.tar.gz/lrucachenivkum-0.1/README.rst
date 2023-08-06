To use, simply call
from lrucachenivkum.lrucaheNivKum import LRU

To store value in cache
intialize LRU as:
l= LRU("giveanysize")


Functions:

To put values into the cache:
l.put(integer vaalue)
It does not return anything

To get values from the cache:
l.get(integer value) 
It returns True if value is present, else returns False

To check contents of the cache:
l.contents()
It returns an OrderedDict of all the cache contents
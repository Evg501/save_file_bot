from time import gmtime, strftime
import datetime
import random, string

def randomword(length=10):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def currdate(fm = "%Y-%m-%d-%H-%M-%S"):
    return strftime(fm, gmtime())

def genfname(pref="rep", postf=".csv"):
    return pref + datetime.datetime.now().strftime( "%Y%m%d-%H%M%S" ) + randomword() + postf

# dd.mm.yyyy => yyyy-mm-dd
def format_date_db(s):
    if s!=None:
        d = s.split('.')
        if len(d)>=3:
            return d[2]+'-'+d[1]+'-'+d[0]
    return None

def conv_data(p):
    return datetime.datetime.strptime(p, '%Y%m%d').strftime('%Y-%m-%d')


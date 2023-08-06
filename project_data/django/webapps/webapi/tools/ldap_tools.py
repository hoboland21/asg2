import ldap
from json import dumps
from .api import TZPST
from datetime import datetime, timedelta

ACCESS_SG_1 = [
    b"IS-ASG-DEPLOYMENT",b"IT-AppAdmin"
]
ACCESS_SG_2 = [
    b"WebAppDevTechLeads"
]

ACCESS_SG_3 = [
    b"WebAppDev"
]


def AD_Authenticate(username,password) :
    l = ldap.initialize("ldap://nsauth.pdx.odshp.com")
    try:
        l.protocol_version = ldap.VERSION3
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.simple_bind_s(f"{username}@pdx.odshp.com",password)
    except:
        return False
    finally:
        l.unbind()
        return True


class Ldap(object) :
    def __init__(self,username) :
        self.ldap_check(username)

    def ldap_check(self,username) :
        self.ldap_error = False
        self.results = []
        self.l = ldap.initialize("ldap://nsauth.pdx.odshp.com")
        
        try:
            self.l.protocol_version = ldap.VERSION3
            self.l.set_option(ldap.OPT_REFERRALS, 0)
            bind = self.l.simple_bind_s("CMSearchAD", "WLkjzEaU")
            base = "dc=pdx,dc=odshp,dc=com"
            criteria = f'userPrincipalName={username}@pdx.odshp.com'
            attributes = ['pwdLastSet','lastLogon','lastLogonTimestamp','memberOf']
            self.result = self.l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
            attributes = []
            self.all_result = self.l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
            self.results = [entry for dn, entry in self.result if isinstance(entry, dict)]
            self.all_results = [entry for dn, entry in self.all_result if isinstance(entry, dict)]
        
        except:
            self.ldap_error = True

        finally:
            self.l.unbind()
    
    def show(self,arg) :
        return self.all_results[0][arg]

    def show_time(self, arg) :
        return self.to_timestamp(self.show(arg))

    def authenticate(self,username,password) :
        if not self.ldap_error :
            return self._authenticate(username,password)
    
    def authorized_group(self) :
        for sg in ACCESS_SG_1 :
            if self.results :
                for member in self.results[0]['memberOf'] :
                    if b"OU=Security Groups" in member :
                        if sg in member :
                            return 1
        for sg in ACCESS_SG_2 :
            if self.results :
                for member in self.results[0]['memberOf'] :
                    if b"OU=Security Groups" in member :
                        if sg in member :
                            return 2
        for sg in ACCESS_SG_3 :
            if self.results :
                for member in self.results[0]['memberOf'] :
                    if b"OU=Security Groups" in member :
                        if sg in member :
                            return 3
    
        return 100

    def to_timestamp(self,timestamp):
        timestamp = float(timestamp[0])
        seconds_since_epoch = timestamp/10**7
        loc_dt = datetime.fromtimestamp(seconds_since_epoch)
        loc_dt -= timedelta(days=(1970 - 1601) * 365 + 89)
        return loc_dt

    def password_age(self) :
        pls = self.show_time("pwdLastSet")
        return  (datetime.now() - pls).total_seconds()



#========================================
def ldap_check(request) :
  l = Ldap(request.user)
  request.session["ldap_authorized"]=l.authorized_group()
  

'''

self.results = [entry for dn, entry in self.result if isinstance(entry, dict)]

pwdLastSet = result['pwdLastSet']
print pwdLastSet

pwdLastSet_2 = convert_ad_timestamp(pwdLastSet)

print pwdLastSet_2.strftime("%m/%d/%y %H:%M:%S")
print pwdLastSet_2.strftime("%m/%d/%y %I:%M:%S.%f %p")

# Let's see all of the groups that Moss in in, including nested groups

LDAP Server
ldap://nsauth.pdx.odshp.com

Base DN:
dc=pdx,dc=odshp,dc=com
 
User Attribute:
samaccountname
 
User Name:
CN=CMSearchAD,OU=System User Accounts,DC=pdx,DC=odshp,DC=com
 
WLkjzEaU

l = ldap.initialize("ldap://nsauth.pdx.odshp.com")
try:
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
 
    bind = l.simple_bind_s("zzappadmin06@pdx.odshp.com", "bD9H4UCj9klnbmSX")
 
    base = "dc=example, dc=com"
    criteria = "(&(objectClass=user)(sAMAccountName=username))"
    attributes = ['displayName', 'company']
    result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
    results = [entry for dn, entry in result if isinstance(entry, dict)]
    print results
fina
lly:
    l.unbind()
 

l = ldap.initialize("ldap://nsauth.pdx.odshp.com")
l.protocol_version = ldap.VERSION3
l.set_option(ldap.OPT_REFERRALS, 0)
bind = l.simple_bind_s("zzappadmin06@pdx.odshp.com", "bD9H4UCj9klnbmSX")
 

'''
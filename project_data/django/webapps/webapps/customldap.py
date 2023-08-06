from django_auth_ldap.backend import LDAPBackend

class LDAPBackend1(LDAPBackend):
    settings_prefix = "AUTH_LDAP_1_"
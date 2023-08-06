import json
import requests

class AccountDO(object):
    def __init__(self, droplet_limit=0,
        floating_ip_limit=0, email="", uuid="",
        email_verified=False, status="", status_message=""):
        self.droplet_limit = droplet_limit
        self.floating_ip_limit = floating_ip_limit
        self.email = email
        self.uuid = uuid
        self.email_verified = email_verified
        self.status = status
        self.status_message = status_message

    def __json__(self):
        return {
            'droplet_limit': self.droplet_limit,
            'floating_ip_limit': self.floating_ip_limit,
            'email': self.email,
            'uuid': self.uuid,
            'email_verified': self.email_verified,
            'status': self.status,
            'status_message': self.status_message
        }

    for_json = __json__

    def from_json(cls,json):
        obj = cls()
        obj.droplet_limit = json['droplet_limit']
        obj.floating_ip_limit = json['floating_ip_limit']
        obj.email = json['email']
        obj.uuid = json['uuid']
        obj.email_verified = json['email_verified']
        obj.status = json['status']
        obj.status_message = json['status_message']
        return obj


class DomainDO(object):
    def __init__(self, name="",ttl=0,zone_file=""):
        self.name = name
        self.ttl = ttl
        self.zone_file = zone_file

    def __json__(self):
        return {
            'name': self.name,
            'ttl': self.ttl,
            'zone_file': self.zone_file
        }

    for_json = __json__

    def from_json(cls,json):
        obj = cls()
        obj.name = json['name']
        obj.ttl = json['ttl']
        obj.zone_file = json['zone_file']
        return obj
class DomainRecordDO(object):
    def __init__(self, id=0, type="", name="", data="", priority=None, port=None, ttl=0,weight=None, flags=0, tag=""):
        self.id = id
        self.type = type
        self.name = name
        self.data = data
        self.priority = priority
        self.port = port
        self.ttl = ttl
        self.weight = weight
        self.flags = flags
        self.tag = tag

    def __json__(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'data': self.data,
            'priority': self.priority,
            'port': self.port,
            'ttl': self.ttl,
            'weight': self.weight,
            'flags': self.flags,
            'tag': self.tag
        }

    for_json = __json__

    def from_json(cls,json):
        obj = cls()
        obj.id = json['id']
        obj.type = json['type']
        obj.name = json['name']
        obj.data = json['data']
        obj.priority = json['priority']
        obj.port = json['port']
        obj.ttl = json['ttl']
        obj.weight = json['weight']
        obj.flags = json['flags']
        obj.tag = json['tag']
        return obj

class ClientDOApi(object):
    """
    Class to connect to Digital Ocean API and manage their endpoints

    :param string api_token: The token provided from Digital Ocean to access its API
    """
    def __init__(self, api_token):
        self.__api_url_base = 'https://api.digitalocean.com/v2/'
        self.__api_token = api_token
        self.__headers = {'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__api_token}'}

    def get_account_info(self):
        """
        Method to get information from the digital ocean account

        :returns: a AccountDO object containing account info
        :rtype: AccountDO
        """
        api_url = f'{self.__api_url_base}account'

        response = requests.get(api_url, headers=self.__headers)

        if response.status_code == 200:
            account = json.loads(response.content.decode('utf-8'))
            account = account["account"]
            account_info = AccountDO()
            account_info.droplet_limit = account["droplet_limit"]
            account_info.email = account["email"]
            account_info.floating_ip_limit = account["floating_ip_limit"]
            account_info.uuid = account["uuid"]
            account_info.email_verified = account["email_verified"]
            account_info.status = account["status"]
            account_info.status_message = account["status_message"]

            return account_info
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def get_domains(self):
        """
        Method to get a domains list

        :returns: a list with DomainDO objects containing domain info as name, ttl and zone_file
        :rtype: list
        """
        api_url = f'{self.__api_url_base}domains'

        domains = []
        response = requests.get(api_url, headers=self.__headers)

        if response.status_code == 200:
            domain_list = json.loads(response.content.decode('utf-8'))
            domain_list = domain_list["domains"]

            for dom in domain_list:
                domain = DomainDO()
                domain.name = dom["name"] 
                domain.ttl = dom["ttl"]
                domain.zone_file = dom["zone_file"]
                domains.append(domain)

            return domains
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def create_domain(self, name, ip_address):
        api_url = f'{self.__api_url_base}domains'
        
        new_domain = { "name": name, "ip_address": ip_address }

        response = requests.post(api_url, headers=self.__headers, json=new_domain)

        if response.status_code == 201:
            domain_created = json.loads(response.content.decode('utf-8'))
            domain_created = domain_created["domain"]

            domain = DomainDO()

            domain.name = domain_created["name"] 
            domain.ttl = domain_created["ttl"]
            domain.zone_file = domain_created["zone_file"]

            return domain
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def get_domain(self, domain_name):
        api_url = f'{self.__api_url_base}domains/{domain_name}'

        response = requests.get(api_url, headers=self.__headers)

        if response.status_code == 200:
            domain_response = json.loads(response.content.decode('utf-8'))
            domain_response = domain_response["domain"]

            domain = DomainDO()
            domain.name = domain_response["name"]
            domain.ttl = domain_response["ttl"]
            domain.zone_file = domain_response["zone_file"].splitlines()

            return domain
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def delete_domain(self, domain_name):
        api_url = f'{self.__api_url_base}domains/{domain_name}'

        response = requests.delete(api_url, headers=self.__headers)

        if response.status_code == 204:
            return response.status_code
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def get_domain_records(self, domain_name):
        api_url = f'{self.__api_url_base}domains/{domain_name}/records'

        domain_records = []

        response = requests.get(api_url, headers=self.__headers)

        if response.status_code == 200:
            record_list = json.loads(response.content.decode('utf-8'))
            record_list = record_list["domain_records"]

            for rec in record_list:
                domain_record = DomainRecordDO()
                domain_record.id = rec["id"]
                domain_record.type = rec["type"]
                domain_record.name = rec["name"]
                domain_record.data = rec["data"]
                domain_record.priority = rec["priority"]
                domain_record.port = rec["port"]
                domain_record.ttl = rec["ttl"]
                domain_record.weight = rec["weight"]
                domain_record.flags = rec["flags"]
                domain_record.tag = rec["tag"]
                domain_records.append(domain_record)

            return domain_records
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

    def create_domain_record(self,domain_name, type, record_name, data, priority, port, ttl, weight, flags, tag):
        api_url = f'{self.__api_url_base}domains/{domain_name}/records'
        
        new_record = { "type": type, "name": record_name, "data": data, "priority": priority, "port": port, "ttl": ttl, "weight": weight, "flags": flags, "tag": tag }

        response = requests.post(api_url, headers=self.__headers, json=new_record)

        if response.status_code == 201:
            record_created = json.loads(response.content.decode('utf-8'))
            record_created = record_created["domain_record"]

            domain_record = DomainRecordDO()

            domain_record.id = record_created["id"]
            domain_record.type = record_created["type"]
            domain_record.name = record_created["name"]
            domain_record.data = record_created["data"]
            domain_record.priority = record_created["priority"]
            domain_record.port = record_created["port"]
            domain_record.ttl = record_created["ttl"]
            domain_record.weight = record_created["weight"]
            domain_record.flags = record_created["flags"]
            domain_record.tag = record_created["tag"]

            return domain_record
        else:
            raise ConnectionError(f'''Code: {response.status_code} Message: {response.reason} Text: {response.text}''')

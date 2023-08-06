import json
import requests
import time
from requests.auth import HTTPBasicAuth

domain = '.elastichosts.com'

class Node:
  # TODO: Handle disk size on VM
  def __init__(self, params):
    default = {
      'name': None,
      'type': 'container',
      'distro': 'debian9',
      'cpusize': 500,
      'disksize': 10,
      'memsize': 512,
      'persistent': False,
      'disk': None,
      'net': {}
    }
    default.update(params)
    self.params = default
    pass

  def get_params(self):
    return self.params

  def node_to_json(self):
    res = {
      'name': self.params['name'],
      'type': self.params['type'],
      'mem': self.params['memsize'],
      'cpu': self.params['cpusize'],
      'nic:0:model': 'e1000',
      'nic:0:dhcp': 'auto',
      'password': 'Tr0l0l0'
    }
    if self.params['type'] is 'vm':
      res['boot'] = 'ide:0:0'
      res['ide:0:0'] = self.params['disk']
      res['vnc'] = 'auto'
    else:
      res['fs:0:mount'] = '/'
      res['fs:0'] = self.params['disk']
      if self.params['persistent']:
        res['persistent'] = True
    return res

  def json_to_node(self, data):
    # IN: json input (from server/create API)
    # OUT: a dict of node params
    # This also renames container-specific attributes such as 'fs:0'
    # into generic ones, e.g. 'disk'
    res = {
      'name': data['name'],
      'id': data['server'],
      'type': data['type'],
      'disk': data['fs:0'],
      'ip': data['nic:0:ip'],
      'cpu': data['cpu']
    }

    if data['type'] is 'vm':
      pass
    else:
      pass
    return res

class Client:
  def __init__(self, zone, user, pwd, debug=False):
    self.debug = debug
    self.req = Request(zone, user, pwd, debug=debug)

  def log(self, msg):
    if self.debug:
      print(msg)

  def create_node(self, params):
    # Create node ('container' or 'vm')
    try:
      # Get disk for distro
      node = Node(params)
      params = node.get_params()
      disk_img = self.get_disk_for_distro(params['distro'], params['type'])
    except Exception as e:
      raise Exception('No disk for distro {}'.format(params['distro']))

    # Create disk, and sync distro to it
    params['disk'] = self.clone_disk(disk_img, params)
    while self.is_cloning(params['disk'], params['type']):
      time.sleep(2)

    node = Node(params)
    data = node.node_to_json()
    ret = self.req.post('/servers/create', data)
    return node.json_to_node(ret)

  def clone_disk(self, disk_img, params):
    # Returns disk id
    disk_data = { 'name': params['name'] }
    if params['type'] is 'vm':
      disk_data['size'] = params['size']
      url = '/drives/{}/clone/gunzip'.format(disk_img)
    else:
      url = '/folders/{}/clone'.format(disk_img)
    disk = self.req.post(url, disk_data)
    if params['type'] is 'vm':
      return disk['drive']
    else:
      return disk['folder']

  def echo_node(self, params):
    # Dummy method, echo given params
    return params

  def get_disk_for_distro(self, distro, app_type):
    # Return uuid of distro's disk image
    #   app_type: 'vm', 'container'
    #   distro: e.g. 'debian9'
    self.log('Get image for {}'.format(distro))
    if app_type is 'vm':
      url = '/drives/info/standard'
    else:
      url = '/folders/info/standard'
    try:
      l = self.req.get(url)
    except Exception as e:
      raise Exception('Could not get standard disks')

    for i in l:
      if i['name'].startswith('Debian 9'):
        if app_type is 'vm':
          return i['drive']
        else:
          return i['folder']
    # /for
    raise Exception('Could not find distro')

  def get_servers(self):
    return self.req.get('/servers/list')

  def is_cloning(self, uuid, app_type):
    # Given uuid of a disk, return True if the disk is cloning
    # app_type = 'vm' or 'container'
    if app_type is 'vm':
      if 'imaging' in self.req.get('/drives/{}/info'.format(uuid)).keys():
        return True
    else:
      if 'syncing' in self.req.get('/folders/{}/info'.format(uuid)).keys():
        return True
    return False

class Request:
  def __init__(self, zone, user, pwd, debug=False):
    self.url = 'https://api.' + zone + domain
    self.auth = HTTPBasicAuth(user, pwd)
    self.debug = debug

  def log(self, msg):
    if self.debug:
      print(msg)

  # PRIVATE
  # HTTP REST wrappers
  def get(self, url):
    return self.request('GET', url)

  def post(self, url, data):
    return self.request('POST', url, data)

  # Request
  def request(self, method, url, data=None):
    url = self.url + url
    self.log('{} {}'.format(method, url))
    headers = {'Accept': 'application/json'}
    try:
      if method == 'POST' and data != None:
        self.log('DATA')
        self.log(json.dumps(data, indent=2))
        f = requests.post(url, auth=self.auth, headers=headers, json=data)
      else:
        f = requests.get(url, auth=self.auth, headers=headers)
      f.raise_for_status()
      return json.loads(f.text)
    except requests.exceptions.HTTPError as e:
      print('%s' %e)
      raise e
    except requests.exceptions.RequestException as e:
      print('Other error: %s' %e)

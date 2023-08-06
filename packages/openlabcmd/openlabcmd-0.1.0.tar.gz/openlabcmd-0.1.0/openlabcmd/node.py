import json


class NodeStatus(object):
    INITIALIZING = 'initializing'
    UP = 'up'
    DOWN = 'down'
    MAINTAINING = 'maintaining'


class Node(object):
    def __init__(self, name, role, type, ip, heartbeat=None, alarmed=None,
                 status=None, **kwargs):
        self.name = name
        self.role = role
        self.type = type
        self.ip = ip
        self.heartbeat = heartbeat if heartbeat else 0
        self.alarmed = alarmed if alarmed else False
        self.status = status if status else NodeStatus.INITIALIZING

    def to_zk_data(self):
        node_dict = {
            'name': self.name,
            'role': self.role,
            'type': self.type,
            'ip': self.ip,
            'heartbeat': self.heartbeat,
            'alarmed': self.alarmed,
            'status': self.status
        }
        return json.dumps(node_dict).encode('utf8')

    @ classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)

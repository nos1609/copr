# coding: utf-8

from pprint import pformat
from . import KEY_VM_INSTANCE


class VmDescriptor(object):
    def __init__(self, vm_ip, vm_name, group, state):
        self.vm_ip = vm_ip
        self.vm_name = vm_name
        self.state = state
        self.group = group

        # self.last_health_check = None
        # self.last_release = None
        # self.in_use_since = None
        # self.terminating_since = None
        #
        self.bound_to_user = None

    def __str__(self):
        return pformat(self.__dict__)

    def to_dict(self):
        return {str(k): str(v) for k, v in self.__dict__.items() if v is not None}

    @classmethod
    def from_dict(cls, raw):
        vmd = cls(raw["vm_ip"], raw["vm_name"], raw["group"], raw["state"])
        vmd.__dict__.update(raw)
        return vmd

    @classmethod
    def load(cls, rc, vm_name):
        raw = rc.hgetall(KEY_VM_INSTANCE.format(vm_name=vm_name))
        if raw is None:
            raise Exception("VmDescriptor for `{}` not found".format(vm_name))
        return cls.from_dict(raw)

    def store(self, rc):
        """
        :type rc: StrictRedis
        """
        rc.hmset(KEY_VM_INSTANCE.format(vm_name=self.vm_name), self.__dict__)

    def store_field(self, rc, field, value):
        """
        :type rc: StrictRedis
        """
        setattr(self, field, value)
        rc.hset(KEY_VM_INSTANCE.format(vm_name=self.vm_name), field, value)

    def get_field(self, rc, field):
        """
        :type rc: StrictRedis
        """
        value = rc.hget(KEY_VM_INSTANCE.format(vm_name=self.vm_name), field)
        setattr(self, field, value)
        return value
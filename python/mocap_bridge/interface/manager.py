from mocap_bridge.interface.rigid_body import RigidBody
from mocap_bridge.interface.skeleton import Skeleton
from mocap_bridge.utils.event import Event

class Manager:
    _instance = None

    def instance(*args, **kargs):
        if not Manager._instance:
            Manager._instance = Manager(*args, **kargs)
        return Manager._instance

    def __init__(self):
        self.rigid_bodies = {}
        self.skeletons = {}

        # Events
        self.updateEvent = Event()
        self.updateRigidBodyEvent = Event()
        self.newRigidBodyEvent = Event()

        self.startTime = None

    # === === ===
    # RigidBodies
    # === === ===

    # fetchers
    def allRigidBodies(self):
        return self.rigid_bodies.values()

    def rigidBodyById(self, id):
        try:
            return self.rigid_bodies[id]
        except KeyError:
            return None

    def getOrCreateRigidBody(self, id):
        rigid_body = self.rigidBodyById(id)

        if rigid_body == None:
            rigid_body = RigidBody(id)
            self.addRigidBody(rigid_body)

        return rigid_body

    # adders

    def addRigidBody(self, rigid_body):
        existing = self.rigidBodyById(rigid_body.id)

        if existing != None:
            existing.copy(rigid_body)
            self.updateRigidBodyEvent(rigid_body)
        else:
            self.rigid_bodies[rigid_body.id] = rigid_body
            self.newRigidBodyEvent(rigid_body)

        self.updateEvent(self)

    # just an alias with a more explicit name
    def addOrUpdateRigidBody(self, rigid_body):
        self.addRigidBody(rigid_body)

    # RAW data processors, these are convenience methods,
    # so the calling class doesn't necessarily have to know
    # about the mocap interface proprietary data classes

    def processRigidBodyJson(self, json):
        rb = RigidBody().fromJSON(json)
        self.addOrUpdateRigidBody(rb)

    def processRigidBodyObject(self, obj):
        rb = RigidBody().fromObject(obj)
        self.addOrUpdateRigidBody(rb)

    # this
    def addRigidBodiesCallback(self, callback):
        # register callback for both new and update events
        self.updateRigidBodyEvent += callback
        self.newRigidBodyEvent += callback

        # and invoke callback for every rigid body already in the system
        for rigid_body in self.rigid_bodies:
            callback(rigid_body)

    #
    # skeletons
    #

    def skeletonById(self, id):
        try:
            return self.skeletons[id]
        except KeyError:
            return None

    def getOrCreateSkeleton(self, id):
        skeleton = self.skeletonById(id)

        if skeleton == None:
            skeleton = Skeleton(id)
            self.addSkeleton(skeleton)

        return skeleton

    def addSkeleton(self, skeleton):
        existing = skeletonById(skeleton.id)
        if existing != None:
            existing.copy(skeleton)
        else:
            self.skeletons[skeleton.id] = skeletonById

        self.updateEvent(self)

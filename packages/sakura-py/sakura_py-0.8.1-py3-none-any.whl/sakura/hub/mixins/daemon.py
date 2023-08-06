from sakura.hub.context import get_context
from sakura.common.errors import APIRequestErrorOfflineDaemon

class DaemonMixin:
    APIS = {}

    @property
    def api(self):
        if not self.enabled:
            raise APIRequestErrorOfflineDaemon('Daemon is offline!')
        return DaemonMixin.APIS[self.name]

    @property
    def disabled_message(self):
        if self.enabled:
            raise AttributeError
        return 'Sakura daemon "%s" is disconnected!' % self.name

    @api.setter
    def api(self, value):
        DaemonMixin.APIS[self.name] = value

    # Property 'enabled' is not stored in database.
    # It should be 'volatile'.
    # Each time the hub starts it considers all
    # daemons are disconnected (which is obviously true).
    @property
    def enabled(self):
        return self.name in DaemonMixin.APIS

    def save_api(self, api):
        self.api = api

    def on_connect(self):
        # restore according to up-to-date info from daemon
        daemon_info = self.api.get_daemon_info_serializable()
        self.restore(**daemon_info)

    def on_disconnect(self):
        # unregister api object
        del DaemonMixin.APIS[self.name]
        # notify related objects
        for cls in self.op_classes:
            cls.on_daemon_disconnect()
        for ds in self.datastores:
            ds.on_daemon_disconnect()

    def pack(self):
        return dict(
            name = self.name,
            datastores = self.datastores,
            op_classes = self.op_classes,
            **self.pack_status_info()
        )

    @classmethod
    def get_or_create(cls, name):
        daemon = cls.get(name = name)
        if daemon is None:
            daemon = cls(name = name)
            # we will need an up-to-date daemon id
            get_context().db.commit()
        return daemon

    def restore(self, name, datastores, op_classes, **kwargs):
        context = get_context()
        # update metadata
        self.set(**kwargs)
        # restore datastores and related components (databases, tables, columns)
        self.datastores = set(context.datastores.restore_datastore(self, **ds) for ds in datastores)
        # restore op classes
        self.op_classes = set(context.op_classes.restore_op_class(self, **cls) for cls in op_classes)
        # re-instanciate op instances and their parameters
        for op_cls in self.op_classes:
            for op in op_cls.op_instances:
                op.instanciate_on_daemon()
        # re-instanciate links when possible
        for op_cls in self.op_classes:
            for op in op_cls.op_instances:
                op.restore_links()

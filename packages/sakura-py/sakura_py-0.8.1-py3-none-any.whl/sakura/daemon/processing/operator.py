import inspect
from pathlib import Path
from sakura.common.io import pack
from sakura.daemon.processing.plugs.input import InputPlug
from sakura.daemon.processing.plugs.output import OutputPlug
from sakura.daemon.processing.tab import Tab
from gevent.lock import Semaphore

class Operator:
    IGNORED_FILENAMES = ("__pycache__", ".DS_Store")
    def __init__(self, op_id):
        self.op_id = op_id
        operator_py_path = Path(inspect.getabsfile(self.__class__))
        self.root_dir = operator_py_path.parent
        self.event_lock = Semaphore()
        self.opengl_apps = []
    # overridable dynamic properties
    @property
    def input_plugs(self):
        return getattr(self, '_input_plugs', ())
    @property
    def output_plugs(self):
        return getattr(self, '_output_plugs', ())
    @property
    def internal_plugs(self):
        return getattr(self, '_internal_plugs', ())
    @property
    def parameters(self):
        return getattr(self, '_parameters', ())
    @property
    def tabs(self):
        return getattr(self, '_tabs', ())
    # static properties
    def register_input(self, input_plug_label):
        return self.register('_input_plugs', InputPlug(input_plug_label))
    def register_output(self, *args, condition = None, **kwargs):
        if condition is None:
            condition = self.is_ready
        return self.register('_output_plugs', OutputPlug(*args, condition = condition, **kwargs))
    def register_internal_plug(self, *args, **kwargs):
        return self.register('_internal_plugs', OutputPlug(*args, **kwargs))
    def register_parameter(self, param):
        return self.register('_parameters', param)
    def register_tab(self, tab_label, html_path):
        return self.register('_tabs', Tab(tab_label, html_path))
    def register_opengl_app(self, ogl_app):
        ogl_id = len(self.opengl_apps)
        url = '/streams/%d/opengl/%d/video.mjpeg' % (self.op_id, ogl_id)
        ogl_app.url = url
        ogl_app.init()
        self.opengl_apps.append(ogl_app)
    # other functions
    def register(self, container_name, obj):
        container = getattr(self, container_name, [])
        container.append(obj)
        setattr(self, container_name, container)
        return obj
    def is_ready(self):
        for plug in self.input_plugs:
            if not plug.connected():
                return False
        for parameter in self.parameters:
            if not parameter.selected():
                return False
        return True
    def descriptor(op_cls):
        return dict(
                name = op_cls.NAME,
                short_desc = op_cls.SHORT_DESC,
                tags = op_cls.TAGS,
                icon = op_cls.ICON)
    def get_num_parameters(self):
        return len(self.parameters)
    def pack(self):
        return pack(dict(
            op_id = self.op_id,
            cls_name = self.NAME,
            parameters = self.parameters,
            inputs = self.input_plugs,
            outputs = self.output_plugs,
            internal_plugs = self.internal_plugs,
            tabs = self.tabs,
            opengl_apps = tuple(app.label for app in self.opengl_apps)
        ))
    def auto_fill_parameters(self, plug = None):
        for param in self.parameters:
            # restrict to parameters concerning the specified plug if any
            if plug != None and not param.is_linked_to_plug(plug):
                continue
            param.recheck()
    def check_input_compatibility_parameters(self, plug):
        for param in self.parameters:
            if param.is_linked_to_plug(plug):
                if not param.check_input_compatible():
                    return False
        return True
    def unselect_parameters(self, plug = None):
        for param in self.parameters:
            # restrict to parameters concerning the specified plug if any
            if plug != None and not param.is_linked_to_plug(plug):
                continue
            param.unset_value()
    def serve_file(self, request):
        return request.serve(str(self.root_dir))
    def get_file_content(self, file_path):
        with (self.root_dir / file_path).open() as f:
            return f.read()
    def get_file_tree(self, path=None):
        if path == None:
            path = self.root_dir
        return tuple(self.iterate_file_tree(path))
    def iterate_file_tree(self, p):
        for f in p.iterdir():
            if f.name in Operator.IGNORED_FILENAMES:
                continue
            if f.is_dir():
                yield dict(
                    name = f.name,
                    is_dir = True,
                    dir_entries = self.get_file_tree(f)
                )
            else:
                yield dict(
                    name = f.name,
                    is_dir = False
                )
    def save_file_content(self, file_path, file_content):
        with (self.root_dir / file_path).open('w') as f:
            f.write(file_content)

    def new_file(self, file_path, file_content):
        self.save_file_content(file_path, file_content)

    def new_directory(self, dir_path):
        (self.root_dir / dir_path).mkdir()

    def move_file(self, file_src, file_dst):
        (self.root_dir / file_src).rename(
                    self.root_dir / file_dst)

    def delete_file(self, path):
        self.delete_abs_file(self.root_dir / path)

    def delete_abs_file(self, p):
        if p.is_dir():
            for f in p.iterdir():
                self.delete_abs_file(f)
            p.rmdir()
        else:
            p.unlink()
    def sync_handle_event(self, *args, **kwargs):
        # operators handle events one at a time
        # (easier for the operator developer)
        with self.event_lock:
            return self.handle_event(*args, **kwargs)
    def set_check_mode(self, check_mode):
        for parameter in self.parameters:
            parameter.set_check_mode(check_mode)

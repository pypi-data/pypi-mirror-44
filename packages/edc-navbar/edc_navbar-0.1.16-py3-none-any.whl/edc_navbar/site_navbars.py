import sys
import copy

from django.apps import apps as django_apps
from django.core.management.color import color_style
from django.utils.module_loading import module_has_submodule
from importlib import import_module

from .navbar import NavbarError


class PermissionsCodenameError(Exception):
    pass


class AlreadyRegistered(Exception):
    pass


class NavbarCollection:

    """A class to contain a dictionary of navbars. See Navbar.
    """

    name = "default"

    def __init__(self):
        self.registry = {}
        self.permission_codenames = {}

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def register(self, navbar=None):
        if navbar.name not in self.registry:
            self.registry.update({navbar.name: navbar})
            self.permission_codenames.update(**navbar.permission_codenames)
        else:
            raise AlreadyRegistered(
                f"Navbar with name {navbar.name} is already registered."
            )

    def context(self, name=None, selected_item=None):
        """Returns the named navbar in the collection as context.
        """
        return dict(
            navbar_item_selected=selected_item,
            navbar=self.get_navbar(name=name, selected_item=selected_item),
            navbar_name=name,
        )

    def get_navbar(self, name=None, selected_item=None):
        """Returns a selected navbar in the collection.
        """
        # does navbar exist?
        try:
            navbar = self.registry[name]
        except KeyError:
            raise NavbarError(
                f"Navbar '{name}' does not exist. Expected one of "
                f"{list(self.registry.keys())}. See {repr(self)}."
            )
        else:
            # does navbar have items?
            if not [item.name for item in navbar]:
                raise NavbarError(
                    f"Navbar '{navbar.name}' has no items. Expected "
                    f"'{selected_item}'. See {repr(self)}"
                )
            # does selected item exist?
            if selected_item:
                if selected_item not in [navbar_item.name for navbar_item in navbar]:
                    navbar_item_names = [item.name for item in navbar]
                    raise NavbarError(
                        f"Navbar item name does not exist. Got '{selected_item}'. "
                        f"Expected one of {navbar_item_names}. "
                        f"See navbar '{navbar.name}'."
                    )
        return navbar

    def update_permission_codenames(self, verbose=None):
        """Recreates auth.permission objects for the Navbar
        models.
        """
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Navbar

        write = str if verbose is False else sys.stdout.write
        content_type = ContentType.objects.get_for_model(Navbar)
        Permission.objects.filter(content_type=content_type).delete()
        for app_codename, name in self.permission_codenames.values():
            try:
                app_label, codename = app_codename.split(".")
            except ValueError as e:
                raise PermissionsCodenameError(
                    f"Invalid Navbar codename. Expected format "
                    f"'edc_navbar.<some_codename>'. Got {app_codename}. ({e})"
                )
            if app_label != "edc_navbar":
                raise PermissionsCodenameError(
                    f"Invalid Navbar codename. Expected an app_label prefix of "
                    f"'edc_navbar' as prefix. Got {app_codename}."
                )
            write(f'  - adding {app_codename} "{name}" to Permissions.\n')
            Permission.objects.create(
                codename=codename, name=name, content_type=content_type
            )

    def show_user_permissions(self, username=None, navbar_name=None):
        user = django_apps.get_model("auth.user").objects.get(username=username)
        navbar = self.registry.get(navbar_name)
        return navbar.show_user_permissions(user=user)

    def show_user_codenames(self, username=None, navbar_name=None):
        user_permissions = self.show_user_permissions(username, navbar_name)
        codenames = []
        for l in [list(v.keys()) for v in user_permissions.values()]:
            codenames.extend(l)
        return codenames

    def autodiscover(self, module_name=None, verbose=True):
        module_name = module_name or "navbars"
        writer = sys.stdout.write if verbose else lambda x: x
        style = color_style()
        writer(f" * checking for site {module_name} ...\n")
        for app in django_apps.app_configs:
            writer(f" * searching {app}           \r")
            try:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_navbars.registry)
                    import_module(f"{app}.{module_name}")
                    writer(f" * registered navbars '{module_name}' from '{app}'\n")
                except NavbarError as e:
                    writer(f"   - loading {app}.navbars ... ")
                    writer(style.ERROR(f"ERROR! {e}\n"))
                except ImportError as e:
                    site_navbars.registry = before_import_registry
                    if module_has_submodule(mod, module_name):
                        raise NavbarError(e)
            except ImportError:
                pass


site_navbars = NavbarCollection()

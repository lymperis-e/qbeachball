import os
import sys

plugin_dir = os.path.dirname(__file__)
site_packages = os.path.join(plugin_dir, "site-packages")


def init_site_packages() -> str:
    """
    Initialize the site-packages directory for the plugin and return its path.
    """
    if not os.path.exists(site_packages):
        os.makedirs(site_packages)

    sys.path.append(site_packages)
    return site_packages

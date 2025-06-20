"""
Check if required packages are installed and prompt user to install them if not.
"""

import importlib
import os
import sys

from qgis.PyQt.QtWidgets import QMessageBox


def install(package, target=None):
    target_str = f" --target {target}" if target else ""
    print(f"pip install {package} {target_str}")
    os.system(f"pip install {package} {target_str}")
    try:
        if target:
            sys.path.append(target)
        importlib.import_module(package)
        return True
    except ImportError:
        return False


def check(required_packages, target=None):
    # Check if required packages are installed
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)

    if not missing_packages:
        return True

    # If any required packages are missing, prompt user to install them

    message = (
        "The following Python packages are required to use the qbeachball plugin:\n\n"
    )
    message += "\n".join(missing_packages)
    message += "\n\nWould you like to install them now?"
    message += f"\n\n (target dir: {target})"

    reply = QMessageBox.question(
        None,
        "Missing Dependencies",
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if reply == QMessageBox.No:
        return False

    success = False
    for package in missing_packages:
        success = install(package, target)
        if not success:
            QMessageBox.critical(
                None,
                "Error",
                f"Failed to install the required package ({package}). Please install manually.",
            )
            break

    return success

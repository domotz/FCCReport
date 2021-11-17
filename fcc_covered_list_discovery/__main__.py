import logging
import subprocess
from os.path import join, dirname
from subprocess import check_output

try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain


def assure_installed():
    with open(join(dirname(__file__), "..", "requirements.txt")) as requirements:
        for requirement in requirements:
            requirement = requirement.strip()
            if not requirement or requirement.startswith("#"):
                continue
            check_output(["pip", "install", requirement], stderr=subprocess.STDOUT)


if __name__ == "__main__":
    try:
        import fire
        import xlsxwriter
        import requests
    except ModuleNotFoundError:
        assure_installed()
        import fire
        import xlsxwriter
        import requests
    from .ban_reporter import BanReporter

    logging.basicConfig(level=logging.INFO)
    fire.Fire(BanReporter)

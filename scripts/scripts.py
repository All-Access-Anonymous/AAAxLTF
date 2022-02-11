"""
Scripts to be used by Python Poetry
"""
import subprocess as sp
import sys

def run_pylint() -> None:
    """
    Run Pylint with the configuration for Pylint
    sourced from the config used for the Github Workflow itself.
    That way, you don't to push your commit and wait for Github
    to raise an error.
    """

    try:
        sp.run("pylint --rcfile=.github/linters/.python-lint aaa/*", check=True, shell=True)
    except sp.CalledProcessError as error:
        print(f"error")
        sys.exit(1)


def run_pytest() -> None:

    try:
        sp.run("pytest", check=True, shell=True)
    except sp.CalledProcessError as error:
        print(f"error")
        sys.exit(1)


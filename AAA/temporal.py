
import abc
from typing import List

class Temporal(metaclass=abc.ABCMeta):
    """
    Abstract Base Class designed to be inherited
    by a Class that is affected by time in the simulation.
    Any class that inherits Temporal and invokes its constructor,
    are added to a global list of instances that execute day_pass(),
    completely eliminating the need for objects depending on parent objects
    to manage their time-based behaviours.
    """

    instances: List = []

    @abc.abstractmethod
    def __init__(self) -> None:
        Temporal.instances.append(self)

    @abc.abstractmethod
    def run_epoch(self) -> None:
        pass

    @abc.abstractproperty
    def epochs_elapsed(self) -> None:
        pass

    @classmethod
    def elapse_epoch(cls) -> None:
        """
        Loops through the list of all instances
        that inherited Temporal regardless of what Class it
        is, and starts their unique day_pass( ) implementations.
        """
        for instance in Temporal.instances:
            instance.run_epoch() # runs in order the list of Temporal instances
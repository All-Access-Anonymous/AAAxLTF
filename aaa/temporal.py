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
    def day_pass(self) -> None:
        pass

    @abc.abstractproperty
    def days_elapsed(self) -> int | None:
        pass

    @classmethod
    def elapse_day(cls) -> None:
        """
        Loops through the list of all instances
        that inherited Temporal regardless of what Class it
        is, and starts their unique day_pass( ) implementations.
        """
        for instance in Temporal.instances:
            instance.day_pass()

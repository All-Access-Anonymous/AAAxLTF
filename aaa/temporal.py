import abc
from typing import List

class Temporal(metaclass=abc.ABCMeta):

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
        for instance in Temporal.instances:
            instance.day_pass()

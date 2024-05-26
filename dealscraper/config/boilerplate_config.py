from abc import ABC, abstractmethod


class BoilerPlateConfig(ABC):
    """
    This holds the general boilerplate configuration to be used in classes
    """

    @abstractmethod
    def __init__(self) -> None:
        pass

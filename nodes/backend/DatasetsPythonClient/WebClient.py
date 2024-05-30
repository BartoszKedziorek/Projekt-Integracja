from abc import ABC, abstractmethod


class WebClient(ABC):
    @abstractmethod
    def getSource(self, url, dest_dir) -> None:
        pass
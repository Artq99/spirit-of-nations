import os
from dataclasses import dataclass
from typing import List

import pygame
from pygame import Surface


class ResourceNotFoundError(Exception):
    """
    Raised when a resource manager could not find a resource of a given name.
    """

    def __init__(self, resource_name: str) -> None:
        super().__init__("Resource not found: {}".format(resource_name))


@dataclass
class DataPath:
    """
    Dataclass holding information about a resource directory.

    Prefix is optional and will be added to the resource name, separated with a dot.
    """
    path: str
    prefix: str = None


class ResourceManager:
    """
    Resource manager cares for loading the resources from the given list and provides an easy way to get them
    using their assigned name.
    """

    def __init__(self, paths: List[DataPath]) -> None:
        self._paths: List[DataPath] = paths
        self._resources = dict()

    def load_resources(self) -> None:
        """
        Load all resources from the specified data paths.
        """
        data_path = os.path.join(os.getcwd(), "data")
        for path in self._paths:
            dir_path = os.path.join(data_path, path.path)
            for el in os.listdir(dir_path):
                el_path = os.path.join(dir_path, el)
                if os.path.isfile(el_path):
                    name = self._get_resource_name(el, path)
                    surface = pygame.image.load(el_path)
                    self._resources[name] = surface

    def get_resource(self, name: str) -> Surface:
        """
        Get a resource of the given name.

        :raises ResourceNotFoundError: when the resource could not be found
        """
        try:
            return self._resources[name]
        except KeyError:
            raise ResourceNotFoundError(name)

    @staticmethod
    def _get_resource_name(resource: str, path: DataPath) -> str:
        # Get rid of the extension
        name = os.path.splitext(resource)[0]
        # Add prefix if specified
        if path.prefix is not None:
            name = path.prefix + "." + name
        return name

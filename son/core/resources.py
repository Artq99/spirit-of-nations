import os
from dataclasses import dataclass

import pygame
from pygame import Surface

# TODO refactoring


@dataclass
class ResourceInfo:
    name: str
    file: str


class ResourceNotFoundError(Exception):

    def __init__(self, resource_name: str) -> None:
        super().__init__("Resource not found: {}".format(resource_name))


class ResourceManager:

    def __init__(self, resource_list: list) -> None:
        self.resource_list = resource_list
        self._resources = dict()

    def load_resources(self) -> None:
        for resource in self.resource_list:
            path = os.path.join("data", resource.file)
            file = pygame.image.load(path)
            self._resources[resource.name] = file

    def get_resource(self, name: str) -> Surface:
        try:
            return self._resources[name]
        except KeyError:
            raise ResourceNotFoundError(name)

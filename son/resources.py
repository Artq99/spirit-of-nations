import os

import pygame

# TODO Move this to an XML file
RESOURCE_LIST = [
    {"name": "grass", "file": "grass.png"}
]


class ResourceNotFoundError(Exception):
    def __init__(self, resource_name):
        super().__init__("Resource not found: {}".format(resource_name))


class ResourceManager:
    def __init__(self):
        self._resources = dict()

    def load_resources(self):
        for resource in RESOURCE_LIST:
            path = os.path.join("data", resource["file"])
            file = pygame.image.load(path)
            self._resources[resource["name"]] = file

    def get_resource(self, name):
        try:
            return self._resources[name]
        except KeyError:
            raise ResourceNotFoundError(name)

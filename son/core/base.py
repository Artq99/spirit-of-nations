from pygame import Surface
from pygame.event import Event


class Lifecycle:
    """
    Base class for all classes that should go through the lifecycle in the main loop.
    """

    def pre_update(self, *args, **kwargs) -> None:
        """
        Lifecycle hook: Pre-Update

        :param args: any arguments
        :param kwargs: any keyword arguments
        """
        pass

    def update(self, *args, **kwargs) -> None:
        """
        Lifecycle hook: Update

        :param args: any arguments
        :param kwargs: any keyword arguments
        """
        pass

    def handle_event(self, event: Event, *args, **kwargs) -> bool:
        """
        Lifecycle hook: Handle event

        :param event: event to handle
        :param args: any arguments
        :param kwargs: any keyword arguments
        """
        return False

    def draw(self, destination_surface: Surface, *args, **kwargs) -> None:
        """
        Lifecycle hook: Draw

        :param destination_surface: surface the object should be drawn on
        :param args: any arguments
        :param kwargs: any keyword arguments
        """
        pass

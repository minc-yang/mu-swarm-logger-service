import asyncio
import logging

__all__ = [
    "Event", "ContainerEvent", "cleanup_fixtures", "register_event",
    "run_on_startup_coroutines", "send_event",
]


logger = logging.getLogger(__name__)
on_startup_coroutines = []
event_handlers = []
module_mtimes = {}
fixture_coroutines = []
fixture_generators = []


class Event:
    """
    A Docker Event
    """
    @classmethod
    def new(cls, client, data):
        """
        New Docker events are transformed here to the class Event
        """
        event_type = data['Type']
        if event_type == "container":
            return ContainerEvent(client, data)
        else:
            logger.debug("Unrecognized event (%s): %s", event_type, data)
            return Event(client, data)

    def __init__(self, client, data):
        self.client = client
        self.data = data

    @property
    def type(self):
        return self.data['Type']

    @property
    def action(self):
        return self.data['Action']

    @property
    def id(self):
        return self.data['Actor']['ID']

    @property
    def attributes(self):
        return self.data['Actor']['Attributes']

    @property
    def time(self):
        return self.data['time']

    @property
    def time_nano(self):
        return self.data['timeNano']


class ContainerEvent(Event):
    """
    A Docker container event
    """

    _container_task = None

    @property
    def container(self):
        if self._container_task is None:
            self._container_task = asyncio.ensure_future(
                self.client.inspect_container(self.id))
        return self._container_task

    @property
    def name(self):
        return self.attributes['name']

    @property
    def status(self):
        return self.data['status']


async def send_event(event, fixtures):
    """
    Send the Docker event to all the registered hooks
    """
    coros_or_futures = []
    for handler in list_handlers(event):
        kwargs = get_kwargs_for_fixtures(handler, [event] + fixtures)
        coros_or_futures.append(handler(**kwargs))
    results = await asyncio.gather(*coros_or_futures, return_exceptions=True)
    exceptions = filter(lambda x: isinstance(x, BaseException), results)
    for exc in exceptions:
        try:
            raise exc
        except:
            logger.exception("An error occurred")


async def run_on_startup_coroutines(fixtures):
    """
    This function starts all the on_startup coroutines
    """
    for coroutine in on_startup_coroutines:
        try:
            kwargs = get_kwargs_for_fixtures(coroutine, fixtures)
            await coroutine(**kwargs)
        except Exception:
            logger.exception("Startup coroutine failed")


def on_startup(coroutine):
    """
    A decorator that can be used to register a coroutine that is called when
    the application starts up
    """
    on_startup_coroutines.append(coroutine)


def register_event(coroutine):
    """
    A decorator that can be used to register a coroutine as a receiver of
    Docker events
    """
    event_handlers.append(coroutine)


def fixture(coroutine):
    """
    A decorator that adds a fixture to your application, allowing it to be used
    in any registered event very much like py.test but based on the type of the
    annotations instead of the parameter name. You can even add fixture
    dependencies in your fixtures.
    """
    fixture_coroutines.append(coroutine)


async def startup_fixtures(docker):
    """
    Start all the fixtures and return them
    """
    fixtures = [docker]
    rejected = 0
    while fixture_coroutines:
        if rejected == len(fixture_coroutines):
            raise RuntimeError("Cannot resolve fixture dependencies: %r"
                               % fixture_coroutines)
        coroutine = fixture_coroutines.pop(0)
        kwargs = get_kwargs_for_fixtures(coroutine, fixtures)
        try:
            async_gen = coroutine(**kwargs)
        except TypeError:
            fixture_coroutines.append(coroutine)
            rejected += 1
        else:
            rejected = 0
            fixture_generators.append(async_gen)
            fixture = await async_gen.__anext__()
            fixtures.append(fixture)
    return fixtures


async def cleanup_fixtures():
    """
    Clean-up all the fixtures opened
    """
    for async_gen in fixture_generators:
        try:
            async for _ in async_gen:
                pass
        except Exception:
            logger.exception("While cleaning-up fixture %r", async_gen)


def get_kwargs_for_fixtures(func, fixtures):
    """
    Get the keyword arguments passed to a function according to the type
    annotations of that function and the list of possible fixtures
    """
    return {
        key: p
        for key, type_ in func.__annotations__.items()
        for p in fixtures
        if isinstance(p, type_)
    }


def list_handlers(event):
    """
    List all the handlers for a specific type of event
    """
    event_type = type(event)
    return [
        event_handler
        for event_handler in event_handlers
        if any(issubclass(event_type, x)
               for x in event_handler.__annotations__.values())
    ]

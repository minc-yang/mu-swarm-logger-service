from aiosparql.syntax import IRI, Namespace, PrefixedName, RDF  # noqa: F401

__all__ = """
    rdf swarmui mu ext dct doap w3vocab foaf auth session
    """.split()


class SwarmUI(Namespace):
    __iri__ = IRI("http://swarmui.semte.ch/vocabularies/core/")

    PidsStats = PrefixedName
    SectorsRecursive = PrefixedName
    CpuUsage = PrefixedName
    ThrottlingData = PrefixedName
    CpuStats = PrefixedName
    CpuUsage = PrefixedName
    ThrottlingData = PrefixedName
    PrecpuStats = PrefixedName
    Stats = PrefixedName
    MemoryStats = PrefixedName
    Network = PrefixedName
    Stats = PrefixedName


class Mu(Namespace):
    __iri__ = IRI("http://mu.semte.ch/vocabularies/core/")


class Ext(Namespace):
    __iri__ = IRI("http://mu.semte.ch/vocabularies/ext/")


class Dct(Namespace):
    __iri__ = IRI("http://purl.org/dc/terms/")


class Doap(Namespace):
    __iri__ = IRI("http://usefulinc.com/ns/doap#")


class Foaf(Namespace):
    __iri__ = IRI("http://xmlns.com/foaf/0.1/")


class Auth(Namespace):
    __iri__ = IRI("http://mu.semte.ch/vocabularies/authorization/")


class Session(Namespace):
    __iri__ = IRI("http://mu.semte.ch/vocabularies/session/")


class W3Vocab(Namespace):
    __iri__ = IRI("https://www.w3.org/1999/xhtml/vocab#")


class DockEvent(Namespace):
    __iri__ = IRI("http://ontology.aksw.org/dockevent/")

    action = PrefixedName
    actionExtra = PrefixedName
    actor = PrefixedName
    actorId = PrefixedName
    container = PrefixedName
    dateTime = PrefixedName
    eventId = PrefixedName
    image = PrefixedName
    link = PrefixedName
    name = PrefixedName
    nodeId = PrefixedName
    nodeIp = PrefixedName
    nodeIpPort = PrefixedName
    nodeName = PrefixedName
    source = PrefixedName
    time = PrefixedName
    timeNano = PrefixedName
    type = PrefixedName


class DockEventTypes(Namespace):
    __iri__ = IRI("http://ontology.aksw.org/dockevent/types/")

    container = PrefixedName
    event = PrefixedName
    network = PrefixedName
    plugin = PrefixedName
    volume = PrefixedName


class DockEventActions(Namespace):
    __iri__ = IRI("http://ontology.aksw.org/dockevent/actions/")

    attach = PrefixedName
    connect = PrefixedName
    create = PrefixedName
    destroy = PrefixedName
    die = PrefixedName
    exec_create = PrefixedName
    exec_start = PrefixedName
    health_status = PrefixedName
    resize = PrefixedName
    start = PrefixedName


class DockContainer(Namespace):
    __iri__ = IRI("http://ontology.aksw.org/dockcontainer/")

    env = PrefixedName
    id = PrefixedName
    label = PrefixedName
    name = PrefixedName
    network = PrefixedName


class DockContainerNetwork(Namespace):
    __iri__ = IRI("http://ontology.aksw.org/dockcontainer/network/")

    name = PrefixedName
    id = PrefixedName
    ipAddress = PrefixedName

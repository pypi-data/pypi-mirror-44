from conda.models.version import VersionOrder
from graphviz import Digraph


def vparse(v, add=""):
    version, build = v
    version = version.strip("*").strip(".")
    # print(v, _vparse(v.strip("*").strip(".")))
    return VersionOrder(f"{version}{add}"), f"{build}"


def print_dag(all_nodes, to_install):
    dot = Digraph()

    out_nodes = set()

    # nodes
    for v in to_install:
        dot.node(f"{v.name}_{v.version}", f"{v.name} {v.version}")
        out_nodes.add(v)

    # edges
    for v in to_install:
        for c in v.out_nodes:
            if c in out_nodes:
                for d in v.p["depends"]:
                    if d.startswith(c.name):  # finde dependency
                        dot.edge(f"{v.name}_{v.version}", f"{c.name}_{c.version}", label=d)

    print(dot.source)

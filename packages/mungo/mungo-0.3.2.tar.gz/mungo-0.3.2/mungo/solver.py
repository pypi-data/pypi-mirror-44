import re
from collections import defaultdict
from functools import lru_cache
from functools import partial

from pulp import *
from pulp import LpProblem, LpMinimize, LpStatusOptimal, LpStatus

from mungo.common import vparse
from mungo.repodata import get_repository_data, merge_repodata

operator_function = {
    ">=": lambda x, y: vparse(x) >= vparse(y),
    ">": lambda x, y: vparse(x) > vparse(y),
    "<=": lambda x, y: vparse(x) <= vparse(y),
    "<": lambda x, y: vparse(x) < vparse(y),
    "!=": lambda x, y: ~(vparse(x) >= vparse(y)) and (vparse(x) < vparse(y, ".99999999999999")),
    "=": lambda x, y: (vparse(x) >= vparse(y)) and (vparse(x) < vparse(y, ".99999999999999")),
    "==": lambda x, y: (vparse(x) >= vparse(y)) and (vparse(x) < vparse(y, ".99999999999999")),
}


class Node:
    def __init__(self, name, version, p):
        self.name = name
        self.version = version
        self.factor = 1
        self._in_nodes = []
        self._out_nodes = defaultdict(list)
        self._x = None
        self.p = p
        self._mass_low = None
        self._mass_high = None
        self.invalid = False

    def add_in_node(self, n):
        self._in_nodes.append(n)

    def remove_in_node(self, n):
        self._in_nodes.remove(n)

    def add_out_node(self, n):
        self._out_nodes[n.name].append(n)

    def remove_out_node(self, n):
        self._out_nodes[n.name].remove(n)

    @property
    def channel_name(self):
        if self.p is None or "channel" not in self.p:
            return ""
        return self.p['channel'].split('/')[-2]

    @property
    def is_installed(self):
        if self.p is None:
            return False
        # print(self.name, self.version, "installed" in self.p)
        return "installed" in self.p and self.p["installed"]

    @property
    def in_nodes(self):
        return self._in_nodes

    @property
    def out_nodes(self):
        for nodes in self._out_nodes.values():
            for n in nodes:
                yield n

    @property
    def x(self):
        # create LP variable, if not exist
        if self._x is None:
            self._x = LpVariable("{name}-{version}".format(name=self.name, version=self.version), 0, 1, LpInteger)
        return self._x

    def delete(self):
        for n in self.in_nodes:
            n.remove_out_node(self)
        for n in self.out_nodes:
            n.remove_in_node(self)


@lru_cache()
def valid_packages(ls, repodata):
    # print(ls)
    all_valids = []
    for s in ls:
        name, is_valid = _valid_packages_function(s)
        all_valids.append(is_valid)

    # all_valid = lambda x: reduce((lambda a, b: a(x) and b(x)), all_valids)
    all_valid = lambda x: all([f(x) for f in all_valids])
    ret = [(name, v) for v in repodata.d[name] if all_valid(v)]
    return ret


def split_package_constraint(s):
    split = s.split(",")
    ret = []

    for i, x in enumerate(split):
        res = re.split('(==|!=|>=|<=|=|<|>| )', x)
        res = [y for y in res if y != " " and len(y) > 0]
        if i == 0:
            name = res.pop(0)
        ret.append(res)

    return name, ret


# print(split_package_constain("pysocks 4 rc3"))
# print(split_package_constain("pysocks >=1.5.6,<2.0,!=1.5.7"))
# print(split_package_constain("pysocks>=   1.5.6,  <  2.0,!= 1.5.7"))
# print(split_package_constain("pysocks 1=4"))
# exit()

def _valid_packages_function(s):
    name, constraints = split_package_constraint(s)

    is_valids = []  # lambda x: True

    for c in constraints:
        len_c = len(c)
        if len_c == 0:
            # no version constraint
            pass
        elif len_c == 1:
            # version constraint without operator (equals ==)
            version = c[0]
            is_valids.append(lambda x: partial(operator_function["="], y=(version, 0))(x))
        elif len_c == 2:
            # version constraint
            operator, version = c
            if operator in [">=", ">", "<=", "<", "!=", "=", "=="]:
                is_valids.append(partial(operator_function[operator], y=(version, 0)))
            else:
                # version build constraint with no operator
                # TODO: dont ignore build
                version, build = c
                is_valids.append(partial(operator_function["="], y=(version, 0)))
        else:
            raise Exception("invalid version constraint", s)
    is_valid = lambda x: all([f(x) for f in is_valids])
    return name, is_valid


def create_node(name, version, repodata,
                sender=None,
                all_nodes=defaultdict(dict),
                override_dependencies=None):
    if version in all_nodes[name]:
        node = all_nodes[name][version]
        node.add_in_node(sender)  # add the parent to in-nodes
        return node

    # create new node
    if version in repodata.d[name]:
        p = repodata.d[name][version]
    else:
        p = None

    new_node = Node(name, version, p)

    if sender is not None:
        new_node.add_in_node(sender)

    all_nodes[name][version] = new_node

    # get package information from repodata
    if override_dependencies is not None:
        dependencies = override_dependencies
    else:
        dependencies = p["depends"]

    # multiple constraints may refer the same package
    # group them

    grouped_dependencies = defaultdict(list)
    for dependency in dependencies:
        name = split_package_constraint(dependency)[0]
        grouped_dependencies[name].append(dependency)

    # print("python >=3.7,<3.8.0a0", valid_packages(("python >=3.7,<3.8.0a0", ), repodata))
    # exit()

    # print("openssl 1.0.1", list(valid_packages(["openssl 1.0.1"], repodata)))
    # exit()

    # print(name, version, grouped_dependencies)

    for dependency in grouped_dependencies.values():
        d_node = None
        # make sure s is list like if string
        if isinstance(dependency, str):
            dependency = (dependency,)
        for d_name, d_version in valid_packages(tuple(dependency), repodata):
            d_node = create_node(d_name, d_version, repodata, new_node, all_nodes)
            new_node.add_out_node(d_node)

        if d_node is None:  # no versions were found for a dependency
            print_missing_package(dependency)
            new_node.invalid = True
            # raise Exception("no packages found for", *dependency)

    return new_node


def reduce_dag(all_nodes, channels):
    # reduce DAG

    #for name, versions in all_nodes.items():
    #    for current_node in versions.values():
    #        print(current_node.name, current_node.version)

    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    nodes_to_remove = set()

    for name, versions in all_nodes.items():
        if name == "root":
            continue
        seen_keys = set()

        # if name == "ca-certificates":
        #     print(list(sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name] + versions[v].is_installed * (priority + 1), vparse(v)), reverse=True)))
        #     exit()

        # TODO the following line is also used in "base" and should be some kind of function import
        for v in sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name] + versions[v].is_installed * (priority + 1), vparse(v)), reverse=True):
            current_node = versions[v]
            in_node_key = tuple(sorted([(n.name, n.version) for n in current_node.in_nodes]))
            out_node_key = tuple(sorted([(n.name, n.version) for n in current_node.out_nodes]))
            key = (in_node_key, out_node_key)

            #if current_node.version[0] == "3.6.8":
            #print(current_node.channel_name, current_node.is_installed, current_node.name, current_node.version, key in seen_keys)

            if key in seen_keys:
                # the in-node out-node combination exist in a higher version of the same package
                # thus the higher version is ALWAYS preferable and this version can be removed
                nodes_to_remove.add(current_node)
            else:
                seen_keys.add(key)

    # remove the identified nodes
    for n in nodes_to_remove:
        n.delete()
        del (all_nodes[n.name][n.version])


def create_dag(channels, packages, local_repodata, njobs=8, offline=False, force_download=False):
    repodata_chunks = get_repository_data(channels, njobs, offline, force_download)
    repodata = merge_repodata(local_repodata + repodata_chunks)

    # add installed packages to the repodata

    # default_packages = {"sqlite", "wheel", "pip"}
    default_packages = set()

    all_nodes = defaultdict(dict)
    root = create_node("root", ("0", "0"), repodata, all_nodes=all_nodes,
                       override_dependencies=list(packages | default_packages))

    # reduce DAG
    reduce_dag(all_nodes, channels)
    return all_nodes, root


def nodes_to_install(all_nodes, root, channels):
    channel_order = dict()
    for priority, channel in enumerate(reversed(channels)):
        if channel == "defaults":
            channel_order['main'] = priority
            channel_order['free'] = priority
            channel_order['pro'] = priority
            channel_order['r'] = priority
        else:
            channel_order[channel] = priority
        channel_order[""] = priority + 1  # highest priority for local installed packages

    # create ILP problem
    prob = LpProblem("DependencySolve", LpMinimize)

    # build LP on the reduced DAG
    objective = []
    prob += root.x == 1

    # n.p['channel'].split('/')[-2]

    # create brother information
    for name, versions in all_nodes.items():
        big_brother = None
        # small hack to make local always be the highest

        for v in sorted(versions.keys(), key=lambda v: (channel_order[versions[v].channel_name] + versions[v].is_installed * (priority + 1), vparse(v)), reverse=True):
            n = versions[v]
            n.big_brother = big_brother
            big_brother = n

    def mass(n):
        if n is None:
            return 0, 0

        if n._mass_low is None:
            n._mass_low = 0  # temporarily set mass to 0 for loops in "DAG"
            n._mass_high = 0  # temporarily set mass to 0 for loops in "DAG"
            m_low = 0
            m_high = 0
            for children in n._out_nodes.values():
                children_masses = [mass(c) for c in children]
                m_low += min([c for c, _ in children_masses])
                m_high += max([c for _, c in children_masses])
            # n._mass_low = m_low + 1 + mass(n.big_brother)[1]
            # n._mass_high = m_high + 1 + mass(n.big_brother)[1]
            n._mass_high = m_high - m_low + 1 + mass(n.big_brother)[1]
            n._mass_low = 1 + mass(n.big_brother)[1]
        return n._mass_low, n._mass_high

    # for name, versions in all_nodes.items():
    #     for version, n in versions.items():
    #         print(name, version, mass(n))


    # create ILP
    for name, versions in all_nodes.items():
        # constraint: install at most one version of a package
        prob += sum(n.x for n in versions.values()) <= 1
        # exclude invalid node
        # constraint: if a parent is installed, one version of each dependency must be installed too
        for current_node in versions.values():
#            print(current_node.name, current_node.version)

            if current_node.invalid:  # exlude invalid nodes
                prob += current_node.x == 0
                continue

            for out_group in current_node._out_nodes.values():
                prob += sum([n.x for n in out_group]) >= current_node.x

        # storing the objectives
        objective.extend([mass(n)[0] * n.x for n in versions.values()])
        # print([(n.name, n.normalized_version, n.factor) for n in versions.values()])

        if current_node is root:  # no no_install for root  # FIXME current_node might be uninitialized
            continue

    prob += sum(objective)
    prob.writeLP("WhiskasModel.lp")
    prob.solve()

    if prob.status != LpStatusOptimal:
        print(f"ERROR: Solution is not optimal (status: {LpStatus[prob.status]}).\nAborting.", file=sys.stderr)
        exit(1)

    # for v in prob.variables():
    #     print(v.name, v.varValue)

    # collect all install nodes
    install_nodes = []
    for _, versions in sorted(all_nodes.items()):
        for n in versions.values():
            # print(n.name, n.version, n.x.varValue, "installed" in n.p)
            if n.p is None:  # skip root
                continue
            x = n.x
            if x.varValue == 1.0:
                install_nodes.append(n)

    return sorted(install_nodes, key=lambda x: x.factor)


missing_dependencies = set()


def print_missing_package(dependency):
    # print missing package information for a dependency constraint
    # only print once by remembering
    dependency = tuple(dependency)
    if dependency not in missing_dependencies:
        print("WARNING:", "no packages found for", *dependency, file=sys.stderr)
        missing_dependencies.add(dependency)

# mungo

**IMPORTANT WARNING**
*mungo* is experimental, things are *very* likely to break.

*mungo* acts as a drop-in replacement for `conda create` and `conda install` -
but with way faster environment resolution.
The improvements in speed are achieved by employing linear programming instead
of sat-solving and caching of intermediate results (see "The ILP" for more information).

Note that we do not want to replace conda - we merely wish to share our solution so that it can be tested and perhaps
someday be integrated into conda itself.

## Caveats
  - *mungo* only exposes basic functionality:
    - `install (package_spec)+ (--name NAME)? (--channel CHANNEL)* (--file FILE)?`
    - `create  (package_spec)* (--name NAME)? (--channel CHANNEL)* (--file FILE)?`
  - *mungo*'s solutions will *not* be the same as conda's.
  - *mungo* cannot handle custom channel urls. Any channel which has `repodata.json.bz2` files available from `https://conda.anaconda.org/CHANNEL/ARCH` is fine, though.
  - *mungo* only reads channels from `~/.condarc` (but also uses the `--channel` arguments, if supplied, of course).
  - *mungo* only supports linux at the moment.

## Installation
You need a working conda installation, since actual package installation is
delegated to conda.
### from PIP
    pip install mungo

## Examples
    # create an environment named 'foo' with the specified packages
    mungo create -n foo "python>=3.7" pulp packaging pyyaml

    # create an environment from an environment file (such as mungo.yml)
    mungo create --file mungo.yml

    # install packages into the current environment
    mungo install bwa

    # install packages into a different environment
    mungo install -n foo bwa

## The ILP
*mungo* uses an integer linear program to determine a configuration of compatible packages which maximizes version numbers while also keeping channel order in mind.

![alt text](images/dag.png "Dependency DAG")

After merging, ILP variables ∈ {0, 1} are created for each *p*-node. These variables relate to `(package, version)` configurations and tell us whether a configuration is selected for installation (1) or not (0).
In a second step, the following ILP constraints are generated from the constrain nodes defined above:
For each parent `p` (variable), the sum of all children (variables) `C` must be greater or equal to `p`; in other words: If `p` is selected, at least one available version of each dependent package must also be selected. If `p` is *not* selected for installation (i.e. `p = 0`), installation status of its dependencies is not relevant (for `p`).

![alt text](images/dag2.png "Dependency DAG")


![alt text](images/dag3.png "Dependency DAG")
## Changelog
  - version 0.1.4: Show packages that get updated/downgraded/installed.
  - version 0.1.3: Prioritize channels over version numbers. Add '-y/--yes' flag to skip package installation confirmation.
  - version 0.1.0: Initial version.

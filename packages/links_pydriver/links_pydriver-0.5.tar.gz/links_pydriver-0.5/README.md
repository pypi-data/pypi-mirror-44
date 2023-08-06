# links_pydriver

links_pydriver allows to fill a MongoDB database in python by respecting the standards of Links.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/tanguyesteoule/links_pydriver

Binary installers for the latest released version are available at the [Python
package index](https://pypi.org/project/links_pydriver)
```sh
pip install links_pydriver
```

## Example

```py
from links_pydriver.connection import db_utils
from links_pydriver.model.Experiment import Experiment
from links_pydriver.model.Relation import Relation
from links_pydriver.model.Snapshot import Snapshot
from links_pydriver.model.Entity import Entity
from links_pydriver.marshaler.DriverMarshaler import marshalling

# Creating entities
e1 = Entity("Agent 1", "Ant", {'name': 'Maholise'})
e2 = Entity("Agent 2", "Ant", {'name': 'Tuoi'})

# Creating relations
r1 = Relation('helping1', 'Agent 2', 'Agent 1', True, 'Help', {'name': 'Helping 1')

# Creating snapshot
s1 = Snapshot(0, [e1], [], {'Encountered exception': 'Unhandled NCS !'})
s2 = Snapshot(1, [e1, e2], [r1], {'Encountered exception': 'Unhandled NCS !'})

# Creating experiment
exp = Experiment('exp_example', {'Description': 'Example links data structure'}, [s1, s2])

# Filling the database
db = db_utils.connect(url='localhost', db_name='links', port=27017)
marshalling(db, exp)
```
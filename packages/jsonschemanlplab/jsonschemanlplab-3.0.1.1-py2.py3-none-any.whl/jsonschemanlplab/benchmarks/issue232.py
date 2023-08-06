#!/usr/bin/env python
"""
A performance benchmark using the example from issue #232:

https://github.com/Julian/jsonschema/pull/232

"""
from twisted.python.filepath import FilePath
from perf import Runner
from pyrsistent import m

from jsonschemanlplab.tests._suite import Collection
import jsonschemanlplab


collection = Collection(
    path=FilePath(__file__).sibling("issue232"),
    remotes=m(),
    name="issue232",
    validator=jsonschemanlplab.Draft7Validator,
)


if __name__ == "__main__":
    collection.benchmark(runner=Runner())

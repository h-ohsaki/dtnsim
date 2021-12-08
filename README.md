# NAME

dtnsim - DTN (Delay/Disruption Tolerant Networking) simulator with several agent/mobility models

# DESCRIPTION

**dtnsim** is a DTN (Delay/Disruption-Tolerant Networking) simulator written
in Python.  Since all programs in **dtnsim** are written in Python, if you are
a Python programmer, you can easily modify simulator functionalities and/or
add new features.  Python is one of major light-weight programming languages,
which enables rapid prototyping of DTN simulations.  For instance, when you
think of a novel network protocol for DTN, you can rapidly implement the
protocol with the help of high expressiveness of Python language.

Since almost everything in **dtnsim** is written in Python, **dtnsim** is not
suitable for extremely large-scale DTN simulations.  For instance, **dtnsim**
is not suitable for very large-scale DTN simulations with millions of agents
(i.e., mobile nodes/terminals).  However, such limitation is not an issue in
practice since DTN is generally expected to be utilized in environments with
spares agents.

# EXAMPLE

```sh
dtnsim | cellx
```

# INSTALLATION

```python
pip3 install dtnsim
```

# AVAILABILITY

The latest version of **dtnsim** is available at PyPI
(https://pypi.org/project/dtnsim/) .

# AUTHOR

Hiroyuki Ohsaki (ohsaki[atmark]lsnl.jp)

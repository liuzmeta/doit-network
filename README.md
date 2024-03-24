
# doit-network

Generates a graph (using networkx) of [doit](http://pydoit.org) tasks.

Sample for [doit tutorial](http://pydoit.org/tutorial_1.html) tasks:

![Sample output](/tasks.png)


## install

pip install doit-network


## usage

```
$ doit network
```

- By default sub-tasks are hidden. Use option `--show-subtasks` to display them.
- By default all tasks are included in graph.
  It is possible to specify which tasks should be included in the graph (note dependencies will be automatically included).

### limitations

`calc_dep` and `delayed-tasks` are not supported.




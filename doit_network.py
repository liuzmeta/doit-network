"""doit-netowrk

The MIT License

Copyright (c) 2024-present Zhu Liu & contributors
"""

__version__ = (0, 1, 0)

from collections import deque

import networkx as nx
import matplotlib
import matplotlib.pyplot

from doit.cmd_base import DoitCmdBase
from doit.control import TaskControl


opt_subtasks = {
    'name': 'subtasks',
    'short': '',
    'long': 'show-subtasks',
    'type': bool,
    'default': False,
    'help': 'include subtasks in netowrk',
}

opt_outfile = {
    'name': 'outfile',
    'short': 'o',
    'long': 'output',
    'type': str,
    'default': None, # actually default dependends parameters
    'help': 'name of generated file',
}



class NetowrkCmd(DoitCmdBase):
    name = 'netowrk'
    doc_purpose = "create task's dependency-netowrk (in dot file format)"
    doc_description = """Creates a DAG (directly acyclic graph) representation of tasks.
Website/docs: https://github.com/liuzmeta/doit-network
    """
    doc_usage = "[TASK ...]"

    cmd_options = (opt_subtasks, opt_outfile)


    def node(self, task_name):
        """get netowrk node that should represent for task_name

        :param task_name:
        """
        if self.subtasks:
            return task_name
        task = self.tasks[task_name]
        return task.subtask_of or task_name

    def draw_to_file(self, filename):
        fig = matplotlib.pyplot.figure()
        options = {'with_labels':True, 'font_size':18, 'font_color': "whitesmoke", 'node_size':2400, 
            'arrowsize':20, 'arrowstyle':'simple', 'edge_color':'tab:gray'}
        nx.draw(self.netowrk, node_color = self.node_colors, ax=fig.add_subplot(), **options)
        fig.savefig(filename)

    def add_node(self, task, subtasks):
        node_attrs = {True: 'tab:blue', False: 'tab:red'}
        sub_node_attrs = {True: 'blue', False: 'red'}
        if task.has_subtask:
            node_attrs = sub_node_attrs
        if (not task.subtask_of) or subtasks:
            self.netowrk.add_node(task.name)
            self.node_colors.append(node_attrs[self.uptodate(task)])

    def uptodate(self, task):
        uptodate = task.uptodate
        for i in uptodate:
            if not i: return False
        return True
        


    def add_edge(self, src_name, sink_name):
        source = self.node(src_name)
        sink = self.node(sink_name)
        if source != sink and (source, sink) not in self._edges:
            self._edges.add((source, sink))
            self.netowrk.add_edge(source, sink)


    def _execute(self, subtasks, outfile, pos_args=None):
        # init
        control = TaskControl(self.task_list)
        self.tasks = control.tasks
        self.subtasks = subtasks
        self._edges = set() # used to avoid adding same edge twice

        # create netowrk
        self.netowrk = nx.DiGraph()
        self.node_colors = []

        # populate netowrk
        processed = set() # str - task name
        if pos_args:
            to_process = deque(pos_args)
        else:
            to_process = deque(control.tasks.keys())

        while to_process:
            task = control.tasks[to_process.popleft()]
            if task.name in processed:
                continue
            processed.add(task.name)

            # add nodes
            self.add_node(task, subtasks)
            

            # add edges
            for sink_name in task.setup_tasks:
                self.add_edge(task.name, sink_name)
                if sink_name not in processed:
                    to_process.append(sink_name)
            for sink_name in task.task_dep:
                self.add_edge(sink_name, task.name)
                if sink_name not in processed:
                    to_process.append(sink_name)

        if not outfile:
            name = pos_args[0] if len(pos_args)==1 else 'tasks'
            outplot = '{}.png'.format(name)
        print('Generated file: {}'.format(outplot))
        self.draw_to_file(outplot)


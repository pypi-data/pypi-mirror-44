# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 23:17:38 2019

@author: yoelr
"""
from biosteam import Unit, np, pd
from .block import Block

__all__ = ('Sensitivity',)

DF = pd.DataFrame

# %% Functions

def _blockunit(blockfunc_args):
    element = blockfunc_args[0]._block._element
    if isinstance(element, Unit): return element
    else: return element._sink

def _fill_space(args, num_stack, argspace, thread, tuple_):
    for i, f, fargs in num_stack:
        for a in fargs[1:]:
            args[i] = a
            argspace.append(tuple_(args))
            thread.append((f, a))
            _fill_space(args, num_stack[:i], argspace, thread, tuple_)
        fargs.reverse()

# %% Grid of simulation blocks

class Sensitivity:
    """Create a Sensitivity object that allows for optimized sensitivity analysis over an argument space.
    
    **Parameters**
    
        **system:** [System] Sensitivity parameters should act on the system.
    
        **getter:** [function] Should return value for sensitivity.
        
        **args:** [tuple] Arguments to pass to the getter function.
    
    **Examples**

         :doc:`Sensitivity Example`
    
    """
    __slots__ = ('table',
                 '_system',
                 '_stack',
                 '_funcs',
                 '_initial_args',
                 '_argarray',
                 '_thread',
                 '_getter',
                 '_paramIDs',
                 '_ID',)
    
    def __init__(self, system, getter, *, args=(), ID=None):
        if args:
            getter_no_args = lambda: getter(*args)
            getter_no_args.__name__ = getter.__name__
            self._getter = getter_no_args
        else: self._getter = getter
        self._system = system
        self._ID = ID
        
        #: [(function, args)] Iterable of block fuctions and respective arguments.
        self._stack = []
    
    def evalparam(self, element, setter, values, isolated=False):
        """Return sensitivity at given parameter values.
        
        **Parameters**
        
            **element:** [Unit or Stream] Element in the system being altered.
            
            **setter:** [function] Should set parameter in the element.
            
            **values:** [iterable] Values for parameter.
            
            **isolated** [bool] If True, account for downstream operations. If False, only account for element.
        
        """
        system = None if isolated else self._system
        blockfunc = Block(element, system)(self._getter, setter)
        return [blockfunc(i) for i in values]
    
    def addparam(self, element, setter, values, isolated=False):
        """Add parameter to vary in sensitivity.
        
        **Parameters**
        
            **element:** [Unit or Stream] Element in the system being altered.
            
            **setter:** [function] Should set parameter in the element.
            
            **values:** [iterable] Values for parameter.
            
            **isolated** [bool] If True, account for downstream operations. If False, only account for element.
        
        """
        system = None if isolated else self._system
        self._stack.append((Block(element, system)(self._getter, setter), values))
    
    def _loadstack(self):
        """Load argument space and cache a thread of block functions and arguments."""
        system = self._system
        stack = self._stack
        if not stack: raise RuntimeError(f'No sensitivity parameters set for {repr(self)} object.')
        tuple_ = tuple
        # Order blocktests from last in network to first
        index = system._unitnetwork.index
        stack.sort(key=lambda x: index(_blockunit(x))
                                 if x[0]._block._system else -1,
                   reverse=True)
        
        initial_args = []
        funcs = []
        element_names = []
        all_args = []
        list_ = list
        for func, args in stack:
            initial_args.append(args[0])
            funcs.append(func)
            element = func._block._element
            element_names.append(element.line + '-' + element.ID.replace('_', ' '))
            all_args.append(list_(args))
        num_stack = tuple_(zip(range(len(funcs)), funcs, all_args))
        args = initial_args
        initial_args = tuple_(initial_args)
        argspace = [initial_args]
        thread = [(funcs[0], initial_args[0])]
        _fill_space(args, num_stack, argspace, thread, tuple_)
        paramIDs = [i._param.capitalize().replace('_', ' ')
                    for i in funcs]
        spacelen = len(argspace)
        spacerange = range(spacelen)
        self._argarray = np.asarray(argspace)
        
        #: All block functions
        self._funcs = funcs
        
        #: [List] All block functions and arguments to be simulated.
        self._thread = thread
        
        #: [tuple] First arguments to be simulated
        self._initial_args = initial_args
        if self._ID: ID = self._ID
        else: self._ID = ID = funcs[0].__name__
        
        #: [DataFrame] Table of the argument space with results in the final column.
        self.table = DF(argspace,
                        columns=pd.MultiIndex.from_arrays((element_names, paramIDs),
                                                           names=('Element', 'Parameter')),
                        index=spacerange)
        self._paramIDs = paramIDs
        self.table[ID] = (None,)*spacelen
        
        
    def simulate(self):
        """Simulate sensitivity over the argument space."""
        # Setup units before simulation
        self._loadstack()
        for func, arg in zip(self._funcs, self._initial_args):
            func._setter(arg)
        
        # Simulate system to initialize whole network
        try: self._system.simulate()
        except: pass
        values = []
        add = values.append
        for func, arg in self._thread:
            try: add(func(arg))
            except: add(None)
        self.table[self._ID] = values
        
    def _repr(self):    
        blocks = ''
        for i in self._funcs:
            e = i._block._element
            blk = f'{type(e).__name__}-{e}|'
            if blk not in blocks: blocks += blk
        blocks = blocks.rstrip('|')
        return f'{type(self).__name__}: {self._ID}'
    
    def __repr__(self):
        return f'[{self._repr()}]'
       
    def _info(self):
        blocks = {}
        for i in self._funcs:
            e = i._block._element
            p = i._param
            blk = f'{type(e).__name__}-{e}'
            if blk not in blocks: blocks[blk] = [p]
            else: blocks[blk].append(p)
        
        lenghts_block = []
        lines = []
        for blk, params in blocks.items():
            newline = f' [{blk}!'
            blklen = len(blk)
            blklen_spaces = (blklen)*' '
            many = len(params) > 1
            if many: newline += '('
            len_params = 0
            for p in params:
                p = f'{p}, '
                len_p = len(p)
                len_params += len_p
                if len_p != len_params and len_params > 35:
                    len_params = 0
                    p = f']\n% [{blklen_spaces}$' + p
                newline += p
            newline = newline.rstrip(', ') + (')' if many else '') + ']\n'
            newlines = newline.split('%')
            lines.extend(newlines)
            lenghts_block.extend((blklen,)*len(newlines))
                
        maxlen_block = max(lenghts_block)
        lengths = []
        lines_2 = []
        for newline, len_ in zip(lines, lenghts_block):
            newline = newline.replace('!', ' '*(maxlen_block-len_) + '| param=')
            newline = newline.replace('$', ' '*(maxlen_block-len_) + '|        ')
            lengths.append(newline.find(']'))
            lines_2.append(newline)
        
        maxlen = max(lengths)
        out = f'{self._repr()}\n'
        for newline, len_ in zip(lines_2, lengths):
            out += newline.replace(']', ' '*(maxlen-len_) + ']')
        return out.rstrip('\n ')
    
    def show(self):
        """Return information on sensitivity parameters."""
        print(self._info())
        
        
        
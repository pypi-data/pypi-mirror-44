# -*- Python -*-
# -*- coding: utf-8 -*-

'''rtctree

Copyright (C) 2009-2015
    Geoffrey Biggs
    RT-Synthesis Research Group
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the GNU Lesser General Public License version 3.
http://www.gnu.org/licenses/lgpl-3.0.en.html

Object representing an unknown node in the tree.

'''


from rtctree import exceptions
from rtctree.node import TreeNode


##############################################################################
## Unknown node object

class Unknown(TreeNode):
    '''Node representing an unknown object on a name server.

    Unknown nodes can occur below name server and directory nodes. They
    cannot contain any children.

    '''
    def __init__(self, name, parent, obj):
        '''Constructor.

        @param name Name of this object (i.e. its entry in the path).
        @param parent The parent node of this node, if any.
        @param obj The CORBA object to wrap.

        '''
        super(Unknown, self).__init__(name, parent)
        self._obj = obj

    ###########################################################################
    # Node functionality

    @property
    def is_unknown(self):
        '''Is this node unknown?'''
        return True

    @property
    def object(self):
        '''The CORBA object this object wraps.'''
        with self._mutex:
            return self._obj

    ###########################################################################
    # Internal API

    def _add_child(self):
        # Unknowns cannot contain children.
        raise exceptions.CannotHoldChildrenError


# vim: set expandtab tabstop=8 shiftwidth=4 softtabstop=4 textwidth=79

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

Object representing a zombie node in the tree.

'''

from rtctree import exceptions
from rtctree.node import TreeNode


##############################################################################
## Zombie node object

class Zombie(TreeNode):
    '''Node representing a zombie object on a name server.

    Zombie nodes can occur below name server and directory nodes. They
    cannot contain any children. They do not contain a reference to a
    CORBA object as they represent the lack of such an object under a
    name still registered on the name server.

    '''
    def __init__(self, name, parent, *args, **kwargs):
        '''Constructor.

        @param name Name of this object (i.e. its entry in the path).
        @param parent The parent node of this node, if any.

        '''
        super(Zombie, self).__init__(name=name, parent=parent, *args, **kwargs)

    @property
    def is_zombie(self):
        '''Is this node a zombie?'''
        return True


    ###########################################################################
    # Internal API

    def _add_child(self):
        # Zombies cannot contain children.
        raise exceptions.CannotHoldChildrenError


# vim: set expandtab tabstop=8 shiftwidth=2 softtabstop=2 textwidth=79

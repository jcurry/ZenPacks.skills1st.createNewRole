#########################################################################################
#
# Author:               Jane Curry,  jane.curry@skills-1st.co.uk
# Date:                 July 2nd, 2014
# Revised:		
#
#
# It create a new role, ZenNewOperator on install which has the same
#  permissions as the standard ZenUser but also has "Manage Events" permission.
#  This means users with ZenNewOperator role can Close / Ack events that they
#  have access to.
#  The role is deleted again when the ZenPack is removed.
#
# A second role,ZEN_COMMON is also created / removed.  This role ONLY has 
#  the ZEN_COMMON premission.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
##########################################################################

from Products.ZenUtils.Utils import unused
import Globals
unused(Globals)
from Products.ZenModel.ZenossSecurity import *

import os
zenhome = os.environ['ZENHOME']
from Products.ZenModel.ZenPack import ZenPackBase

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

ZEN_NEWOP_ROLE = 'ZenNewOperator'

class ZenPack(ZenPackBase):

    def install( self, app):
        super(ZenPack, self).install(app)
    #
    # On ZenPack install, create a new role called ZenNewOperator with ZenUser roles plus 'Manage Events'
    #
        self.addZenNewOperatorRole(app.zport)


    def remove( self, app, leaveObjects=False):
    #
    # On ZenPack remove, delete role ZenNewOperator 
    #
        self.removeZenNewOperatorRole(app.zport)
        ZenPackBase.remove( self, app, leaveObjects=False )

    def addZenNewOperatorRole(self, zport):

	dmd = self.dmd
	# This adds ZenNewOperator to the roles in http://<your zenoss>:8080/zport/manage_access
        if not ZEN_NEWOP_ROLE in zport.__ac_roles__:
            zport.__ac_roles__ += (ZEN_NEWOP_ROLE,)

	# Next few lines adds the ZenNewOperator role to the roleManager
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
        for rm in rms:
            if not ZEN_NEWOP_ROLE in rm.listRoleIds():
                rm.addRole(ZEN_NEWOP_ROLE)

        # Following are standard roles same as for ZenUser
        # Look in $ZENHOME/Products/ZenModel/ZenossSecurity.py for possible roles

        self.addPermissions(zport, ZEN_VIEW,
            [ZEN_NEWOP_ROLE,], 0)
        self.addPermissions(zport, ZEN_VIEW_HISTORY,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_ZPROPERTIES_VIEW,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_RUN_COMMANDS,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_DEFINE_COMMANDS_VIEW,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_MAINTENANCE_WINDOW_VIEW,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_ADMINISTRATORS_VIEW,
            [ZEN_NEWOP_ROLE,], 1)
        self.addPermissions(zport, ZEN_COMMON,
            [ZEN_NEWOP_ROLE,], 1)
    # ZEN_MANAGE_EVENTS permission is extra to allow Ack / Close of events
        self.addPermissions(zport, ZEN_MANAGE_EVENTS,
            [ZEN_NEWOP_ROLE,], 1)


    def removeZenNewOperatorRole(self, zport):
	dmd = self.dmd
        rms = (dmd.getPhysicalRoot().acl_users.roleManager,
                    zport.acl_users.roleManager)
	# This removes the role from the roleManager
	# If a user has this role, it is simply removed from them
        for rm in rms:
            if ZEN_NEWOP_ROLE in rm.listRoleIds():
                rm.removeRole(ZEN_NEWOP_ROLE)
	#This removes the role from the manage_access list
        if ZEN_NEWOP_ROLE in zport.__ac_roles__:
            rolelist=list(zport.__ac_roles__)
	    rolelist.remove(ZEN_NEWOP_ROLE)
	    zport.__ac_roles__ = tuple(rolelist)

    def addPermissions(self, obj, permission, roles=None, acquire=0):
        if not roles:
            roles = []
        if not permission in obj.possible_permissions():
            obj.__ac_permissions__=(
                obj.__ac_permissions__+((permission,(),roles),))

        for permissionDir in obj.rolesOfPermission(permission):
            if permissionDir['selected']:
                if permissionDir['name'] not in roles:
                    roles.append(permissionDir['name'])
        obj.manage_permission(permission, roles, acquire)




=================================
ZenPacks.skills1st.createNewRole
=================================

Description
===========

Create a new role, ZenNewOperator on install which has the same
permissions as the standard ZenUser but also has "Manage Events" permission.
This means users with ZenNewOperator role can Close / Ack events that they
have access to.

The role is deleted again when the ZenPack is removed.


Install with zenpack --install
Restart zenhub and zopectl.


Check roles in Zope by pointing your browser at https://<your Zenoss server>:<your Zenoss port>/zport/manage_access .
You will need to be a user with Manager role.


Change History
==============
* 1.0.0
   * Initial Release
                                                                        


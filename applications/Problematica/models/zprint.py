"""
for row in db(db.auth_user).select():
	print row.last_name 

for row in db(db.auth_user).select():
	auth.add_membership(32, row.id)
	print "%s added to group_admin" % (row.first_name)


#print auth.has_membership(31, 1)

#print auth.id_group(role="user")
	
#auth.add_permission(group_id, 'name', 'object', record_id)

#print type(db)

for row in db(db.auth_user).select():
	admin_status = auth.has_membership(32, row.id)
	if admin_status == True:
		print "%s %s is an admin" % (row.first_name, row.last_name)
	else:
		print "%s %s is not an admin" % (row.first_name, row.last_name)
"""

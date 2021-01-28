from util.dict import row2dict

def serialize(query_results):
    results_arr = []
    for r in query_results:
        # rr = r.__table__.columns.add(r.role.role, key="role")
        results_arr.append(row2dict(r))
        print(r.role.role)
    return results_arr

def user_serializer(self, query):
    res = []
    for user in query:
        res.append(row2dict(user))
        print(user.role.role)

class serialize_class(object):

    def serialize(self, query):
        return {
            '_id': query._id,
            'name': query.name,
            'email': query.email,
            'password': query.password,
            'role_id': query.role_id,
            'role': query.role.role
        }
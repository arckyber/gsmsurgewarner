from util.dict import row2dict

def serialize_user_role(user):
    rd = []
    for r in user:
        d = row2dict(r)
        d['role'] = r.role
        rd.append(d)
    return rd
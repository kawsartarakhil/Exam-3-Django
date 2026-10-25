
def can_manage_trip(user,trip):
    if not user.is_authenticated:
        return False
    return (trip.user_id==user.id or user.has_perm("travel.manage_all_trips"))



def can_manage_companion_requeest(user,companion_request):
    if not user.is_authenticated:
        return False
    return (companion_request.user_id==user.id or user.has_perm("travel.manage_all_companionrequests"))
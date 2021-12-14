def date_intersection(start_time, end_time, rezervs, rezerv_space=None):
    for i in rezervs:
        if rezerv_space and i == rezerv_space:
            continue
        else:
            if (i.start_time <= start_time < i.end_time) or (start_time <= i.start_time < end_time):
                return True
    return False

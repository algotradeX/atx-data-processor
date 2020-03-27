def create_response(status, success, data):
    resp = {"status": status, "data": data}
    if success:
        resp["success"] = "Create successful"
    else:
        resp["success"] = "Create failed"
    return resp


def update_response(status, success, data):
    resp = {"status": status, "data": data}
    if success:
        resp["success"] = "Upsert successful"
    else:
        resp["success"] = "Upsert failed"
    return resp


def delete_response(status, success, data):
    resp = {"status": status, "data": data}
    if success:
        resp["success"] = "Delete successful"
    else:
        resp["success"] = "Delete failed"
    return resp

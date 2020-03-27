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


def generate_response(status, response_type, success, data):
    resp = {"status": status, "data": data}
    if response_type == "create":
        if success:
            resp["success"] = "Create successful"
        else:
            resp["success"] = "Create failed"
    elif response_type == "update":
        if success:
            resp["success"] = "Upsert successful"
        else:
            resp["success"] = "Upsert failed"
    elif response_type == "delete":
        if success:
            resp["success"] = "Delete successful"
        else:
            resp["success"] = "Delete failed"
    return resp

from fastapi import Depends

def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

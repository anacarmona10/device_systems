import time
import uuid

from fastapi import Request


async def request_middleware(
    request: Request,
    call_next
):

    start_time = time.time()

    request_id = request.headers.get(
        "X-Request-ID",
        str(uuid.uuid4())
    )

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-App-Name"] = "device_systems"

    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    response.headers["X-Request-ID"] = request_id

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code}"
    )

    return response
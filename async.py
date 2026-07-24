import time

from rich import print


def endpoint(route):
    print(f">> handling {route}")

    # emulate database delay
    time.sleep(2)

    print(f"<< response {route}")


def server():
    # Run test requests
    tests = (
        "GET /shipment?id=1",
        "PATCH /shipment?id=4",
        "GET /shipment?id=3",
    )

    start = time.perf_counter()

    for route in tests:
        endpoint(route)

    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f}s")


# Run server
server()

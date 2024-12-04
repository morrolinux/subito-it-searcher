from cars.BLACKLIST_CARS import BLACKLIST_CARS


def get_BLACKLIST(cars):
    BLACKLIST = []
    if cars:
        BLACKLIST += BLACKLIST_CARS

    return BLACKLIST
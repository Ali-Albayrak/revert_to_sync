import os
from typing import List

INTERNAL_IP_RANGES = os.getenv("INTERNAL_IP_RANGES") 


def get_internal_ip_ranges() -> List[str]:
    """
    Return array of internal ip ranges
    """
    if INTERNAL_IP_RANGES is None:
        raise ValueError("INTERNAL_IP_RANGES environment variable is not set. Please set it before running the application.")
    return INTERNAL_IP_RANGES.split(',')


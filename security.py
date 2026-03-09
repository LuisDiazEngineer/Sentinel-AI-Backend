# List of regions considered high-risk for the system
RISK_ZONES = ["Region_X", "Region_Y", "Latam_High_Risk"]


def is_secure(region: str) -> bool:
    """
    Logic: If the region is in the blacklist, it's flagged as insecure.
    """
    return region not in RISK_ZONES

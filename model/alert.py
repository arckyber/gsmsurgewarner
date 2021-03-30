from config.const import NORMAL, YELLOW, ORANGE, RED
# from models import desequivalert

def get_alert_level(desequivalert, distance):
    distance = float(distance)
    if distance <= desequivalert['_red']:
        return RED
    elif distance <= float(desequivalert['_orange']) and distance > desequivalert['_red']:
        return ORANGE
    elif distance <= desequivalert['_yellow'] and distance > desequivalert['_orange']:
        return YELLOW
    elif distance <= desequivalert['_normal'] and distance > desequivalert['_yellow']:
        return NORMAL
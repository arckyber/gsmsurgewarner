# This is useful when dealing
#  with notification 
#  classification
SUCCESS = 'success'
FAILED = 'failed'
ERROR = 'error'

MISSING_DATA = 'missing data'

# Constant for alert level
# NORMAL = 1
# YELLOW = 2
# ORANGE = 3
# RED = 4

# dapat mag coincide ni sa arduino code
SOURCE_INDEX = 0
CMD_INDEX = 1
DISTANCE_INDEX = 2
ALERT_TYPE_INDEX = 3
SIMNUMBER_INDEX = 4
DATETIME_INDEX = 5

MSG_INDEX = 2

ALERT_3_MESSAGE = "Critical water level is detected!"
ALERT_4_MESSAGE = "Rapid rise of water is detected!"

DISTANCE_DEFAULT_UNIT = "cm"


SUCCESS_COLOR = "#018401"
WARNING_COLOR = "#ffc107"
DANGER_COLOR = "#dc3545"
PRIMARY_COLOR = "#007bff"

MODULES = [
    'dashboard',
    'sms',
    'graph',
    'map',
    'transmitters',
    'users',
    'profile',
    'extrasms',
    'roles'
]
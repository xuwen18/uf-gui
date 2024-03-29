IS_DEBUG = True

BAUD_RATE = 115200

RESERVOIR_NAMES = ["None", "1", "2", "3", "4"]
RESERVOIR_INDEX = dict(zip(RESERVOIR_NAMES, range(-1,4)))
CSV_LEN = 3
OUT_DIR = "./output/"

FLOW_RATE_MAX = 80.0
DURATION_MAX = 86_400_000

MSG_BEGIN = " " # "["
MSG_END   = "\n" # "]"

TABLE_COL = CSV_LEN + 1
TABLE_WID = 128
STATUS_DONE = "done"
STATUS_PENDING = ""
STATUS_RUNNING = "running"
STATUS_ERROR = "error"

X_LABEL = "time (ms)"
Y_LABEL = "pressure (psi)"
DATA_LENGTH = 50

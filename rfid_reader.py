import board
import busio
from adafruit_pn532.i2c import PN532_I2C

class RFIDReader:
    def __init__(self):
        # I2C init
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pn532 = PN532_I2C(i2c, debug=False)
        self.pn532.SAM_configuration()

    def get_tag(self, timeout=0.5):
        """
        Poll for a tag for up to `timeout` seconds.
        Returns a hex string (e.g. "AB12CD34") or None if no tag.
        """
        uid = self.pn532.read_passive_target(timeout=timeout)
        if uid is None:
            return None
        return "".join(f"{b:02X}" for b in uid)

import smbus
from PIL import Image
from PIL import ImageDraw
import math

address = 0x3c
addressingMode = None

PAGE_MODE = 0o1
HORIZONTAL_MODE = 0o2

OLED_Address = 0x3d
OLED_Command_Mode = 0x00
OLED_Data_Mode = 0x40
OLED_Display_Off_Cmd = 0xAE
OLED_Display_On_Cmd = 0xAF
OLED_Normal_Display_Cmd = 0xA6
OLED_Inverse_Display_Cmd = 0xA7
OLED_Activate_Scroll_Cmd = 0x2F
OLED_Dectivate_Scroll_Cmd = 0x2E
OLED_Set_Brightness_Cmd = 0x81

init_sequence_for_70x40 = [
    0xD5,  # set osc division
    0xF0,
    0xA8,  # multiplex ratio
    0x27,  # duty = 1/40
    0xD3,  # set display offset
    0x00,
    0x40,  # Set Display Start Line
    0x8D,  # set charge pump enable
    0x14,
    0x20,  # Set page address mode
    0x02,
    0xA1,  # set segment remap
    0xC8,  # Com scan direction
    0xDA,  # set COM pins
    0x12,
    0xAD,  # Internal IREF Setting
    0x30,
    0x81,  # contract control
    0x02,
    0xD9,  # set pre-charge period
    0x22,
    0xDB,  # set vcomh
    0x20,
    0xA4,  # Set Entire Display On/Off
    0xA6,  # normal / reverse
    0x0C,  # set lower column address
    0x11  # set higher column address 	
]

init_sequence_for_64x32 = [
    0x00,  # ---set low column address
    0x12,  # ---set high column address
    0x00,  # --set start line address  Set Mapping RAM Display Start Line (0x00~0x3F)
    0xB0,  # --set page address
    0x81,  # contract control
    0x03,
    0xA1,  # set segment remap
    0xA6,  # --normal / reverse
    0xA8,  # --set multiplex ratio(1 to 64)
    0x1F,  # --1/32 duty
    0xC8,  # Com scan direction
    0xD3,  # -set display offset
    0x00,
    0xD5,  # set osc division
    0x80,
    0xD9,  # set pre-charge period
    0x1F,
    0xDA,  # set COM pins
    0x12,
    0xDB,  # set vcomh
    0x40,
    0x8D,  # set charge pump enable
    0x14
]


class device():
    def __init__(self, bus, width, height):
        self.bus = smbus.SMBus(bus)
        self.OLED_Width = width  # 128 Pixels
        self.OLED_Height = height  # 64  Pixels
        if (width == 64 and height == 32):
            self.offset = 32
            self.init_sequence = init_sequence_for_64x32
        elif (width == 70 and height == 40):
            self.offset = 28
            self.init_sequence = init_sequence_for_70x40

        self.image = Image.new('1', (width, height))
        self.draw = ImageDraw.Draw(self.image)

        self.init()
        self.clear()  # clear the screen and set start position to top left corn$
        self.setNormalDisplay()  # Set display to normal mode (i.e non-inverse mode)
        self.setHorizontalMode()

    def __del__(self):
        pass

    def update(self, img=None):
        if img is not None:
            self.drawImage(img)
        else:
            self.drawImage(self.image)

    def sendCommand(self, byte):
        try:
            block = []
            block.append(byte)
            return self.bus.write_i2c_block_data(address, OLED_Command_Mode, block)
        except IOError:
            print("IOError")
            return -1

    def sendData(self, byte):
        try:
            block = []
            block.append(byte)
            return self.bus.write_i2c_block_data(address, OLED_Data_Mode, block)
        except IOError:
            print("IOError")
            return -1

    def sendArrayData(self, array):
        try:
            return self.bus.write_i2c_block_data(address, OLED_Data_Mode, array)
        except IOError:
            print("IOError")
            return -1

    def multi_comm(self, commands):
        for c in commands:
            self.sendCommand(c)

    # Init function of the OLED
    def init(self):
        self.sendCommand(0xAE)  # display off
        for cmd in self.init_sequence:
            self.sendCommand(cmd)
        self.sendCommand(0xAF)  # display ON

    def setBrightness(self, Brightness):
        self.sendCommand(OLED_Set_Brightness_Cmd)
        self.sendCommand(Brightness)

    def setHorizontalMode(self):
        global addressingMode
        addressingMode = HORIZONTAL_MODE
        self.sendCommand(0x20)  # set addressing mode
        self.sendCommand(0x00)  # set horizontal addressing mode

    def setPageMode(self):
        global addressingMode
        addressingMode = PAGE_MODE
        self.sendCommand(0x20)  # set addressing mode
        self.sendCommand(0x02)  # set page addressing mode

    def setTextXY(self, Column, Row):
        Column = Column + self.offset
        self.sendCommand(0xb0 + Row)
        self.sendCommand(((Column & 0xf0) >> 4) | 0x10)
        self.sendCommand((Column & 0x0f))

    def clear(self, hard_clear=False):
        if (hard_clear):
            bitList = [0 for x in range(self.OLED_Width)]
            for i in range(math.ceil(self.OLED_Height / 8)):
                self.sendCommand(0xB0 + i)
                self.sendCommand(0x00)
                self.sendCommand(0x12)
                for self.chunk in self.chunks(bitList, 32):
                    self.sendArrayData(self.chunk)
        else:
            self.draw.rectangle((0, 0, self.OLED_Width, self.OLED_Height), outline=0, fill=0)

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def drawImage(self, image):
        """Set buffer to value of Python Imaging Library image.  The image should
        be in 1 bit mode and a size equal to the display size.
        """
        if type(image).__name__ == "Image":  # means PIL Image
            imwidth, imheight = image.size
            # Grab all the pixels from the image, faster than getpixel.

            if imwidth != self.OLED_Width or imheight != self.OLED_Height:
                raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
                                 .format(self.OLED_Width, self.OLED_Height))

            pix = image.load()

            for y in range(math.ceil(self.OLED_Height / 8)):
                self.setTextXY(0, y)
                bitList = []
                for x in range(self.OLED_Width):
                    # Set the bits for the column of pixels at the current position.
                    bits = 0
                    # Don't use range here as it's a bit slow
                    for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                        bits = bits << 1
                        bits |= 0 if pix[x, y * 8 + 7 - bit] == 0 else 1
                    bitList.append(bits)
                for chunk in self.chunks(bitList, 32):
                    self.sendArrayData(chunk)
        else:
            imheight, imwidth = image.shape

            if imwidth != self.OLED_Width or imheight != self.OLED_Height:
                raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
                                 .format(self.OLED_Width, self.OLED_Height))

            for y in range(math.ceil(self.OLED_Height / 8)):
                self.setTextXY(0, y)
                bitList = []
                for x in range(self.OLED_Width):
                    # Set the bits for the column of pixels at the current position.
                    bits = 0
                    # Don't use range here as it's a bit slow
                    for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                        bits = bits << 1
                        bits |= 0 if image[y * 8 + 7 - bit, x] == 0 else 1
                    bitList.append(bits)
                for chunk in self.chunks(bitList, 32):
                    self.sendArrayData(chunk)

    def setNormalDisplay(self):
        self.sendCommand(OLED_Normal_Display_Cmd)

    def setInverseDisplay(self):
        self.sendCommand(OLED_Inverse_Display_Cmd)

'''
this is just the accelerometer class for the Py_Rocket Project
By Jeremy Mill <jeremymill@gmail.com>
'''

class Accelerometer:
    def __init__(self):
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        
        self.bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        self.address = 0x68       # This is the address value read via the i2cdetect command
        
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
        
    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
        self.high = self.bus.read_byte_data(self.address, adr)
        self.low = self.bus.read_byte_data(self.address, adr+1)
        val = (self.high << 8) + self.low
        return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self,a,b):
        return math.sqrt((a*a)+(b*b))

    #the math here is that roll = atan(y/(sqrt(x^2 + z^2)))
    #we use atan2 because it automaticall determines the sign for us (the quadrant)
    def get_y_rotation(self,x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    #the math here is that the pitch is = atan(x/(sqrt(y^2 + z^2)))
    #we use atan2 because it automaticall determines the sign for us (the quadrant)
    def get_x_rotation(self,x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)
    
    #as a note here, the 'scaled' values are the values in G's
    def get_x_scaled(self):
        self.accel_xout = self.read_word_2c(0x3b)
        self.accel_xout_scaled = self.accel_xout / 16384.0
        return self.accel_xout_scaled
    
    #as a note here, the 'scaled' values are the values in G's  
    def get_y_scaled(self):
        self.accel_yout = self.read_word_2c(0x3d)
        self.accel_yout_scaled = self.accel_yout / 16384.0
        return self.accel_yout_scaled
    
    #as a note here, the 'scaled' values are the values in G's  
    def get_z_scaled(self):
        self.accel_zout = self.read_word_2c(0x3f)
        self.accel_zout_scaled = self.accel_zout / 16384.0
        return self.accel_zout_scaled
        
    def get_GX_scaled(self):
        GX = self.read_word_2c(0x43)
        GX_scaled = GX/131
        return GX_scaled
        
    def get_GY_scaled(self):
        GY = self.read_word_2c(0x45)
        GY_scaled = GY/131
        return GY_scaled
        
    def get_GZ_scaled(self):
        GZ = self.read_word_2c(0x47)
        GZ_scaled = GZ/131
        return GZ_scaled
        
    def testclass(self):
        return "test"

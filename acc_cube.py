"""
This is a cube imitating the position of an accelerometer.

The cube drawing is based off of code by Leonel Machava <leonelmachava@gmail.com>
	http://codeNtronix.com
	
The accelerometer data/interface is based off of code by Bitify and can be found at:
	http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html
"""

import sys, math, pygame, smbus
from operator import itemgetter

class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    def rotateX(self, angle):
        """ Rotates the point around the X axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - self.z * sina
        z = self.y * sina + self.z * cosa
        return Point3D(self.x, y, z)
 
    def rotateY(self, angle):
        """ Rotates the point around the Y axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - self.x * sina
        x = self.z * sina + self.x * cosa
        return Point3D(x, self.y, z)
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        rad = angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - self.y * sina
        y = self.x * sina + self.y * cosa
        return Point3D(x, y, self.z)
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        factor = fov / (viewer_distance + self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, self.z)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        pygame.init()

        self.screen = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Simulation of a rotating 3D Cube (http://codeNtronix.com)")
        
        self.clock = pygame.time.Clock()

        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]

        # Define the vertices that compose each of the 6 faces. These numbers are
        # indices to the vertices list defined above.
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        # Define colors for each face
        self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]

        #self.angle = 0
        
        #make an instance of the accelerometer class
        self.acc = Accelerometer()
        
        #set the initial angles to 0
        self.x_angle = 0
        self.y_angle = 0
        self.z_angle = 0
        
    def run(self):
        """ Main Loop """
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill((0,32,0))

            # It will hold transformed vertices.
            t = []
            
            for v in self.vertices:
				#get the angles from the accelerometer
				x = self.acc.get_x_scaled()
				y = self.acc.get_y_scaled()
				z = self.acc.get_z_scaled()
				
				#get the rotation values
				self.x_angle = self.acc.get_x_rotation(x,y,z)
				self.y_angle = self.acc.get_y_rotation(x,y,z)
				
				#this next value will be the z when I figure it out
				#self.z_angle = self.acc.get_z_rotation(x,y,z)
				
				#rotate around the x and y, leave z as 0
				'''here, rotateX is forward and backwards
				rotateY is around a vertical axis with positive numbers meaning CCW(left) rotation
				rotateZ is rotating around an axis pointing straight at you with positive numbers rotating CCW (left hand)'''
				r = v.rotateX(self.x_angle).rotateY(self.y_angle).rotateZ(self.z_angle)
				
				# Transform the point from 3D to 2D
				p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
				
				# Put the point in the list of transformed vertices
				t.append(p)
				
			# Calculate the average Z values of each face.
            avg_z = []
            i = 0
            for f in self.faces:
                z = (t[f[0]].z + t[f[1]].z + t[f[2]].z + t[f[3]].z) / 4.0
                avg_z.append([i,z])
                i = i + 1
            
            # Draw the faces using the Painter's algorithm:
            # Distant faces are drawn before the closer ones.
            for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
                face_index = tmp[0]
                f = self.faces[face_index]
                pointlist = [(t[f[0]].x, t[f[0]].y), (t[f[1]].x, t[f[1]].y),
                             (t[f[1]].x, t[f[1]].y), (t[f[2]].x, t[f[2]].y),
                             (t[f[2]].x, t[f[2]].y), (t[f[3]].x, t[f[3]].y),
                             (t[f[3]].x, t[f[3]].y), (t[f[0]].x, t[f[0]].y)]
                pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

                
            #self.angle += 1
            
            
            
            pygame.display.flip()
            
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

	def get_y_rotation(self,x,y,z):
		radians = math.atan2(x, self.dist(y,z))
		return -math.degrees(radians)

	#for backup: def get_x_rotation(self,x,y,z):
	def get_x_rotation(self,x,y,z):
		radians = math.atan2(y, self.dist(x,z))
		return math.degrees(radians)
	
	def get_x_scaled(self):
		self.accel_xout = self.read_word_2c(0x3b)
		self.accel_xout_scaled = self.accel_xout / 16384.0
		return self.accel_xout_scaled
		
	def get_y_scaled(self):
		self.accel_yout = self.read_word_2c(0x3d)
		self.accel_yout_scaled = self.accel_yout / 16384.0
		return self.accel_yout_scaled
		
	def get_z_scaled(self):
		self.accel_zout = self.read_word_2c(0x3f)
		self.accel_zout_scaled = self.accel_zout / 16384.0
		return self.accel_zout_scaled
		
	def testclass(self):
		return "test"


if __name__ == "__main__":
    Simulation().run()

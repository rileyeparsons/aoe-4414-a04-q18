# eci_to_ecef.py

# Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km
# Test Case: py eci_to_ecef.py 2054 4 29 11 29 3 3.3 5870.038832 3389.068500 3838.027968
# Converting from eci to ecef positions

# Parameters:
#  year : int 
#   year
#  month : int 
#   month
#  day : int 
#   day
#  hour : int 
#   hour
#  minute : int 
#   min
#  second : float
#   sec
#  eci_x_km : int | float | str
#   ECI X position in km
#  eci_y_km : int | float | str
#   ECI Y position in km
#  eci_z_km : int | float | str
#   ECI Z position in km


# Output:
#  eci : list
# eci position vector

# Written by Riley Parsons

import sys
import math

# "constants"
w = 7.292115e-5

# helper functions  
def ymdhms_tojd(y : int, m : int, d: int, hr: int, min: int, sec: float):
  jd = d - 32075 \
      + int(1461 * (y + 4800 + int((m - 14)/12))/4) \
      + int(367 * (m - 2 - int((m-14)/12) * 12)/12) \
      - int(3 * int(((y + 4900 + int((m-14)/12))/100))/4)
  
  jd_midnight = jd - 0.5
  d_frac = (sec + 60 * (min + 60 * hr ))/86400
  jd_frac = jd_midnight + d_frac
    
  return jd_frac

def jd_to_tut(jd_frac):
  return (jd_frac - 2451545.0)/36525

def tut_to_GMST_rads(tut):
  gmst_angle = 67310.54841 \
    + (876600 * 60 * 60 + 8640184.812866)*tut \
    + 0.093104*(tut**2) \
    + (-6.2e-6)*(tut**3)
  return ((gmst_angle % 86400) * w )

def z_rot(theta, eci_x_km, eci_y_km, eci_z_km):
  Rz = [[math.cos(-theta), -math.sin(-theta), 0], [math.sin(-theta), math.cos(-theta), 0], [0, 0, 1]]
  ecef_x_km = Rz[0][0]*eci_x_km + Rz[0][1]*eci_y_km + Rz[0][2]*eci_z_km
  ecef_y_km = Rz[1][0]*eci_x_km + Rz[1][1]*eci_y_km + Rz[1][2]*eci_z_km
  ecef_z_km = Rz[2][0]*eci_x_km + Rz[2][1]*eci_y_km + Rz[2][2]*eci_z_km

  return [ecef_x_km, ecef_y_km, ecef_z_km]

# main function
def eci_to_ecef(y, m, d, hr, min, sec, eci_x_km, eci_y_km, eci_z_km):
  
 jd_frac = ymdhms_tojd(y, m, d, hr, min, sec)
 t_ut = jd_to_tut(jd_frac)
 gmst_angle_rads = tut_to_GMST_rads(t_ut)
 eci = z_rot(gmst_angle_rads, eci_x_km, eci_y_km, eci_z_km)
 print(eci[0])
 print(eci[1])
 print(eci[2])
 return eci
  
# initialize script arguments
year = None
month = None
day = None
hour = None
min = None
sec = None
eci_x_km = None
eci_y_km = None
eci_z_km = None

# parse script arguments
if len(sys.argv)==10:
  year = int(sys.argv[1])
  month = int(sys.argv[2])
  day = int(sys.argv[3])
  hour = int(sys.argv[4])
  min = int(sys.argv[5])
  sec = float(sys.argv[6])
  eci_x_km = float(sys.argv[7])
  eci_y_km = float(sys.argv[8])
  eci_z_km = float(sys.argv[9])

else:
  print('Usage: python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km')
  exit()

# write script below this line
if __name__ == '__main__':
  eci_to_ecef(year, month, day, hour, min, sec, eci_x_km, eci_y_km, eci_z_km)
else:
  eci_to_ecef(year, month, day, hour, min, sec, eci_x_km, eci_y_km, eci_z_km)
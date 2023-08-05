from libc cimport math
import numpy as np
cimport numpy as np
cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef CreateVRMapping(const int vr_image_double_height, const int vr_image_width,
                      const int text_piece_height, const int text_piece_width,
                      const float azimuth_0, const float elevation_0,
                      np.float32_t[:,:] map1_right, np.float32_t[:,:] map2_right,
                      np.float32_t[:,:] map1_left, np.float32_t[:,:] map2_left,
                      float ipd=0.05, float distance=1.0, float scale_meter_per_pixel=0.01):
  cdef:
    float kFOVWidth = 360
    float kFOVHeight = 180
    int vr_image_height = vr_image_double_height // 2
  
  cdef:
    float center_z = distance * math.tan(elevation_0)
    
    int y, x
    float elevation, azimuth, alpha
    float l_x, l_z, r_x, r_z, direction
    
  for y in range(vr_image_height):
    for x in range(vr_image_width):
      
      elevation = 1.0 * (y - vr_image_height / 2) / vr_image_height * math.pi
      azimuth = 1.0 * (x - vr_image_width / 2) / vr_image_width * 2 * math.pi
      
      alpha = azimuth - azimuth_0
    
      l_x = distance * math.tan(alpha) - ipd / math.cos(alpha)
      l_z = (distance / math.cos(alpha)  - ipd * math.tan(alpha)) * math.tan(elevation)
      
      r_x = distance * math.tan(alpha) + ipd / math.cos(alpha)
      r_z = (distance / math.cos(alpha)  + ipd * math.tan(alpha)) * math.tan(elevation)
      
      direction = math.cos(alpha)
      
      if direction <= 0:
        map1_right[y, x] = -1
        map2_right[y, x] = -1
        map1_left[y, x] = -1
        map2_left[y, x] = -1
      else:
        map1_right[y, x] = r_x / scale_meter_per_pixel + text_piece_width // 2
        map2_right[y, x] = (r_z - center_z) / scale_meter_per_pixel + text_piece_height // 2
        map1_left[y, x] = l_x / scale_meter_per_pixel + text_piece_width // 2
        map2_left[y, x] = (l_z - center_z) / scale_meter_per_pixel + text_piece_height // 2
        
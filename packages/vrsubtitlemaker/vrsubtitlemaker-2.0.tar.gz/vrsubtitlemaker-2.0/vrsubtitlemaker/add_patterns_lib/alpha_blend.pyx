from libc cimport math
import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef AlphaBlend(np.uint8_t[:,:,:] img_back, np.uint8_t[:,:,:] img_front,
                 np.uint8_t[:,:,:] img_blended):
  cdef:
    int width = img_back.shape[1]
    int height = img_back.shape[0]
    int n_channels = img_back.shape[2]
    int i, j, c
    float alpha1, alpha2, alpha
    
  for i in range(width):
    for j in range(height):

      alpha1 = 1.0 * img_back[i, j, 3] / 255
      alpha2 = 1.0 * img_front[i, j, 3] / 255

      alpha = 1 - (1 - alpha1) * (1 - alpha2)

      for c in range(3):
        img_blended[i, j, c] = int((img_back[i, j, c] * alpha1 * (1 - alpha2) + img_front[i, j, c] * alpha2) / alpha)
      img_blended[i, j, 3] = int(alpha * 255)
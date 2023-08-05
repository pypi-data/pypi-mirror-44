from libc cimport math
import numpy as np
cimport numpy as np
cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef ReplaceColorCython(np.uint8_t[:,:,:] image, np.uint8_t[:] font_color, np.uint8_t[:] bg_color):
  cdef:
    int i, j, c
    int height = image.shape[0]
    int width = image.shape[1]
    int n_channels = image.shape[2]
  for i in range(height):
    for j in range(width):
      if image[i,j,0] < 100:
        for c in range(n_channels):
          image[i,j,c] = font_color[c]
      else:
        for c in range(n_channels):
          image[i,j,c] = bg_color[c]
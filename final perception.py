import numpy as np
import cv2

##------------------------------------------------------------------------------------------------------------------(1)
    # Identify pixels above the threshold
    # Threshold of RGB > 160 does a nice job of identifying ground pixels only
## navigable train is tresholded with high values of RED GREEN BLUE (grey color as image will be processed in single channel)    
def color_thresh(img, rgb_thresh=(160, 160, 160)):
    
    # Create an array of zeros same xy size as img, but single channe (z Represinting RGB is set to zero) 
    color_select = np.zeros_like(img[:,:,0])
    
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met

    above_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select

def obstacles_tresh(img, obs_thresh=(160, 160,160 )):
    color_select = np.zeros_like(img[:,:,0])
    obs = (img[:,:,0] <= obs_thresh[0])| (img[:,:,1] <= obs_thresh[1]) | (img[:,:,2] <= obs_thresh[2])
    color_select[obs] = 1
    return color_select
## rocks are thresholded with high values of RED & GREEN with much less BLUE  90, 90, 30(shadowed yellow color is our threshold for rocks)

def rock_tresh(img, yellow_thresh=(90, 90, 30)):
    color_select = np.zeros_like(img[:,:,0])
    rock = (img[:,:,0] > yellow_thresh[0]) & (img[:,:,1] > yellow_thresh[1]) & (img[:,:,2] < yellow_thresh[2])
    color_select[rock] = 1
    return color_select
    
    
    # Apply the above functions in succession
def calc_forward_dist(path_dists, path_angles):
	abs_angles = np.absolute(path_angles / sum(path_angles))
	idx = np.abs(abs_angles).argmin()
	return path_dists[idx]
##------------------------------------------------------------------------------------------------------------------(1)
##------------------------------------------------------------------------------------------------------------------(2)
# Define a function to convert from image coords to rover coords

def rover_coords(binary_img):
    # Identify nonzero pixels of the input image ,information of image 
    ypos, xpos = binary_img.nonzero()# (y,x)
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
  
#binary_img.shape[0]>>height(vertical)
#binary_img.shape[1]>>width(horizontal)
# # reversing where x in image coords is y in rover coords and vice versa 
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)#
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)#

    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel (magnitude)
    dist = np.sqrt(x_pixel*2 + y_pixel*2)
    # Calculate angle away from vertical for each pixel(
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles
##------------------------------------------------------------------------------------------------------------------(2)


# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated


##------------------------------------------------------------------------------------------------------------------(4)

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world
##------------------------------------------------------------------------------------------------------------------(4)
##------------------------------------------------------------------------------------------------------------------(5)
# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped


# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    if Rover.start_pos == None:      
       Rover.start_pos = Rover.pos      #Records the starting point to return to later
    # NOTE: camera image is coming to you in Rover.img
    
 # 1) Define source and destination points for perspective transform
        # The destination box will be 2*dst_size on each side
    dst_size = 5 # output image 5x5
    # Set a bottom offset to account for the fact that the bottom of the image 
    # is not the position of the rover but a bit in front of it
    # this is just a rough guess, feel free to change it!
    bottom_offset=6 
    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])# rough estimation
    destination = np.float32([[Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - bottom_offset],
                      [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - bottom_offset],
                      [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset], 
                      [Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],
                      ])
    # 2) Apply perspective transform
    warped = perspect_transform(Rover.img, source, destination)
    thresh = color_thresh(warped)
    
   ##------------------------------------------------------------------------------------------------------------------(5)
   ##------------------------------------------------------------------------------------------------------------------(1)
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    rocks = rock_tresh(warped)
    obstacles = obstacles_tresh(warped)   
    ##areas
    
    # 4) Update Rover.vision_image (this will be displayed on left side of screen) our image is 200 x200 pixels
    Rover.vision_image[:,:,2] = thresh*200 #navigable train set to Blue
    Rover.vision_image[:,:,1] = rocks *200# rocks Set to GREEN
    Rover.vision_image[:,:,0] = obstacles*200#obstacles set to Red
   ##------------------------------------------------------------------------------------------------------------------(1)
   ##------------------------------------------------------------------------------------------------------------------(2)
        
    Rover.nav_area = np.sum(thresh)
    Rover.ob_area = np.sum(obstacles)
   
    # 5) Convert map image pixel values to rover-centric coords
    # Calculate pixel values in rover-centric coords and distance/angle to all pixels
    xpix, ypix = rover_coords(thresh)
    obxpix, obypix = rover_coords(obstacles)
    roxpix, roypix = rover_coords(rocks)
  
      
    dist, angles = to_polar_coords( xpix, ypix)
   
    
   ##------------------------------------------------------------------------------------------------------------------(2)
   ##----------------------------------------------
 
   ##------------------------------------------------------------------------------------------------------------------(2)
   ##------------------------------------------------------------------------------------------------------------------(4)
    # 6) Convert rover-centric pixel values to world coordinates 
    worldmap = Rover.worldmap
    scale = 20
    
   
    obstacle_x_world, obstacle_y_world = pix_to_world(obxpix,obypix,Rover.pos[0],Rover.pos[1],Rover.yaw,worldmap.shape[0],scale)
    rock_x_world, rock_y_world = pix_to_world(roxpix,roypix,Rover.pos[0],Rover.pos[1],Rover.yaw,worldmap.shape[0],scale)
    navigable_x_world, navigable_y_world = pix_to_world(xpix,ypix,Rover.pos[0],Rover.pos[1],Rover.yaw,worldmap.shape[0],scale)
     # 7) Update Rover worldmap (to be displayed on right side of screen)  
    if ((Rover.pitch < 1 or Rover.pitch > 359) and (Rover.roll < 1 or Rover.roll > 359)):
          Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] = 200
          Rover.worldmap[navigable_y_world, navigable_x_world, 0] = 0
          Rover.worldmap[rock_y_world, rock_x_world, 1] = 200
          Rover.worldmap[navigable_y_world, navigable_x_world, 2] = 200
    ##------------------------------------------------------------------------------------------------------------------(4)
        
   
    ## for finding rocks   
    distrock, anglesro = to_polar_coords(roxpix, roypix)
    ## obstacles angles
    distob, anglesob = to_polar_coords(obxpix, obypix )
    Rover.rock_angle = anglesro
    Rover.rock_dist = distrock
    Rover.ob_angle = anglesob
    Rover.ob_dist = distob
    
    # 8) Convert rover-centric pixel positions to polar coordinates
    Rover.nav_dists = dist
    Rover.nav_angles = angles
    
    return Rover

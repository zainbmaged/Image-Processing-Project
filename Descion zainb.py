import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
    
    if(Rover.rock_angle is not None):
       Rover.samples_insight=1
    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
          
        
        
        
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            loop_flag = 0     
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward :
            ##check that rover is not looping around itself
                
                if Rover.steer > 14.5 and Rover.vel > 2: 
                    if loop_flag==0 or loop_flag==1:
                      loop_flag+=1
                    if loop_flag ==2:
                      loop_flag=0
                      Rover.steer = 13
                      Rover.mode = 'stop'
                if Rover.steer < -14.5 and Rover.vel > 2:  
                    Rover.steer = -13
                    Rover.mode = 'stop'
              
              
                    
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel :
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
            
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -10, -15, 15)
            ## rock in sight     
            if Rover.samples_insight==1: #rock found
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'rock' #enter rock searching mode   
           
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward :
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'
            elif np.min(Rover.nav_dists) < Rover.stop_forward :
                   Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + 14, -15, 15)
        ## mode is rock            
        elif Rover.mode == 'rock':
            # find the rock direction
            # far detecting
                    
            Rover.brake = 0
            if Rover.samples_insight == 1:
                if Rover.vel > 0:
                    Rover.steer=np.mean(Rover.rock_angle * 180/np.pi)
                else: 
                    Rover.steer= - np.mean(Rover.rock_angle * 180/np.pi)
                Rover.rockcount = 0
                if Rover.vel < Rover.max_vel/2:
                    Rover.throttle = Rover.throttle_set/2
                    Rover.brake = 0
                else:
                    Rover.throttle = 0
                    Rover.brake = 0
                
            else:                
                Rover.rockcount += 1
                if Rover.rockcount >=10:
                    Rover.brake = Rover.brake_set
                else:
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -10, -15, 15) #lost track of rock? keep searching!
                    Rover.rockcount = 0
                    
            
            if Rover.near_sample: #close enough?
                Rover.brake=1
                Rover.throttle = 0
                Rover.rockcount = 0
                 
                 
            # anti_block operation       
            if Rover.vel < Rover.max_vel :
            
                    
                    # count how long we have been in 'slow motion' mode
                    if Rover.vel < 0.5:
                        Rover.stuck_count += 1
                       
                    else:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.vel < -0.5:
                        Rover.stuck_count = 0
                        Rover.back = 0
                        
                    if Rover.stuck_count < 5 or Rover.back > 5: # if we haven't been 'slow' for long or have been drive back for a while
                        # Set throttle value to throttle setting and not stucked
                        Rover.throttle = Rover.throttle_set/2
                        
                        
                    else:
                        Rover.throttle = - Rover.throttle_set # try drive back
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -12, -15, 15)
                        Rover.back += 1
                        Rover.mode = 'forward'
                        
                        
            else:
                        Rover.throttle = - Rover.throttle_set # try drive back
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -10, -15, 15)
                        Rover.back += 1
                        Rover.mode = 'forward'    
        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
        
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = 15 
                   
                    # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward :
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -12, -15, 15)
                    Rover.mode = 'forward'
                
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
    
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

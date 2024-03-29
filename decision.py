import numpy as np


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!
     # Once we are done we need to get back to the starting position
    if Rover.total_time >= 700:
         print("GO TO START")
         dist_start = np.sqrt((Rover.pos[0] - Rover.start_pos[0])**2 + (Rover.pos[1] - Rover.start_pos[1])**2)
        # Make sure we are heading in right general direction
        # TODO
        # If we are in 10 meters steer to starting point
   
        # If we are in 3 meters just stop
         if dist_start < 10.0 :
            print("10m From start")
            Rover.mode = 'stop'
            Rover.throttle = 0
            Rover.brake = Rover.brake_set
            return Rover
    print(Rover.samples_collected)
    print(Rover.total_time)
    # Example:
    # Check if we have vision data to make decisions with
    if len(Rover.ob_dist)<=100 and Rover.rock_angle is None :
                    if Rover.vel !=0:
                        Rover.brake=10
                    Rover.steer=-15
                    Rover.throttle=0
                    Rover.brake=0
                    if nav_area>650 :
                        Rover.mode='forward'   
                    if nav_area<650 :
                        Rover.mode='stop'
       
        # Check if there are rocks
    if Rover.rock_angle is not None and len(Rover.rock_angle) > 0:
        Rover.mode = 'forward'
        Rover.steer = np.clip(np.mean(Rover.rock_angle * 180/np.pi), -15, 15)
        # Move towards the rock slowly
        if not Rover.near_sample:
            if Rover.vel < Rover.max_vel/2:
                Rover.brake = 0
                Rover.throttle = 0.1
            else:
                Rover.throttle = 0
                Rover.brake = 1
        # Stop when close to a rock.
        else:
            Rover.throttle = 0
            Rover.brake = Rover.brake_set
    elif Rover.nav_angles is not None:
          
        
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
             
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward :
            ##check that rover is not looping around itself
                
                if Rover.steer > 14.5 and Rover.vel > 2.3: 
                    Rover.brake = Rover.brake_set
                    Rover.steer = 15
                    Rover.mode = 'stop'  
                if Rover.steer < -14.5 and Rover.vel > 2.3:  
                    Rover.brake = Rover.brake_set
                    Rover.steer =-15
                    Rover.mode = 'stop'
              
               
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle 
                if Rover.vel < Rover.max_vel :
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15 but always go left
                
                
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) -9, -15, 15)
           
           
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
                    Rover.steer = 20
                   
                    # Could be more clever here about which way to turn
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward :
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + -9, -15, 15)
                    Rover.mode = 'forward'
       
                
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
    
   # If in a state where want to pick ip the rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.mode = 'stop'
    
    return Rover

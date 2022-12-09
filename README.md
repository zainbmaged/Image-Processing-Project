# Image-Processing-Project
--------------------------------------------------------------------------------------------------------------------------------------------------------
## Team Members

Name              | ID
------------------|---------------
Zainb Maged Arafa Zahran|1901420
Reem Hassan Ahmed |1901677
Rana Mohamad Ahmad Abdel Salam |1901208
Nada Waleed Mohammed Ebed| 1901544
Sara Ramadan Mohamed |1901309


## Submission

- The code well written and commented:
submitted in this repo
- The readme should also have clear instructions on how to run your code:
submitted below
- A Jupiter-notebook showing the result of your pipeline on the provided test images:
submitted in this repo
- The output of your pipeline on the provided test videos:
[ link ]
- A report containing the methods used in the pipeline and explaining them in detail:
[ link to report ] https://docs.google.com/document/d/1OUNwhvXxpj7jac4rH3VyrG8Wu1kkk7aooFBvtpSIKTg/edit?usp=sharing
- Finally, your code should support a debugging mode whether it was a video or a single image.
When this mode is activated, your pipeline should be showing all the stages that your code is
going through

## Instructions on How to run the code
### Autonomouse mode

The file called drive_rover.py is what you will use to navigate the environment in autonomous mode. This script calls functions from within perception.py and decision.py. The functions defined in the IPython notebook are all included inperception.py and it's your job to fill in the function called perception_step() with the appropriate processing steps and update the rover map. decision.py includes another function called decision_step(), which includes an example of a conditional statement you could use to navigate autonomously. Here you should implement other conditionals to make driving decisions based on the rover's state and the results of the perception_step() analysis.

drive_rover.py should work as is if you have all the required Python packages installed. Call it at the command line like this:

python drive_rover.py

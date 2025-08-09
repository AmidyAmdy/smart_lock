import subprocess

def photo():
    subprocess.run([
        "libcamera-still",
        "-n",              
        "--immediate",    
        "-t", "1",         
        "-o", "capture.jpg"
    ], check=True)
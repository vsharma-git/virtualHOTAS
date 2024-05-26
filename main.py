import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pyvjoy import VJoyDevice

app = Flask(__name__)
socketio = SocketIO(app,debug=True)

pitchHome = 0
yawHome = 0
rollHome = 0

pitch = 0
yaw = 0
roll = 0

gamepadStatus = False

buttonState =  ['0']*32

def setup():
    '''
    This will always connect to VJoyDevice: 1. 
    Open to vJoyConf - Configure vJoy Devices to change the number of axes and buttons.
    '''
    global virtual_joystick
    virtual_joystick = VJoyDevice(1)

def map_value(value, in_min, in_max, out_min, out_max):
    '''
    Maps a value from one range to another
    Parameters:
        value (float): The value to map
        in_min (float): The minimum value of the input range
        in_max (float): The maximum value of the input range
        out_min (float): The minimum value of the output range
        out_max (float): The maximum value of the output range
    '''
    mapped_value = int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    if (mapped_value < out_min):
        mapped_value = out_min
    if mapped_value > out_max:
        mapped_value = out_max
    return mapped_value


@app.route('/')
def index():
    '''
    This is the main page of the application.
    '''
    setup()
    return render_template('index.html')
    

@socketio.on('orientation')
def handle_orientation(data):
    '''
    This function handles the orientation data from the client.
    It maps the pitch, yaw, and roll values to the virtual joystick.
    '''
    global pitch, yaw, roll
    print(f"Received Orientation Data: {data}")
    pitch = data['pitch'] #beta
    pitch_mapped = map_value(pitch, -1, 1, 0, 32767)
    yaw = data['yaw'] #alpha
    yaw_mapped = map_value(yaw, -1, 1, 0,32767)
    roll = data['roll'] #gamma
    roll_mapped = map_value(roll, -1, 1, 0, 32767)
    headYaw = map_value(data['headYaw'], -1, 1, 0, 32767)
    headPitch = map_value(data['headPitch'], -1, 1, 0, 32767)
    
    # print(f"pitch: {pitch_mapped}, yaw: {yaw_mapped}, roll: {roll_mapped}")    
    # print(pitch," ",pitchHome," ", data['pitch'])
    # You can add more processing or send the data to other clients if needed
    # Update the virtual joystick state
    virtual_joystick.data.wAxisXRot = int(pitch_mapped)
    virtual_joystick.data.wAxisYRot = int(yaw_mapped)
    virtual_joystick.data.wAxisZRot = int(roll_mapped)
    virtual_joystick.data.wAxisX = int(headYaw)
    virtual_joystick.data.wAxisY = int(headPitch)

    virtual_joystick.update()
    # socketio.emit('orientation_updated', {'pitch': map_value(virtual_joystick.data.wAxisXRot,0,32767,-25,25),'roll': map_value(virtual_joystick.data.wAxisYRot,0,32767,-30,30),'yaw':map_value(virtual_joystick.data.wAxisZRot,0,32767,-20,20)})

@socketio.on('orientationPhone')
def handle_orientation(data):
    '''
    This function handles the orientation data from the client.
    It maps the pitch, yaw, and roll values to the virtual joystick.
    It also sends the mapped values back to the client.
    '''
    if gamepadStatus:
        return
    global pitch, yaw, roll
    print(f"Received Orientation Data: {data}")
    pitch = pitchHome-data['pitch'] #beta
    pitch_mapped = map_value(pitch, -25, 25, 0, 32767)
    yaw = yawHome-data['yaw'] #alpha
    yaw_mapped = map_value(yaw, -30, 30, 0, 32767)
    roll = rollHome-data['roll'] #gamma
    roll_mapped = map_value(roll, -20, 20, 0, 32767)
    # print(f"pitch: {pitch_mapped}, yaw: {yaw_mapped}, roll: {roll_mapped}")    
    # print(pitch," ",pitchHome," ", data['pitch'])
    # Update the virtual joystick state
    virtual_joystick.data.wAxisXRot = int(pitch_mapped)
    virtual_joystick.data.wAxisYRot = int(yaw_mapped)
    virtual_joystick.data.wAxisZRot = int(roll_mapped)

    virtual_joystick.update()
    socketio.emit('orientation_updated', {'pitch': map_value(virtual_joystick.data.wAxisXRot,0,32767,-25,25),'roll': map_value(virtual_joystick.data.wAxisYRot,0,32767,-30,30),'yaw':map_value(virtual_joystick.data.wAxisZRot,0,32767,-20,20)})

        

@socketio.on('orientationHOME')
def handle_orientation_home(data):
    '''
    When reset rotation is pressed, the home orientation is saved and the pitch, yaw, and roll are set to 0.
    '''
    global pitchHome, yawHome, rollHome
    # print(f"Received Orientation Data: {data}")
    print("********* Reset Orientation *********")
    if gamepadStatus:
        print("Gamepad Connected")    
        pitchHome = 0
        yawHome = 0
        rollHome = 0
        pitch = 0
        yaw = 0
        roll = 0
        virtual_joystick.data.wAxisXRot = 0
        virtual_joystick.data.wAxisYRot = 16383
        virtual_joystick.data.wAxisZRot = 0
    else:
        print("Gamepad Disconnected")
        pitchHome = data['pitch']
        yawHome = data['yaw']
        rollHome = data['roll']


    print(f"pitch: {pitchHome}, yaw: {yawHome}, roll: {rollHome}")

@socketio.on('update_joystick_throttle')
def handle_update_joystick(data):
    '''
    When the throttle slider is moved, the virtual joystick's throttle value is updated.
    '''
    x_axis_value = int(data['joystick_value'])

    # Update the virtual joystick state
    virtual_joystick.data.wDial = x_axis_value
    virtual_joystick.update()

@socketio.on('update_joystick_flaps')
def handle_update_joystick(data):
    '''
    When the flaps slider is moved, the virtual joystick's throttle value is updated.
    '''
    # print(data)
    flaps_axis_value = int(data['flaps_value'])

    # Update the virtual joystick state
    virtual_joystick.data.wSlider = flaps_axis_value
    virtual_joystick.update()

@socketio.on('button_press')
def handle_button_press(data):
    '''
    When a button is pressed, the virtual joystick's button state is updated.
    To simulate a button press, the virtual joystick's button state is flipped after 0.25 seconds
    
    '''
    # setup()
    print(data["button"])
    print("virtual_joystick.data.lButtons",virtual_joystick.data.lButtons)
    buttonState = ['0'] * 32
    buttonState[-int(data["button"])] = '1'
    flipped_binary_string = ''.join(buttonState)
    # print(buttonState)
    virtual_joystick.data.lButtons = int(flipped_binary_string,2)  
    # flip_bit_prep(1)
    virtual_joystick.update()
    
    time.sleep(0.25)    
    buttonState = ['0'] * 32
    flipped_binary_string = ''.join(buttonState)
    virtual_joystick.data.lButtons = int(flipped_binary_string,2)  
    # flip_bit_prep(1)
    virtual_joystick.update()

@socketio.on('gamepadButton')
def handle_gamepad_button_press(data):
    '''
    Get the button status from the gamepad and update the virtual joystick.
    '''
    # print(data["gamepadButtonData"])
    # print("virtual_joystick.data.lButtons",virtual_joystick.data.lButtons)
    gamepadButtons = data["gamepadButtonData"]
    gamepadButtons.reverse()
    print(gamepadButtons)
    binary_string = ''.join(map(str, gamepadButtons))
    virtual_joystick.data.lButtons = int(binary_string,2)  
    virtual_joystick.update()

@socketio.on('gamepadConnection')
def getGamepadConnectionStatus(data):
    '''
    Get the gamepad connection status.
    Reset all values
    '''
    global gamepadStatus,pitch, yaw, roll,pitchHome, yawHome, rollHome
    gamepadStatus = data["connected"]
    print("Gamepad connection: ",gamepadStatus)

    pitchHome = 0
    yawHome = 0
    rollHome = 0
    pitch = 0
    yaw = 0
    roll = 0
    virtual_joystick.data.wAxisXRot = 0
    virtual_joystick.data.wAxisYRot = 16383
    virtual_joystick.data.wAxisZRot = 0
    virtual_joystick.data.wAxisX = 0
    virtual_joystick.data.wAxisY = 0
    buttonState = ['0'] * 32
    buttonState = ''.join(buttonState)
    virtual_joystick.data.lButtons = int(buttonState,2)  
    virtual_joystick.update()

if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, debug=True,host='192.168.1.23', port=5000)

# Virtual HOTAS

A customizable virtual controller to play flight sims. Supports both modes - phone only and phone with controller.

## Background

It is hard to play flight simulators without a Hands On Throttle-And-Stick (HOTAS). To accurately control the throttle, you need to know its position at all time, keyboards and controllers can't do that. To control the joystick, you need analog input, most keyboards cant do that but controllers are great at it. 

This app converts your phone into a virtual HOTAS. You can now control your throttle and flaps using sliders, and your joystick using your phone's sensors.

You can also extend the capability of the app by pairing a controller.

## Demo
[![Virtual HOTAS Demo](docs/youtube-thumbnail.png)](https://youtu.be/bFi3iqamPNk)


## Table of contents
- [Virtual HOTAS](#virtual-hotas)
  - [Background](#background)
  - [Demo](#demo)
  - [Table of contents](#table-of-contents)
  - [🎁 Installation](#-installation)
  - [🏃‍♀️ Quick Start](#️-quick-start)
  - [▶ Usage](#-usage)
  - [⭐ Features](#-features)
  - [🧩 Components](#-components)
  - [⚙ Customization](#-customization)
    - [Change button names](#change-button-names)
    - [Change layout](#change-layout)
    - [Change sliders](#change-sliders)
    - [Add buttons](#add-buttons)
  - [❔ Troubleshooting](#-troubleshooting)
    - [I can't figure out how to fly](#i-cant-figure-out-how-to-fly)
    - [General troubleshooting steps](#general-troubleshooting-steps)
    - [Throttle in Microsoft Flight Simulator is erratic](#throttle-in-microsoft-flight-simulator-is-erratic)
    - [How do I know I'm connected?](#how-do-i-know-im-connected)
  - [🚀 Beyond HOTAS](#-beyond-hotas)
  - [🗺 Roadmap](#-roadmap)
  - [🎹 Keybindings](#-keybindings)
    - [Phone only](#phone-only)
    - [Phone with Backbone](#phone-with-backbone)


## 🎁 Installation
Installation guide - https://youtu.be/EyKlp2h1qXQ

Steps - 
1. Download and install vJoy from https://www.vjoy.org/download-for-windows.
2. Download and install Python https://www.python.org/downloads/.
3. Install the app
![Installation steps](docs/installation-steps-with-arrows.png)
   1. Navigate to the repo in your browser.
   2. Click on Code.
   3. Click on Download ZIP.
   4. Right click on the downloaded ZIP file.
   5. Extract the downloaded file.
   6. Open the folder.
   7. Run installer.bat.
4. Configure vJoy \
By default vJoy is set for 8 buttons. To make this app work with controllers, we need to set it to 32 buttons.
 ![vJoy configuration steps](docs/vjoy-config.png)
   1. Go to windows start menu
   2. Search for vJoy
   3. Open Configure vJoy
   4. Change Number of Buttons to 32
   5. Click on Apply

## 🏃‍♀️ Quick Start

Complete [Installation](#installation) section. \
Double click on  run.bat\
Navigate to the url on your phone. \
Set up key bindings in Microsoft Flight Simulator.

## ▶ Usage

- Run main.py using this command (If using a virtual environment then, first activate it)
- The terminal will give you the url of the server.
- Open url on your phone.


## ⭐ Features 
- 2 configurable sliders. Default - Flaps and Throttle.
- 5 configurable buttons. 
- Phone's sensors for joystick input.
![Screenshot of UI](docs/buttonsandslider.gif)

## 🧩 Components

Basic rundown of different parts of this app - \
**vJoy** - Creates a virtual joystick that this app uses. https://www.vjoy.org/ \
**Monitor vJoy** - Comes with vJoy. Use this to monitor and troubleshoot input. \
**pyVjoy** - Python bindings for vJoy https://github.com/maxofbritton/pyvjoy \
**index.html** - UI for the this app. \
**main.py** - Backend to process the data from index.html.

## ⚙ Customization

To keep things simple. All css, body and scripts are in index.html.

### Change button names

Change the text in the button. 
```html
<button class="btn btn-primary button" onclick="buttonPress(1)">Gear Up</button>
```

### Change layout

The layout is done using CSS Grids.

### Change sliders

Sliders are done using noUiSlider. https://refreshless.com/nouislider/

### Add buttons

Add a button in index.html using using the snippet below. Change the number in buttonPress(#) to an unassigned number.

```html
<button class="btn btn-primary button" onclick="buttonPress(#)">Gear Up</button>
```

Update layout. Based on the type of customization you might have to update the CSS grid.\
Open vJoyMonitor to check if the input is being reported correctly.

## ❔ Troubleshooting

### I can't figure out how to fly 
- Tap the reset button while flying to level the aircraft. Make small adjustments to your phone and you'll get the hang of it. 
- Check if the controls are mapped inside MSFS.

### General troubleshooting steps
Run python app again and then refresh webpage.
Refresh webpage.
Check vJoy Monitor

### Throttle in Microsoft Flight Simulator is erratic

This is a known issue for MSFS. It is not just for this app, it seems to be an issue for other peripherals too. \
To fix - Disable AI assists in MSFS.

### How do I know I'm connected?
Open vJoy Monitor and look see if your input is being registered.

## 🚀 Beyond HOTAS
1. Accessibility tools - Just by renaming the buttons we can configure this for any game. By running the app on a bigger screen, we can make bigger targets for increased accessibility. 
2. Stream deck - you know how to make a UI and send inputs, it should be possible to connect to an API for OBS. 

## 🗺 Roadmap
- (✔ Done 30MAY2024) Update logic of UI buttons to report long press. Right now, I can only record a tap but not long or sustained button presses.
- Update logic of the css grid so that adding buttons does not require updating CSS for each button. 

## 🎹 Keybindings 
### Phone only
The buttons on the UI will register as 21 and beyond on vJoy
https://youtu.be/crPxxUd480M

### Phone with Backbone
All the buttons and axes of Backbone are mapped in the order in which they are reported from the controller.
https://youtu.be/ZmDCDITcV3w

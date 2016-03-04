# Space machines
Space machines is python-based project for controlling or interfacing with simple machines from a Raspberry Pi.  It was originally written for hackerspace Sector67, then cleaned up and made available for other hackerspaces or anywhere that has a space with members and needs to manage members and access to tools.  Some example applications include controlling access to a door via RFID keys, or tracking and billing members for laser cutter usage.
If you are looking for hard real-time control of things like robots or machine tools, this is likely not the project for you.  However, if you want to control access to a door or authorize the use of a machine via RFID, then you might find this project helpful.
# Architecture

The basic architecture consists of a number of state machines concurrently interacting with each other via messages.  Each “machine” or interface device you want to control will need to be modeled and implemented as a state machine in python using a simple state machine framework.  Individual state machines can then be wired together, via ini file configuration.  By way of example, a simple enable/disable toggle switch on a RPI GPIO pin could be modeled as one machine acting as an unlock/lock switch on a door while a serial-based RFID reader was configured as another machine.  In this example, the GPIO pins and serial rates would be configured via the ini-format config file.

Not every customization will be able to be done via configuration.  Some will require coding changes, but the goal is to be able to implement as many systems as possible via simple configuration changes.
The state machine model is based on the PyStates project by Eric Gradman, with code available at [his github site](https://github.com/egradman/pystates/blob/master/pystates/pystates.py)

We've made some modifications so that each state machine maintains a thread for updating its own state.  Using that simple state machine framework, each state is implemented as a function of a class.  Message passing is handled using the native Python thread-safe Queue class, with a central queue for publishing messages and each component with their own queues for consuming messages.  Messages take the form of a Python dictionary, with a minimum of an “event” entry describing the event via a string.  Additional metadata values, such as the RFPD key in the case of an RFID reader, are passed as key/value pairs in the message dictionary.

# Interactive testing without RPi access
The code is designed to be able to be developed and tested outside of a RPi envornment.  By using the gui-based components and configuring the show_gui option to true you can interact with the gui elements to change the state of the system and confirm proper state machine behavior, etc.  Any component you want to interact with via the gui must implement a config_gui method that initializes the apporpriate TkInter components give the root object.  Components that do not need to interact with the GUI can implement an empty config_gui method.

# Unit testing of components
The RPi GPIO-specific components are designed to be small and decoupled from the main machine logic.  It is hoped that this will make unit testing simpler.  Components can be directly unit tested by directly instantiating and directly passing messages.  Systems of components can be created using configuration files for integration-type testing.

TODO: provide an example

# Installation and setup
Since this project is designed for use on a Raspberry Pi, Pi-specific setup instructions are included here.  You will generally want to start with a modern Raspbian build, currently Jessie.  On top of that, you will want to:

TODO, finish documentation: 
## disable serial TTY
## disable screen saver
## download and install state_machine and any dependencies
## script state_machine startup on reboot

## install the rpi_ws281x dependency
To install the neopixel library for the raspberry pi, you can run:

    sudo pip install rpi_ws281x

this will install the necessary native libraries and python modules.  Code using the neopixel library must be run as root.

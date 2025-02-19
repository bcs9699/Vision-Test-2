Core Components
-------------

    Microcontroller/Processor:
        • Raspberry Pi 4 (4GB or 8GB)
            - Ideal for running Python scripts, Roboflow workflows, and handling servo control
        • Alternative: NVIDIA Jetson Nano 
            - Recommended if more GPU power needed for AI models

    Camera:
        • Raspberry Pi Camera Module v3
            - High-resolution
            - Compatible with Raspberry Pi
            - Wide field of view
        • Alternative: Any USB webcam (e.g., Logitech C920)
            - Provides more flexibility

    Pan-Tilt Mechanism:
        • Pan-Tilt Servo Kit
            - Basic two-axis pan-tilt kit with servo motors
            - Must include mounting brackets for camera
            - Example: Adafruit Pan-Tilt HAT with servos

    Servos:
        • SG90 or MG90S Micro Servos
            - Affordable and sufficient for lightweight setups
        • TowerPro MG995 (for heavier cameras)
            - Provides more torque for larger payloads

    Laser Distance Sensor (Optional):
        • TF Mini Plus LiDAR
            - Provides accurate distance measurement
            - Enhances drone tracking capabilities

Power Supply
-----------

    Power for Raspberry Pi:
        • 5V/3A USB-C power adapter

    Power for Servos:
        • 6V/5A power supply
            - Separate from Pi power to ensure sufficient current
        • UBEC or servo driver board
            - For voltage regulation

Motor Driver for Servos
----------------------

    • Adafruit PCA9685 16-Channel PWM/Servo Driver
        - Efficiently handles multiple servos
        - Easy Raspberry Pi integration

Mounts and Enclosures
--------------------

    Camera Mount:
        • Compatible mount for chosen camera/webcam

    Project Enclosure:
        • Protective case for Raspberry Pi and power modules

Cables and Connectors
--------------------

    • Jumper Wires
        - Male-to-female
        - Male-to-male

    • Servo Extension Cables
        - For driver board connections

    • USB Cables
        - Power delivery
        - Peripheral connections

Peripherals for Setup
--------------------

    • Monitor, Keyboard, and Mouse
        - Required for initial Raspberry Pi setup

    • MicroSD Card
        - 32GB or 64GB Class 10
        - Recommended: SanDisk brand
        - For Raspberry Pi OS installation

Optional Enhancements
--------------------

    • Wide-Angle Lens
        - Expands camera field of view
        - Better sky coverage

    • GPS Module
        - Global position tracking
        - Useful for outdoor applications

    • Battery Pack
        - Enables portable operation
        - Recommended for mobile setups
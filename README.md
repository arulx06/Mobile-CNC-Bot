# 🛠️ Mobile CNC Writer

A lightweight, mobile CNC writing machine built using Arduino, GRBL firmware, Python, and a custom mobile chassis. Designed for basic plotter-based writing on paper with optimized mechanical movement using omni wheels and N20 gear motors.

---

## 📸 Project Demo

![Demo Image](Images/assembled_cnc.jpg)

---

## 🧠 Features

* 🧾 GRBL-based CNC control
* 🔁 Stepper motor + DC motor hybrid movement
* 🧠 Controlled via G-code and Python
* 🔧 Mobile base with omni wheels
* 🪶 Lightweight pen-holding mechanism

---

## 🚀 Getting Started

### 1. 🧩 Hardware Setup

#### Components Used:

* [Omni Wheel Round Chassis](https://robu.in/product/easymech-poly-omni-wheel-round-chassis/)
* [N20 12V 60RPM Micro Gear Motor](https://robu.in/product/n20-12v-60-rpm-micro-metal-gear-box-dc-motor/)
* A4988 Stepper Driver
* CNC Shield V3
* Arduino Uno
* L293D Motor Driver
* 28BYJ-48 Stepper Motor
* Power supply (6V–12V recommended)
* Custom lightweight pen mount

#### Connections:

* Connect Arduino to CNC Shield V3.
* A4988 on the shield controls the stepper motor (pen Z-axis).
* L293D is used for driving N20 DC motors (X/Y movement).
* Supply 12V to the CNC shield via barrel jack.
* Follow detailed schematic in [`Hardware/Wiring_Diagram.png`](Hardware/Wiring_Diagram.png).

---

## 🧠 Software

### 2. 🔧 Arduino

Upload the GRBL firmware to Arduino Uno.

> 🔌 Use the `cnc_writer_grbl.ino` from [`Arduino_Code/`](Arduino_Code/) if you’re modifying GRBL or testing motors.

### 3. 🐍 Python Interface

Python script to send G-code commands to GRBL over serial.

```bash
python Python_Code/send_gcode.py
```

Modify the serial port and baud rate as required in the script.

---

## 📽️ Helpful Resources

* [Demo CNC Video 1](https://www.youtube.com/watch?v=S8YVlR_1hlo)
* [Pen-Lift Mechanism](https://youtu.be/Li_atZt4qUI?si=kLkLP7uPw5nB3DAe)

---

## 📚 Project Notes

> Refer to [`Resources/Notes.md`](Resources/Notes.md) for hardware-related decisions, power supply concerns, and troubleshooting logs.

Key Observations:

* 28BYJ stepper motor needs to be tested with GRBL and A4988.
* Avoid powering motors with more than 12V without regulation.
* PWM affects DC motor speed — prefer consistent voltage if movement is jittery.
* Lightweight pen mount helps reduce z-axis load.

---

## 🤝 Contributing

Have ideas or want to help improve this project? Open a PR or raise an issue!

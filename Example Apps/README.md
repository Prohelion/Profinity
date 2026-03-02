# Profinity API Example Applications

This repository contains several example applications that demonstrate the integration capabilities of the Profinity API and how you can use these APIs to develop custom website, mobile applications or do data science using Profinity as your back end datasource.

1. **Battery Charging Station (Web Application)**
2. **Vehicle Dashboard (Mobile Application)**
3. **Matlab Data Science using Prohelion BMS (Matlab/Octave Example)**
4. **Python Data Science using Prohelion BMS (Python Example)**

All of these examples have been developed to use data from the supplied example PET Profile.  To get examples working load the PET Profile and reply the Example PET Can Log, putting the log in replay mode will keep the example CAN running.

## Battery Charging Station (Web Application)

A web application that demonstrates how to integrate Profinity APIs with Square's payment processing system to create a battery-powered charging station. The application monitors battery pack usage through Profinity's APIs and processes payments using Square's APIs for the consumed power.

![Battery Charging Station Screenshot](Charge%20for%20Power%20using%20Square%20(Web)/public/screen-shot.png)

### Key Features
- Real-time monitoring of battery pack status and power consumption
- Secure payment processing through Square
- User-friendly interface for both station operators and customers
- Detailed logging of power consumption and associated costs

[View detailed documentation](Charge%20for%20Power%20using%20Square%20(Web)/README.md)

## Vehicle Dashboard (Mobile Application)

A cross-platform mobile application built with React Native and Expo that demonstrates how to connect to and use Profinity APIs. The app provides real-time access to WaveSculptor and BMS information, offering a simple vehicle monitoring solution.

<table>
  <tr>
    <td width="50%">
      <img src="Vehicle%20Dashboard%20(Android%20&%20iOS%20Mobile%20App)/assets/login-screen-shot.png" alt="Login Screen" width="100%">
      <p align="center"><strong>Login Screen</strong></p>
    </td>
    <td width="50%">
      <img src="Vehicle%20Dashboard%20(Android%20&%20iOS%20Mobile%20App)/assets/dashboard-screen-shot.png" alt="Dashboard Screen" width="100%">
      <p align="center"><strong>Dashboard Screen</strong></p>
    </td>
  </tr>
</table>

### Key Features
- Cross-platform support (Android & iOS)
- Real-time vehicle data monitoring
- WaveSculptor and BMS information integration
- User authentication and secure access
- Modern, responsive user interface

[View detailed documentation](Vehicle%20Dashboard%20(Android%20%26%20iOS%20Mobile%20App)/README.md)

## Matlab Data Science using Prohelion BMS (Matlab/Octave Example)

A Matlab/Octave script that demonstrates how to authenticate with the Prohelion API, retrieve data from a Gen1 1000V BMS, and plot the cell voltages from each Cell Management Unit (CMU).

- Compatible with Matlab and GNU Octave
- Prompts for server URL, username, and password
- Plots cell voltages for each CMU

**Example Output:**

![Matlab Example Cell Voltage Plot](Matlab%20Data%20Science%20using%20Prohelion%20BMS/GraphExample.png)

## Requirements for Matlab Data Science using Prohelion BMS

- This example requires **GNU Octave 10.0 or later** for full compatibility with web APIs (such as webwrite and webread with JSON payloads).
- Older versions of Octave (prior to 10.0) may not work correctly with webwrite for JSON APIs due to limitations in HTTP and JSON support.
- If you encounter errors with webwrite or web API access, please upgrade your Octave installation to version 10 or later.

- MATLAB is also supported.

[View detailed documentation](Matlab%20Data%20Science%20using%20Prohelion%20BMS/README.md)

## Python Data Science using Prohelion BMS (Python Example)

A Python script that demonstrates how to authenticate with the Prohelion API, retrieve data from a Gen1 1000V BMS, and plot the cell voltages from each Cell Management Unit (CMU).

- Written in Python 3
- Uses requests and matplotlib
- Prompts for server URL, username, and password
- Plots cell voltages for each CMU

**Example Output:**

![Python Example Cell Voltage Plot](Python%20Data%20Science%20using%20Prohelion%20BMS/GraphExample.png)

[View detailed documentation](Python%20Data%20Science%20using%20Prohelion%20BMS/README.md)

## Getting Started

Each example application has its own detailed documentation and setup instructions. Please refer to the respective README files in each application's directory for specific setup and running instructions.

## Prerequisites

Common prerequisites for all applications:
- Profinity API access credentials
- A running Profinity instance
- Internet connection

Additional requirements for each application:

- **Battery Charging Station (Web):**
  - Node.js (v14 or later)
  - Yarn (recommended) or npm
  - Square API credentials

- **Vehicle Dashboard (Mobile):**
  - Node.js (v14 or later)
  - Yarn (recommended) or npm
  - Expo CLI
  - For iOS development: Xcode (Mac only)
  - For Android development: Android Studio

- **Matlab Data Science using Prohelion BMS:**
  - Matlab (R2018b or later) or GNU Octave (v10.0.0 or later)

- **Python Data Science using Prohelion BMS:**
  - Python 3.7 or later
  - pip (for installing dependencies)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Support

For support, please contact Prohelion Support via our website at [www.prohelion.com](https://www.prohelion.com) 

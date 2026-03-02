## Introduction to Profinity

Profinity V2 is a system management platform developed by Prohelion designed to be the most modern CAN bus management and development platform.

You can find the [Prohelion Documentation](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/index.html) on the docs site, or click to download the [latest Profinity release](https://github.com/Prohelion/Profinity/releases/latest/download/Profinity.install.msi) for Windows.

Profinity V2, completely updates the capabilities of Prohelion's Profinity suite by adding:

- Native run anywhere capabilities, use Profinity on your PC, Server, Embedded Device or run in the Cloud
- Fully web enabled user interface that runs on desktop, mobile or Kiosk.
- Full REST based API integration to allow easy extensions to Profinity's features and to build your own custom applications
- Inbuilt Scripting support
- Full ability to create custom dashboards, look and feel and add custom components
- Integration with AI and LLM tooling via MCP.

![Profinity](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/images/prohelion_bmu.png)

Profinity can connect to CAN Bus adapters, which translate CAN Bus traffic from your network to the PC, you can send and receive CAN Bus messages, log messages and replay them.

As well as providing extendable support for any CAN bus based solution, Profinity V2 provides specialised tools for managing [Prohelion Batteries](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Components/Battery_Management_Systems/index.html), MPPT systems from [Elmar Solar](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Components/MPPT/index.html) and [Prohelion WaveSculpters](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Components/Motor_Controller/index.html) as well as any device that can be defined by a CAN DBC file.  

## Download and Install

### Windows

| Installer | Documentation |
| --------- | ------------- |
| [Download Profinity V2 Installer](https://github.com/Prohelion/Profinity/releases/latest/download/Profinity.Install.msi) | [Windows Installation Documentation](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Installation/Windows_Installation.html) |

### Native Unix / macOS:

| Installer | Documentation |
| --------- | ------------- |
| [Download Profinity V2 Zip](https://github.com/Prohelion/Profinity/releases/latest/download/Profinity.zip) | [Native macOS / Unix Installation Documentation](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Installation/Zip_Installation.html) |

### Docker

| Documentation |
| ------------- |
| [Docker Installation Documentation](https://docs.prohelion.com/Profinity_Software/Profinity_Version_2/Installation/Docker_Installation.html) |

## Example Profinity Extensions

This repository includes example applications and example scripts to help you get started with Profinity V2.

### Example applications

The [Example Apps](Example%20Apps/README.md) directory contains sample applications that integrate with the Profinity API:

- **[Battery Charging Station](Example%20Apps/Charge%20for%20Power%20using%20Square%20(Web)/README.md)** (web) — Integrates Profinity with Square for a battery-powered charging station
- **[Artificial Intelligence Chat](Example%20Apps/Artificial%20Intelligence%20Chat%20(Web)/README.md)** (web, MCP) — Chat interface for querying Profinity via Ollama and the Model Context Protocol
- **[Vehicle Dashboard](Example%20Apps/Vehicle%20Dashboard%20(Android%20%26%20iOS%20Mobile%20App)/README.md)** (mobile) — Cross-platform app for real-time WaveSculptor and BMS data
- **Data science** — [Matlab](Example%20Apps/Matlab%20Data%20Science%20using%20Prohelion%20BMS/README.md) and [Python](Example%20Apps/Python%20Data%20Science%20using%20Prohelion%20BMS/README.md) examples for BMS data and cell voltage plotting

All of these use the supplied example PET Profile and CAN log for demo data.

### Example scripts

The [Example Scripts](Example%20Scripts/README.md) directory contains C# and Python scripts that run inside the Profinity scripting engine. They include:

- **Detailed examples** — Receive, Run, and Service templates with commented patterns for CAN, DBC, state, and cancellation
- **Simple examples** — Minimal scripts for one concept each (e.g. send CAN, read CAN, read DBC signal, script state, global state)

Use them to extend Profinity with custom logic or as a reference for the scripting API. See the [C#](Example%20Scripts/CSharp/README.md) and [Python](Example%20Scripts/Python/README.md) subdirectory READMEs for a full list.

## Documentation

Full documentation for Profinity V2 is available at:
[https://docs.prohelion.com/Profinity/Profinity_Version2/index.html](https://docs.prohelion.com/Profinity/Profinity_Version2/index.html)

## Support

- Visit our [Support Portal](https://support.prohelion.com/)
- [Contact Us](https://prohelion.com/contact/)
- Check our [FAQs](https://docs.prohelion.com/FAQs/index.html)

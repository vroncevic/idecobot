# idecobot: Robot IDE & Motion Studio for Elephant Robotics myCobot 280

<img align="right" src="https://raw.githubusercontent.com/vroncevic/idecobot/dev/docs/idecobot_logo.png" width="25%">

**idecobot** is a standalone robotics IDE, motion planning studio, DSL compiler, and real-time serial protocol streamer for Elephant Robotics myCobot 280 6-DOF robotic manipulators.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![idecobot python checker](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python_checker.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python_checker.yml) [![idecobot package checker](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_package_checker.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_package_checker.yml) [![idecobot interface checker](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_interface_checker.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_interface_checker.yml) [![idecobot isp checker](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_isp_checker.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_isp_checker.yml) [![idecobot srp checker](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_srp_checker.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/idecobot.svg)](https://github.com/vroncevic/idecobot/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/idecobot.svg)](https://github.com/vroncevic/idecobot/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
  - [✨ Features](#-features)
  - [📐 myCobot 280 Kinematic & Physical Robot Boundaries](#-mycobot-280-kinematic--physical-robot-boundaries)
  - [📜 myCobot Domain-Specific Language (DSL) & `.cobot` Programs](#-mycobot-domain-specific-language-dsl--cobot-programs)
    - [myCobot DSL Instruction Reference](#mycobot-dsl-instruction-reference)
    - [Example `.cobot` Program: Industrial Pick & Place](#example-cobot-program-industrial-pick--place)
  - [📡 Serial Communication Protocol](#-serial-communication-protocol)
    - [Packet Framing (PC $\leftrightarrow$ Robot)](#packet-framing-pc-%5Cleftrightarrow-robot)
    - [Protocol Command Set](#protocol-command-set)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Command Options](#cli-command-options)
    - [Interactive Robot Studio Workflow](#interactive-robot-studio-workflow)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/idecobot/dev/docs/debtux.png)

[![idecobot python3 build](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python3_build.yml/badge.svg)](https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**idecobot** is located at **[pypi.org](https://pypi.org/project/idecobot/)**.

You can install by using pip

```bash
# python3
pip3 install idecobot
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/idecobot/releases/)** download and extract release archive.

To install **idecobot** type the following

```bash
tar xvzf idecobot-x.y.z.tar.gz
cd idecobot-x.y.z/
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install ./dist/idecobot-*-py3-none-any.whl
rm -f get-pip.py
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/idecobot_run.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/idecobot_run.py /usr/local/bin/idecobot_run.py
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/idecobot/releases)** download and extract release archive.

To install **idecobot** locate and run setup.py with arguments

```bash
tar xvzf idecobot-x.y.z.tar.gz
cd idecobot-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**idecobot** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
* [pyserial - Python Serial Port Extension](https://pypi.org/project/pyserial/) [![License: BSD](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

### 📁 Tool structure

**idecobot** is based on OOP and Clean Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
    idecobot/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── communication/
         │   │   │   ├── __init__.py
         │   │   │   ├── mycobot_frame.py
         │   │   │   ├── protocol_constants.py
         │   │   │   ├── serial_defaults.py
         │   │   │   ├── stream_config.py
         │   │   │   ├── stream_progress.py
         │   │   │   └── stream_state.py
         │   │   ├── dsl/
         │   │   │   ├── ast/
         │   │   │   │   ├── imycobot_instruction.py
         │   │   │   │   ├── imycobot_program.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mycobot_command_type.py
         │   │   │   │   ├── mycobot_instruction.py
         │   │   │   │   └── mycobot_program.py
         │   │   │   ├── diagnostic/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── mycobot_diagnostic.py
         │   │   │   │   └── mycobot_diagnostic_severity.py
         │   │   │   ├── __init__.py
         │   │   │   └── token/
         │   │   │       ├── dsl_grammar_constants.py
         │   │   │       ├── __init__.py
         │   │   │       ├── mycobot_token.py
         │   │   │       └── mycobot_token_type.py
         │   │   ├── __init__.py
         │   │   └── kinematics/
         │   │       ├── __init__.py
         │   │       └── mycobot_bounds.py
         │   └── service/
         │       ├── communication/
         │       │   ├── imycobot_controller.py
         │       │   ├── imycobot_streamer.py
         │       │   ├── __init__.py
         │       │   └── itransport.py
         │       ├── dsl/
         │       │   ├── compiler/
         │       │   │   ├── imycobot_compiler.py
         │       │   │   ├── __init__.py
         │       │   │   └── mycobot_compiler.py
         │       │   ├── imycobot_dsl_service.py
         │       │   ├── __init__.py
         │       │   ├── lexer/
         │       │   │   ├── imycobot_lexer.py
         │       │   │   ├── __init__.py
         │       │   │   └── mycobot_lexer.py
         │       │   ├── linter/
         │       │   │   ├── imycobot_linter.py
         │       │   │   ├── __init__.py
         │       │   │   ├── mycobot_linter.py
         │       │   │   └── rules/
         │       │   │       ├── ground_safety_rule.py
         │       │   │       ├── imycobot_lint_rule.py
         │       │   │       ├── __init__.py
         │       │   │       ├── jerk_limit_rule.py
         │       │   │       ├── joint_bounds_rule.py
         │       │   │       ├── speed_limit_rule.py
         │       │   │       └── workspace_reach_rule.py
         │       │   ├── mycobot_dsl_service.py
         │       │   └── parser/
         │       │       ├── commands/
         │       │       │   ├── home_command_parser.py
         │       │       │   ├── icommand_parser.py
         │       │       │   ├── __init__.py
         │       │       │   ├── move_command_parser.py
         │       │       │   ├── power_command_parser.py
         │       │       │   ├── relax_command_parser.py
         │       │       │   ├── speed_command_parser.py
         │       │       │   ├── tool_command_parser.py
         │       │       │   └── wait_command_parser.py
         │       │       ├── imycobot_parser.py
         │       │       ├── __init__.py
         │       │       └── mycobot_parser.py
         │       ├── engine.py
         │       ├── __init__.py
         │       └── iservice.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── __init__.py
         │   │   ├── studio_command_definition.py
         │   │   └── studio_command_executor.py
         │   ├── communication/
         │   │   ├── __init__.py
         │   │   ├── iserial_port_scanner.py
         │   │   ├── protocol/
         │   │   │   ├── imycobot_protocol_codec.py
         │   │   │   ├── __init__.py
         │   │   │   └── mycobot_protocol_codec.py
         │   │   ├── serial_port_scanner.py
         │   │   ├── streamer/
         │   │   │   ├── __init__.py
         │   │   │   ├── mycobot_controller.py
         │   │   │   └── mycobot_streamer.py
         │   │   └── transport/
         │   │       ├── __init__.py
         │   │       ├── mock_serial_transport.py
         │   │       └── serial_transport.py
         │   ├── config/
         │   │   ├── idecobot.cfg
         │   │   ├── idecobot.logo
         │   │   ├── __init__.py
         │   │   ├── mycobot_geometry.json
         │   │   └── scheme.json
         │   ├── gui/
         │   │   ├── editor/
         │   │   │   ├── code_editor.py
         │   │   │   ├── editor_constants.py
         │   │   │   ├── editor_coordinator.py
         │   │   │   ├── editor_panel.py
         │   │   │   ├── editor_panel_factory.py
         │   │   │   ├── example_catalog.py
         │   │   │   ├── __init__.py
         │   │   │   └── syntax_highlighter.py
         │   │   ├── engine.py
         │   │   ├── engine_constants.py
         │   │   ├── igui.py
         │   │   ├── __init__.py
         │   │   ├── jog/
         │   │   │   ├── cartesian_constants.py
         │   │   │   ├── cartesian_panel.py
         │   │   │   ├── __init__.py
         │   │   │   ├── jog_constants.py
         │   │   │   ├── jog_coordinator.py
         │   │   │   ├── jog_panel.py
         │   │   │   ├── jog_panel_factory.py
         │   │   │   ├── joint_constants.py
         │   │   │   ├── joint_panel.py
         │   │   │   ├── step_constants.py
         │   │   │   ├── step_panel.py
         │   │   │   ├── tool_constants.py
         │   │   │   └── tool_panel.py
         │   │   ├── log/
         │   │   │   ├── bytecode_constants.py
         │   │   │   ├── bytecode_preview.py
         │   │   │   ├── console_constants.py
         │   │   │   ├── __init__.py
         │   │   │   ├── log_constants.py
         │   │   │   ├── log_panel.py
         │   │   │   ├── log_panel_factory.py
         │   │   │   └── serial_console.py
         │   │   ├── menu/
         │   │   │   ├── imenu_bar.py
         │   │   │   ├── __init__.py
         │   │   │   ├── menu_bar.py
         │   │   │   ├── menu_bar_constants.py
         │   │   │   └── menu_bar_factory.py
         │   │   ├── setup/
         │   │   │   ├── bundle.py
         │   │   │   ├── dep_validator.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── factory.py
         │   │   │   ├── gui_bundle_factory_constants.py
         │   │   │   ├── gui_event_handler.py
         │   │   │   ├── igui_event_handler.py
         │   │   │   ├── __init__.py
         │   │   │   ├── keys.py
         │   │   │   ├── opt_validator.py
         │   │   │   ├── options.py
         │   │   │   ├── registry.py
         │   │   │   └── validator.py
         │   │   ├── stream/
         │   │   │   ├── connection_constants.py
         │   │   │   ├── connection_panel.py
         │   │   │   ├── connection_panel_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── status_bar.py
         │   │   │   └── status_bar_constants.py
         │   │   ├── theme/
         │   │   │   ├── color_palette.py
         │   │   │   ├── font_config.py
         │   │   │   ├── __init__.py
         │   │   │   ├── theme.py
         │   │   │   └── theme_constants.py
         │   │   └── toolbar/
         │   │       ├── __init__.py
         │   │       ├── itoolbar.py
         │   │       ├── toolbar.py
         │   │       ├── toolbar_constants.py
         │   │       └── toolbar_factory.py
         │   ├── __init__.py
         │   └── storage/
         │       ├── __init__.py
         │       ├── iscript_storage_service.py
         │       ├── script_storage_service.py
         │       └── storage_constants.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     38 directories, 184 files
```
</details>

#### 🏗 Architecture & SOLID Principles

**idecobot** is built on a strictly decoupled, **Layered Clean Architecture** where presentation, domain logic, AST compilation, and hardware communication are segregated through pure Python structural protocols:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                       Engine                            │ (Presenter / Main Window)
                  └────────────────────────────┬────────────────────────────┘
                                               │ Orchestrates UI Panels & Coordinators via DI
         ┌─────────────────────────┬───────────┴─────────────┬──────────────────────────┐
         ▼                         ▼                         ▼                          ▼
┌──────────────────┐      ┌─────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│     JogPanel     │      │   EditorPanel   │      │     LogPanel      │      │ ConnectionPanel  │
│ (Joint/Cartesian/│      │ (CodeEditor,    │      │ (SerialConsole,   │      │ (Port Scanner &  │
│  Tool/Step)      │      │  Highlighter)   │      │  BytecodePreview) │      │  Baud Selector)  │
└────────┬─────────┘      └────────┬────────┘      └─────────┬─────────┘      └────────┬─────────┘
         │                         │                         │                         │
         └────────────┬────────────┴─────────────────────────┴─────────────────────────┘
                      │ Observes / Invokes Domain Services via Protocols
                      ▼
         ┌──────────────────────────┐
         │     MyCobotBounds        │ (Domain Model: Kinematics Limits & Physical Geometry)
         └────────────┬─────────────┘
                      │
         ┌────────────┴────────────┬────────────────────────┐
         ▼                         ▼                        ▼
┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐
│ KinematicsService│      │    DslService    │     │ ScriptStorage   │
│(Forward/Inverse) │      │(Lexer,Parser,Gen)│     │ (.cobot Storage)│
└──────────────────┘      └────────┬─────────┘     └─────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
     │    CobotLexer   │  │   CobotParser   │  │BytecodeGenerator│
     │  (Token Stream) │  │  (AST Builder)  │  │ (Binary Stream) │
     └─────────────────┘  └─────────────────┘  └─────────────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │ SerialTransport  │ (0xFE 0xFE Framing)
                                               └──────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Every module and class has exactly one clearly bounded reason to change.
  * GUI sub-panels, coordinators, parser, compiler, and storage handlers are segregated into dedicated, focused files.
  * Enforced by automated gate: strict limit of $\le 15$ methods per class across the entire codebase.
* **O — Open/Closed Principle (OCP)**:
  * The DSL parser, compiler, and command executors are open for extension without modifying existing code.
  * New DSL keywords, kinematic transforms, and protocol commands plug in dynamically.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python `@runtime_checkable Protocol` definitions. Concrete classes never inherit from interfaces, ensuring zero circular dependencies and complete interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  * Clients depend only on the minimal interfaces they require (`IKinematicsService`, `IDslService`, `IScriptStorageService`, `ISerialTransport`, `IAppMenuBar`, `IControlsPanel`).
* **D — Dependency Inversion Principle (DIP)**:
  * Core domain entities, services, and presenters depend strictly on abstractions (Protocols), not concrete classes. All dependencies are injected via `setup/factory.py`.

##### Automated Quality Gates (`run_quality_gates.sh`)

Every build is validated against 4 strict automated quality gates:
1. **Structural Protocols Gate**: Verifies 100% compliance with `@runtime_checkable Protocol` structural typing.
2. **Interface Segregation Gate (ISP)**: Verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate**: Enforces file length and line length limits ($\le 100$ characters).
4. **Single Responsibility Gate (SRP)**: Strictly enforces $\le 15$ methods per class.

#### ✨ Features

* **Interactive 6-DOF Robot Studio**: Dedicated Joint jog sliders (J1–J6) with real-time degree readouts, Cartesian translation (X, Y, Z, Rx, Ry, Rz), end-effector tool gripper control (Grip / Release / Angle), and variable step increments (1.0, 5.0, 10.0, 50.0 mm/deg).
* **Integrated `.cobot` DSL Editor & Compiler**: Full-featured code editor with real-time syntax highlighting for industrial myCobot scripts (`.cobot`), AST compilation, and instant bidirectional visual status synchronization.
* **Kinematic Reachability & Boundary Enforcement**: Spherical workspace boundary validation ensuring joint angles remain within physical limits (J1–J5: $\pm 165^\circ$, J6: $\pm 175^\circ$) and arm reach does not exceed $285\text{ mm}$.
* **Binary Bytecode Disassembly & Inspection**: Live bytecode preview panel displaying compiled hex and instruction mnemonic streams before physical transmission to the robot.
* **Packetized Serial Communication**: Multi-threaded USB serial transport implementing Elephant Robotics binary framing protocol (`0xFE 0xFE <len> <cmd> <payload...> 0xFA`) with baudrate selection (115200 default) and auto-detection.
* **Manual Jogging & Diagnostics**: Real-time jog execution, servo torque enable/release (Power/Relax), synchronous wait, homing, and live serial console log.
* **Pure Clean Architecture & Dependency Injection**: 100% structural protocol decoupling, zero ISP/SRP violations, granular imports, and comprehensive test coverage.

#### 📐 myCobot 280 Kinematic & Physical Robot Boundaries

The robot kinematic parameters and physical limits are encapsulated within `MyCobotBounds`:

| Parameter | Limit Value | Description |
|---|:---:|---|
| **`j1_min` / `j1_max`** | `-165.0°` / `+165.0°` | Base rotation joint limit. |
| **`j2_min` / `j2_max`** | `-165.0°` / `+165.0°` | Shoulder elevation joint limit. |
| **`j3_min` / `j3_max`** | `-165.0°` / `+165.0°` | Elbow joint limit. |
| **`j4_min` / `j4_max`** | `-165.0°` / `+165.0°` | Wrist pitch joint limit. |
| **`j5_min` / `j5_max`** | `-165.0°` / `+165.0°` | Wrist roll joint limit. |
| **`j6_min` / `j6_max`** | `-175.0°` / `+175.0°` | Tool rotation joint limit. |
| **`reach_max`** | `285.0 mm` | Maximum spherical reach from robot base origin. |
| **`min_speed` / `max_speed`**| `1%` / `100%` | Allowable joint and Cartesian travel velocity range. |

#### 📜 myCobot Domain-Specific Language (DSL) & `.cobot` Programs

**idecobot** includes a dedicated Domain-Specific Language designed specifically for 6-DOF myCobot manipulators. Programs are written in plain text files with the `.cobot` extension and compiled into validated binary machine instructions via a clean AST pipeline:

```
                    ┌─────────────────────────┐
                    │      .cobot Source      │
                    └────────────┬────────────┘
                                 │ CobotLexer
                                 ▼
                    ┌─────────────────────────┐
                    │      Token Stream       │
                    └────────────┬────────────┘
                                 │ CobotParser
                                 ▼
                    ┌─────────────────────────┐
                    │      Abstract AST       │
                    └────────────┬────────────┘
                                 │ CobotCompiler & BytecodeGenerator
                                 ▼
                    ┌─────────────────────────┐
                    │     Bytecode Stream     │ (0xFE 0xFE Binary Packets)
                    └─────────────────────────┘
```

##### myCobot DSL Instruction Reference

| Category | Instruction & Syntax | Parameters | Description |
|---|---|---|---|
| **Power & State** | `HOME` | None | Moves all 6 joints to calibrated zero reference position ($0.0^\circ$). |
| | `RELAX` | None | Releases servo brakes / disables motor torque for manual teaching. |
| | `POWER` | None | Energizes servo motors and enables active position control. |
| **Timing & Speed** | `SPEED <percent>` | `percent` (1% - 100%) | Sets travel feedrate velocity percentage. |
| | `WAIT <ms>` | `ms` (milliseconds) | Dwells execution for specified hardware duration. |
| **Tool Actuation** | `TOOL GRIP` | None | Closes electric gripper end-effector. |
| | `TOOL RELEASE` | None | Opens electric gripper end-effector. |
| | `TOOL ANGLE <deg>` | `deg` (0° - 100°) | Sets electric gripper opening angle. |
| **Motion** | `MOVE J1 <j1> J2 <j2> J3 <j3> J4 <j4> J5 <j5> J6 <j6> [SPEED <s>]` | `J1..J6` (deg), `SPEED` (%) | Coordinated 6-DOF multi-joint motion. |
| | `MOVE_L X <x> Y <y> Z <z> RX <rx> RY <ry> RZ <rz> [SPEED <s>]` | `X,Y,Z` (mm), `RX,RY,RZ` (deg) | Cartesian linear tool interpolated path. |

##### Example `.cobot` Program: Industrial Pick & Place

```cobot
# ----------------------------------------------------
# Elephant Robotics myCobot 280 Pick-and-Place Cycle
# ----------------------------------------------------
POWER
SPEED 40
HOME
WAIT 500

# Approach workpiece pick station
MOVE J1 0.0 J2 20.0 J3 -45.0 J4 0.0 J5 30.0 J6 0.0 SPEED 50
MOVE_L X 180.0 Y -50.0 Z 120.0 RX 0.0 RY 90.0 RZ 0.0 SPEED 30

# Grip object and wait for mechanical engagement
TOOL GRIP
WAIT 300

# Retract and transfer to drop location
MOVE_L X 180.0 Y -50.0 Z 200.0 RX 0.0 RY 90.0 RZ 0.0 SPEED 30
MOVE J1 90.0 J2 15.0 J3 -30.0 J4 0.0 J5 20.0 J6 45.0 SPEED 40
MOVE_L X 0.0 Y 180.0 Z 100.0 RX 0.0 RY 90.0 RZ 45.0 SPEED 20

# Release object
TOOL RELEASE
WAIT 300

# Return to safe home altitude
HOME
```

#### 📡 Serial Communication Protocol

All communication between **idecobot** and the physical **myCobot 280** microcontroller is governed by the standard binary framing protocol:

##### Packet Framing (PC $\leftrightarrow$ Robot)

```
┌──────┬──────┬─────────┬─────────┬─────────────────┬──────┐
│ 0xFE │ 0xFE │ LEN (N) │ CMD_ID  │ PAYLOAD (N - 2) │ 0xFA │
└──────┴──────┴─────────┴─────────┴─────────────────┴──────┘
  Header 2B     Length    Command        Data bytes     Tail
```

##### Protocol Command Set

| Command ID | Command Name | Description |
|:---:|---|---|
| `0x10` | `POWER_ON` | Powers on and activates all servo motors. |
| `0x11` | `POWER_OFF` | Powers off all servo motors. |
| `0x13` | `RELEASE_ALL_SERVOS` | Disables torque holding for manual positioning. |
| `0x20` | `WRITE_ANGLES` | Sends target joint angles ($J_1 \dots J_6$) with speed. |
| `0x21` | `READ_ANGLES` | Queries active joint angles from robot controllers. |
| `0x22` | `WRITE_COORDS` | Sends target Cartesian coordinates ($X, Y, Z, Rx, Ry, Rz$) with speed. |
| `0x23` | `READ_COORDS` | Queries active Cartesian pose from robot controllers. |
| `0x80` | `SET_GRIPPER_STATE` | Opens or closes electric gripper end-effector. |

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `idecobot/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/communication/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/communication/mycobot_frame.py` | 22 | 1 | 95%|
| `idecobot/core/model/communication/protocol_constants.py` | 39 | 0 | 100%|
| `idecobot/core/model/communication/serial_defaults.py` | 19 | 0 | 100%|
| `idecobot/core/model/communication/stream_config.py` | 17 | 0 | 100%|
| `idecobot/core/model/communication/stream_progress.py` | 18 | 0 | 100%|
| `idecobot/core/model/communication/stream_state.py` | 17 | 0 | 100%|
| `idecobot/core/model/dsl/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/dsl/ast/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/dsl/ast/imycobot_instruction.py` | 22 | 22 | 0%|
| `idecobot/core/model/dsl/ast/imycobot_program.py` | 20 | 20 | 0%|
| `idecobot/core/model/dsl/ast/mycobot_command_type.py` | 19 | 0 | 100%|
| `idecobot/core/model/dsl/ast/mycobot_instruction.py` | 18 | 0 | 100%|
| `idecobot/core/model/dsl/ast/mycobot_program.py` | 21 | 2 | 90%|
| `idecobot/core/model/dsl/diagnostic/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/dsl/diagnostic/mycobot_diagnostic.py` | 23 | 2 | 91%|
| `idecobot/core/model/dsl/diagnostic/mycobot_diagnostic_severity.py` | 14 | 0 | 100%|
| `idecobot/core/model/dsl/token/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/dsl/token/dsl_grammar_constants.py` | 32 | 0 | 100%|
| `idecobot/core/model/dsl/token/mycobot_token.py` | 17 | 0 | 100%|
| `idecobot/core/model/dsl/token/mycobot_token_type.py` | 18 | 0 | 100%|
| `idecobot/core/model/kinematics/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/model/kinematics/mycobot_bounds.py` | 53 | 0 | 100%|
| `idecobot/core/service/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/communication/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/communication/imycobot_controller.py` | 22 | 0 | 100%|
| `idecobot/core/service/communication/imycobot_streamer.py` | 23 | 0 | 100%|
| `idecobot/core/service/communication/itransport.py` | 18 | 0 | 100%|
| `idecobot/core/service/dsl/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/compiler/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/compiler/imycobot_compiler.py` | 18 | 0 | 100%|
| `idecobot/core/service/dsl/compiler/mycobot_compiler.py` | 84 | 14 | 83%|
| `idecobot/core/service/dsl/imycobot_dsl_service.py` | 22 | 0 | 100%|
| `idecobot/core/service/dsl/lexer/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/lexer/imycobot_lexer.py` | 16 | 0 | 100%|
| `idecobot/core/service/dsl/lexer/mycobot_lexer.py` | 78 | 24 | 69%|
| `idecobot/core/service/dsl/linter/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/linter/imycobot_linter.py` | 17 | 0 | 100%|
| `idecobot/core/service/dsl/linter/mycobot_linter.py` | 26 | 1 | 96%|
| `idecobot/core/service/dsl/linter/rules/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/linter/rules/ground_safety_rule.py` | 34 | 5 | 85%|
| `idecobot/core/service/dsl/linter/rules/imycobot_lint_rule.py` | 17 | 0 | 100%|
| `idecobot/core/service/dsl/linter/rules/jerk_limit_rule.py` | 42 | 2 | 95%|
| `idecobot/core/service/dsl/linter/rules/joint_bounds_rule.py` | 36 | 1 | 97%|
| `idecobot/core/service/dsl/linter/rules/speed_limit_rule.py` | 36 | 5 | 86%|
| `idecobot/core/service/dsl/linter/rules/workspace_reach_rule.py` | 37 | 7 | 81%|
| `idecobot/core/service/dsl/mycobot_dsl_service.py` | 47 | 3 | 94%|
| `idecobot/core/service/dsl/parser/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/parser/commands/__init__.py` | 9 | 0 | 100%|
| `idecobot/core/service/dsl/parser/commands/home_command_parser.py` | 21 | 0 | 100%|
| `idecobot/core/service/dsl/parser/commands/icommand_parser.py` | 17 | 0 | 100%|
| `idecobot/core/service/dsl/parser/commands/move_command_parser.py` | 55 | 6 | 89%|
| `idecobot/core/service/dsl/parser/commands/power_command_parser.py` | 21 | 2 | 90%|
| `idecobot/core/service/dsl/parser/commands/relax_command_parser.py` | 21 | 0 | 100%|
| `idecobot/core/service/dsl/parser/commands/speed_command_parser.py` | 25 | 1 | 96%|
| `idecobot/core/service/dsl/parser/commands/tool_command_parser.py` | 37 | 6 | 84%|
| `idecobot/core/service/dsl/parser/commands/wait_command_parser.py` | 25 | 1 | 96%|
| `idecobot/core/service/dsl/parser/imycobot_parser.py` | 18 | 0 | 100%|
| `idecobot/core/service/dsl/parser/mycobot_parser.py` | 51 | 3 | 94%|
| `idecobot/core/service/engine.py` | 34 | 1 | 97%|
| `idecobot/core/service/iservice.py` | 21 | 0 | 100%|
| `idecobot/engine.py` | 60 | 60 | 0%|
| `idecobot/infrastructure/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/cli/engine.py` | 39 | 7 | 82%|
| `idecobot/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `idecobot/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/cli/setup/bundle.py` | 22 | 1 | 95%|
| `idecobot/infrastructure/cli/setup/dep_validator.py` | 36 | 5 | 86%|
| `idecobot/infrastructure/cli/setup/dependencies.py` | 18 | 0 | 100%|
| `idecobot/infrastructure/cli/setup/factory.py` | 37 | 1 | 97%|
| `idecobot/infrastructure/cli/setup/keys.py` | 28 | 0 | 100%|
| `idecobot/infrastructure/cli/setup/opt_validator.py` | 36 | 5 | 86%|
| `idecobot/infrastructure/cli/setup/options.py` | 17 | 0 | 100%|
| `idecobot/infrastructure/cli/setup/registry.py` | 24 | 1 | 96%|
| `idecobot/infrastructure/cli/setup/validator.py` | 43 | 5 | 88%|
| `idecobot/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/command/command.py` | 16 | 0 | 100%|
| `idecobot/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `idecobot/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `idecobot/infrastructure/command/studio_command_definition.py` | 29 | 1 | 97%|
| `idecobot/infrastructure/command/studio_command_executor.py` | 41 | 15 | 63%|
| `idecobot/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/communication/iserial_port_scanner.py` | 15 | 0 | 100%|
| `idecobot/infrastructure/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/communication/protocol/imycobot_protocol_codec.py` | 22 | 0 | 100%|
| `idecobot/infrastructure/communication/protocol/mycobot_protocol_codec.py` | 50 | 5 | 90%|
| `idecobot/infrastructure/communication/serial_port_scanner.py` | 18 | 1 | 94%|
| `idecobot/infrastructure/communication/streamer/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/communication/streamer/mycobot_controller.py` | 66 | 16 | 76%|
| `idecobot/infrastructure/communication/streamer/mycobot_streamer.py` | 71 | 36 | 49%|
| `idecobot/infrastructure/communication/transport/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/communication/transport/mock_serial_transport.py` | 59 | 4 | 93%|
| `idecobot/infrastructure/communication/transport/serial_transport.py` | 57 | 25 | 56%|
| `idecobot/infrastructure/config/__init__.py` | 9 | 9 | 0%|
| `idecobot/infrastructure/gui/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/editor/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/editor/code_editor.py` | 55 | 4 | 93%|
| `idecobot/infrastructure/gui/editor/editor_constants.py` | 54 | 0 | 100%|
| `idecobot/infrastructure/gui/editor/editor_coordinator.py` | 62 | 2 | 97%|
| `idecobot/infrastructure/gui/editor/editor_panel.py` | 69 | 22 | 68%|
| `idecobot/infrastructure/gui/editor/editor_panel_factory.py` | 52 | 0 | 100%|
| `idecobot/infrastructure/gui/editor/example_catalog.py` | 18 | 0 | 100%|
| `idecobot/infrastructure/gui/editor/syntax_highlighter.py` | 48 | 0 | 100%|
| `idecobot/infrastructure/gui/engine.py` | 89 | 36 | 60%|
| `idecobot/infrastructure/gui/engine_constants.py` | 24 | 0 | 100%|
| `idecobot/infrastructure/gui/igui.py` | 17 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/cartesian_constants.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/cartesian_panel.py` | 54 | 6 | 89%|
| `idecobot/infrastructure/gui/jog/jog_constants.py` | 58 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/jog_coordinator.py` | 91 | 7 | 92%|
| `idecobot/infrastructure/gui/jog/jog_panel.py` | 50 | 9 | 82%|
| `idecobot/infrastructure/gui/jog/jog_panel_factory.py` | 59 | 18 | 69%|
| `idecobot/infrastructure/gui/jog/joint_constants.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/joint_panel.py` | 53 | 6 | 89%|
| `idecobot/infrastructure/gui/jog/step_constants.py` | 30 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/step_panel.py` | 52 | 11 | 79%|
| `idecobot/infrastructure/gui/jog/tool_constants.py` | 38 | 0 | 100%|
| `idecobot/infrastructure/gui/jog/tool_panel.py` | 53 | 3 | 94%|
| `idecobot/infrastructure/gui/log/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/log/bytecode_constants.py` | 23 | 0 | 100%|
| `idecobot/infrastructure/gui/log/bytecode_preview.py` | 55 | 11 | 80%|
| `idecobot/infrastructure/gui/log/console_constants.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/log/log_constants.py` | 17 | 0 | 100%|
| `idecobot/infrastructure/gui/log/log_panel.py` | 50 | 7 | 86%|
| `idecobot/infrastructure/gui/log/log_panel_factory.py` | 32 | 0 | 100%|
| `idecobot/infrastructure/gui/log/serial_console.py` | 62 | 9 | 85%|
| `idecobot/infrastructure/gui/menu/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/menu/imenu_bar.py` | 17 | 17 | 0%|
| `idecobot/infrastructure/gui/menu/menu_bar.py` | 56 | 13 | 77%|
| `idecobot/infrastructure/gui/menu/menu_bar_constants.py` | 32 | 0 | 100%|
| `idecobot/infrastructure/gui/menu/menu_bar_factory.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/bundle.py` | 37 | 1 | 97%|
| `idecobot/infrastructure/gui/setup/dep_validator.py` | 36 | 5 | 86%|
| `idecobot/infrastructure/gui/setup/dependencies.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/factory.py` | 103 | 7 | 93%|
| `idecobot/infrastructure/gui/setup/gui_bundle_factory_constants.py` | 23 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/gui_event_handler.py` | 39 | 4 | 90%|
| `idecobot/infrastructure/gui/setup/igui_event_handler.py` | 21 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/keys.py` | 43 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/opt_validator.py` | 36 | 5 | 86%|
| `idecobot/infrastructure/gui/setup/options.py` | 17 | 0 | 100%|
| `idecobot/infrastructure/gui/setup/registry.py` | 24 | 1 | 96%|
| `idecobot/infrastructure/gui/setup/validator.py` | 61 | 5 | 92%|
| `idecobot/infrastructure/gui/stream/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/stream/connection_constants.py` | 42 | 0 | 100%|
| `idecobot/infrastructure/gui/stream/connection_panel.py` | 85 | 2 | 98%|
| `idecobot/infrastructure/gui/stream/connection_panel_factory.py` | 44 | 0 | 100%|
| `idecobot/infrastructure/gui/stream/status_bar.py` | 71 | 24 | 66%|
| `idecobot/infrastructure/gui/stream/status_bar_constants.py` | 33 | 0 | 100%|
| `idecobot/infrastructure/gui/theme/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/theme/color_palette.py` | 34 | 0 | 100%|
| `idecobot/infrastructure/gui/theme/font_config.py` | 21 | 0 | 100%|
| `idecobot/infrastructure/gui/theme/theme.py` | 47 | 0 | 100%|
| `idecobot/infrastructure/gui/theme/theme_constants.py` | 38 | 0 | 100%|
| `idecobot/infrastructure/gui/toolbar/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/gui/toolbar/itoolbar.py` | 15 | 15 | 0%|
| `idecobot/infrastructure/gui/toolbar/toolbar.py` | 58 | 0 | 100%|
| `idecobot/infrastructure/gui/toolbar/toolbar_constants.py` | 28 | 0 | 100%|
| `idecobot/infrastructure/gui/toolbar/toolbar_factory.py` | 37 | 0 | 100%|
| `idecobot/infrastructure/storage/__init__.py` | 9 | 0 | 100%|
| `idecobot/infrastructure/storage/iscript_storage_service.py` | 15 | 0 | 100%|
| `idecobot/infrastructure/storage/script_storage_service.py` | 38 | 5 | 87%|
| `idecobot/infrastructure/storage/storage_constants.py` | 19 | 0 | 100%|
| `idecobot/setup/__init__.py` | 9 | 0 | 100%|
| `idecobot/setup/bundle.py` | 25 | 0 | 100%|
| `idecobot/setup/dep_validator.py` | 36 | 5 | 86%|
| `idecobot/setup/dependencies.py` | 21 | 0 | 100%|
| `idecobot/setup/factory.py` | 116 | 5 | 96%|
| `idecobot/setup/keys.py` | 33 | 1 | 97%|
| `idecobot/setup/opt_validator.py` | 36 | 16 | 56%|
| `idecobot/setup/options.py` | 16 | 0 | 100%|
| `idecobot/setup/registry.py` | 34 | 1 | 97%|
| `idecobot/setup/validator.py` | 53 | 5 | 91%|
| **Total** | 5467 | 614 | 89% |

</details>

### 🛠 Usage

Install package

```bash
pip3 install idecobot
```

Prepare main entry point by downloading [main.py](https://raw.githubusercontent.com/vroncevic/idecobot/main/main.py) or create your own.

```bash
wget -O main.py https://raw.githubusercontent.com/vroncevic/idecobot/main/main.py
```

##### CLI Command Options

Launch the graphical studio with default configuration:

```bash
python3 main.py studio
```

Launch with initial script file and pre-selected serial port:

```bash
python3 main.py studio --file ./scripts/pick_and_place.cobot --port /dev/ttyACM0 --verbose enable
```

| Option | Type | Choices | Description |
|---|:---:|:---:|---|
| **`--file`** | `str` | *File path* | Path to initial `.cobot` DSL script file to load on startup. |
| **`--port`** | `str` | *Serial port* | Serial communication port (e.g. `/dev/ttyACM0` or `COM3`). |
| **`--verbose`** | `str` | `enable`, `disable` | Enable or disable verbose ATS operational logging. |

##### Interactive Robot Studio Workflow

1. **Hardware Connection**:
   * Under the **Connection Panel**, select the detected serial port (e.g., `/dev/ttyACM0`) or mock transport for offline testing.
   * Click **Connect**. The status bar updates to green `Connected`.
2. **Manual Jogging**:
   * Navigate through **Joint**, **Cartesian**, **Tool**, and **Step** sub-panels.
   * Jog individual joints ($J_1 \dots J_6$) or Cartesian axes ($X, Y, Z, Rx, Ry, Rz$) with instant degree readouts.
   * Toggle servo torque (`Power` / `Relax`) and control gripper state (`Grip` / `Release`).
3. **DSL Scripting & Compilation**:
   * Open the **Script Editor** tab to author `.cobot` automation scripts.
   * Load bundled industrial templates from the Example Catalog.
   * Click **Compile** to validate syntax and inspect generated bytecode in the Bytecode Preview panel.
4. **Execution & Monitoring**:
   * Stream compiled instructions directly to the physical robot.
   * Observe live serial communication traffic and acknowledgments in the Serial Console.

### 📚 Docs

More documentation and info at

* `idecobot.readthedocs.io <https://idecobot.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

### 👥 Contributing

[Contributing to idecobot](https://github.com/vroncevic/idecobot/blob/dev/CONTRIBUTING.md)

### 📄 Copyright and licence

Copyright (C) 2026 by [vroncevic.github.io/idecobot](https://vroncevic.github.io/idecobot)

**idecobot** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/idecobot/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)

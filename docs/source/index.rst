Robot IDE & Motion Studio for Elephant Robotics myCobot 280
===========================================================

**idecobot** is a standalone robotics IDE, motion planning studio, DSL compiler, and real-time serial protocol streamer for Elephant Robotics myCobot 280 6-DOF robotic manipulators.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|idecobot python checker| |idecobot python package| |idecobot interface checker| |idecobot isp checker| |idecobot srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |idecobot python checker| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python_checker.yml

.. |idecobot python package| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_package_checker.yml

.. |idecobot interface checker| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_interface_checker.yml

.. |idecobot isp checker| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_isp_checker.yml

.. |idecobot srp checker| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/idecobot.svg
   :target: https://github.com/vroncevic/idecobot/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/idecobot.svg
   :target: https://github.com/vroncevic/idecobot/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/idecobot/badge/?version=latest
   :target: https://idecobot.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
---------------

|idecobot python3 build|

.. |idecobot python3 build| image:: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/idecobot/actions/workflows/idecobot_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/idecobot/releases

To install **idecobot** type the following

.. code-block:: bash

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

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install idecobot

📦 Dependencies
---------------

**idecobot** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|
* `pyserial - Python Serial Port Extension <https://pypi.org/project/pyserial/>`_ |pyserial bsd|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |pyserial bsd| image:: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause

📁 Tool structure
-----------------

**idecobot** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

    idecobot/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── communication/
         │   │   │   ├── __init__.py
         │   │   │   ├── mycobot_frame.py
         │   │   │   ├── protocol_constants.py
         │   │   │   ├── stream_config.py
         │   │   │   ├── stream_progress.py
         │   │   │   └── stream_state.py
         │   │   ├── dsl/
         │   │   │   ├── ast/
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
         │   │       ├── joint_bounds.py
         │   │       ├── joint_limit.py
         │   │       ├── mycobot_bounds.py
         │   │       ├── spatial_bounds.py
         │   │       ├── speed_bounds.py
         │   │       └── trajectory_bounds.py
         │   └── service/
         │       ├── communication/
         │       │   ├── imycobot_controller.py
         │       │   ├── imycobot_streamer.py
         │       │   ├── __init__.py
         │       │   └── itransport.py
         │       ├── dsl/
         │       │   ├── compiler/
         │       │   │   ├── commands/
         │       │   │   │   ├── home_command_compiler.py
         │       │   │   │   ├── icommand_compiler.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── move_coords_command_compiler.py
         │       │   │   │   ├── move_joints_command_compiler.py
         │       │   │   │   ├── power_command_compiler.py
         │       │   │   │   ├── relax_command_compiler.py
         │       │   │   │   ├── speed_command_compiler.py
         │       │   │   │   ├── tool_command_compiler.py
         │       │   │   │   └── wait_command_compiler.py
         │       │   │   ├── compiler_context.py
         │       │   │   ├── imycobot_compiler.py
         │       │   │   ├── __init__.py
         │       │   │   └── mycobot_compiler.py
         │       │   ├── dsl_service_factory.py
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
         │       ├── iservice.py
         │       └── kinematics/
         │           ├── ikinematic_validator.py
         │           ├── __init__.py
         │           └── kinematic_validator.py
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
         │   │   │   ├── imotion_codec.py
         │   │   │   ├── imycobot_protocol_codec.py
         │   │   │   ├── __init__.py
         │   │   │   ├── iprotocol_codec_factory.py
         │   │   │   ├── iprotocol_framer.py
         │   │   │   ├── isystem_codec.py
         │   │   │   ├── itool_codec.py
         │   │   │   ├── motion_codec.py
         │   │   │   ├── mycobot_protocol_codec.py
         │   │   │   ├── protocol_codec_factory.py
         │   │   │   ├── protocol_framer.py
         │   │   │   ├── system_codec.py
         │   │   │   └── tool_codec.py
         │   │   ├── serial_port_scanner.py
         │   │   ├── streamer/
         │   │   │   ├── connection_manager.py
         │   │   │   ├── controller_factory.py
         │   │   │   ├── iconnection_manager.py
         │   │   │   ├── icontroller_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── irobot_actuator.py
         │   │   │   ├── irobot_telemetry.py
         │   │   │   ├── istreamer_factory.py
         │   │   │   ├── mycobot_controller.py
         │   │   │   ├── mycobot_streamer.py
         │   │   │   ├── robot_actuator.py
         │   │   │   ├── robot_telemetry.py
         │   │   │   └── streamer_factory.py
         │   │   └── transport/
         │   │       ├── __init__.py
         │   │       ├── mock_serial_transport.py
         │   │       ├── serial_transport.py
         │   │       └── transport_constants.py
         │   ├── config/
         │   │   ├── examples.tgz
         │   │   ├── idecobot.cfg
         │   │   ├── idecobot.logo
         │   │   ├── mycobot_geometry.json
         │   │   └── scheme.json
         │   ├── diagnostics/
         │   │   ├── diagnostics_constants.py
         │   │   ├── diagnostics_coordinator.py
         │   │   ├── diagnostics_factory.py
         │   │   ├── idiagnostics_coordinator.py
         │   │   ├── ijoint_diagnostics_reader.py
         │   │   ├── __init__.py
         │   │   ├── iservo_diagnostics_reader.py
         │   │   ├── ispatial_diagnostics_reader.py
         │   │   ├── joint_diagnostics_reader.py
         │   │   ├── servo_diagnostics_reader.py
         │   │   └── spatial_diagnostics_reader.py
         │   ├── gui/
         │   │   ├── editor/
         │   │   │   ├── code_editor.py
         │   │   │   ├── editor_constants.py
         │   │   │   ├── editor_coordinator.py
         │   │   │   ├── editor_panel.py
         │   │   │   ├── editor_panel_factory.py
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
         │   │   │   ├── diagnostics_menu_handler.py
         │   │   │   ├── file_menu_handler.py
         │   │   │   ├── help_menu_handler.py
         │   │   │   ├── idiagnostics_menu_handler.py
         │   │   │   ├── ifile_menu_handler.py
         │   │   │   ├── ihelp_menu_handler.py
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
         │   │   │   ├── igui_event_target.py
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
         │       ├── iworkspace_service.py
         │       ├── script_storage_service.py
         │       ├── storage_constants.py
         │       ├── workspace_constants.py
         │       └── workspace_service.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bounds_loader.py
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── gui_factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     41 directories, 244 files

✨ Features
-----------

* **Interactive 6-DOF Robot Studio**: Dedicated Joint jog sliders (J1–J6) with real-time degree readouts, Cartesian translation (X, Y, Z, Rx, Ry, Rz), end-effector tool gripper control (Grip / Release / Angle), and variable step increments (1.0, 5.0, 10.0, 50.0 mm/deg).
* **Integrated .cobot DSL Editor & Compiler**: Full-featured code editor with real-time syntax highlighting for industrial myCobot scripts (``.cobot``), AST compilation, and instant bidirectional visual status synchronization.
* **Kinematic Reachability & Boundary Enforcement**: Spherical workspace boundary validation ensuring joint angles remain within physical limits (J1–J5: :math:`\pm 165^\circ`, J6: :math:`\pm 175^\circ`) and arm reach does not exceed :math:`285\text{ mm}`.
* **Binary Bytecode Disassembly & Inspection**: Live bytecode preview panel displaying compiled hex and instruction mnemonic streams before physical transmission to the robot.
* **Packetized Serial Communication**: Multi-threaded USB serial transport implementing Elephant Robotics binary framing protocol (``0xFE 0xFE <len> <cmd> <payload...> 0xFA``) with baudrate selection (115200 default) and auto-detection.
* **Manual Jogging & Diagnostics**: Real-time jog execution, servo torque enable/release (Power/Relax), synchronous wait, homing, and live serial console log.
* **Pure Clean Architecture & Dependency Injection**: 100% structural protocol decoupling, zero ISP/SRP violations, granular imports, and comprehensive test coverage.

📐 myCobot 280 Kinematic & Physical Robot Boundaries
----------------------------------------------------

The robot kinematic parameters and physical limits are encapsulated within ``MyCobotBounds``:

.. list-table:: Kinematic Limits
   :widths: 25 25 50
   :header-rows: 1

   * - Parameter
     - Limit Value
     - Description
   * - **j1_min / j1_max**
     - :math:`-165.0^\circ` / :math:`+165.0^\circ`
     - Base rotation joint limit.
   * - **j2_min / j2_max**
     - :math:`-165.0^\circ` / :math:`+165.0^\circ`
     - Shoulder elevation joint limit.
   * - **j3_min / j3_max**
     - :math:`-165.0^\circ` / :math:`+165.0^\circ`
     - Elbow joint limit.
   * - **j4_min / j4_max**
     - :math:`-165.0^\circ` / :math:`+165.0^\circ`
     - Wrist pitch joint limit.
   * - **j5_min / j5_max**
     - :math:`-165.0^\circ` / :math:`+165.0^\circ`
     - Wrist roll joint limit.
   * - **j6_min / j6_max**
     - :math:`-175.0^\circ` / :math:`+175.0^\circ`
     - Tool rotation joint limit.
   * - **reach_max**
     - :math:`285.0\text{ mm}`
     - Maximum spherical reach from robot base origin.
   * - **min_speed / max_speed**
     - :math:`1\%` / :math:`100\%`
     - Allowable joint and Cartesian travel velocity range.

📜 myCobot Domain-Specific Language (DSL) & .cobot Programs
-----------------------------------------------------------

**idecobot** includes a dedicated Domain-Specific Language designed specifically for 6-DOF myCobot manipulators. Programs are written in plain text files with the ``.cobot`` extension and compiled into validated binary machine instructions via a clean AST pipeline.

myCobot DSL Instruction Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: DSL Instructions
   :widths: 20 30 20 30
   :header-rows: 1

   * - Category
     - Instruction & Syntax
     - Parameters
     - Description
   * - **Power & State**
     - ``HOME``
     - None
     - Moves all 6 joints to calibrated zero reference position (:math:`0.0^\circ`).
   * - 
     - ``RELAX``
     - None
     - Releases servo brakes / disables motor torque for manual teaching.
   * - 
     - ``POWER``
     - None
     - Energizes servo motors and enables active position control.
   * - **Timing & Speed**
     - ``SPEED <percent>``
     - ``percent`` (:math:`1\% - 100\%`)
     - Sets travel feedrate velocity percentage.
   * - 
     - ``WAIT <ms>``
     - ``ms`` (milliseconds)
     - Dwells execution for specified hardware duration.
   * - **Tool Actuation**
     - ``TOOL GRIP``
     - None
     - Closes electric gripper end-effector.
   * - 
     - ``TOOL RELEASE``
     - None
     - Opens electric gripper end-effector.
   * - 
     - ``TOOL ANGLE <deg>``
     - ``deg`` (:math:`0^\circ - 100^\circ`)
     - Sets electric gripper opening angle.
   * - **Motion**
     - ``MOVE J1 <j1> J2 <j2> J3 <j3> J4 <j4> J5 <j5> J6 <j6> [SPEED <s>]``
     - ``J1..J6`` (deg), ``SPEED`` (%)
     - Coordinated 6-DOF multi-joint motion.
   * - 
     - ``MOVE_L X <x> Y <y> Z <z> RX <rx> RY <ry> RZ <rz> [SPEED <s>]``
     - ``X,Y,Z`` (mm), ``RX,RY,RZ`` (deg)
     - Cartesian linear tool interpolated path.

Example .cobot Program: Industrial Pick & Place
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

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

📊 Code coverage
----------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------

Install package

.. code-block:: bash

    pip3 install idecobot

Prepare main entry point by downloading `main.py` or create your own.

.. code-block:: bash

    wget -O main.py https://raw.githubusercontent.com/vroncevic/idecobot/main/main.py

CLI Command Options
^^^^^^^^^^^^^^^^^^^

Launch the graphical studio with default configuration:

.. code-block:: bash

    python3 main.py studio

Launch with initial script file and pre-selected serial port:

.. code-block:: bash

    python3 main.py studio --file ./scripts/pick_and_place.cobot --port /dev/ttyACM0 --verbose enable

.. list-table:: Studio CLI Options
   :widths: 20 15 25 40
   :header-rows: 1

   * - Option
     - Type
     - Choices
     - Description
   * - **--file**
     - ``str``
     - *File path*
     - Path to initial ``.cobot`` DSL script file to load on startup.
   * - **--port**
     - ``str``
     - *Serial port*
     - Serial communication port (e.g. ``/dev/ttyACM0`` or ``COM3``).
   * - **--verbose**
     - ``str``
     - ``enable``, ``disable``
     - Enable or disable verbose ATS operational logging.

Interactive Robot Studio Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. **Hardware Connection**:
   * Under the **Connection Panel**, select the detected serial port (e.g., ``/dev/ttyACM0``) or mock transport for offline testing.
   * Click **Connect**. The status bar updates to green ``Connected``.
2. **Manual Jogging**:
   * Navigate through **Joint**, **Cartesian**, **Tool**, and **Step** sub-panels.
   * Jog individual joints (:math:`J_1 \dots J_6`) or Cartesian axes (:math:`X, Y, Z, Rx, Ry, Rz`) with instant degree readouts.
   * Toggle servo torque (``Power`` / ``Relax``) and control gripper state (``Grip`` / ``Release``).
3. **DSL Scripting & Compilation**:
   * Open the **Script Editor** tab to author ``.cobot`` automation scripts.
   * Load bundled industrial templates from the Example Catalog.
   * Click **Compile** to validate syntax and inspect generated bytecode in the Bytecode Preview panel.
4. **Execution & Monitoring**:
   * Stream compiled instructions directly to the physical robot.
   * Observe live serial communication traffic and acknowledgments in the Serial Console.

📚 Docs
-------

More documentation and info at

* `idecobot.readthedocs.io <https://idecobot.readthedocs.io>`_
* `www.python.org <https://www.python.org/>`_

👥 Contributing
---------------

`Contributing to idecobot <https://github.com/vroncevic/idecobot/blob/dev/CONTRIBUTING.md>`_

📄 Copyright and licence
-------------------------

Copyright (C) 2026 by `vroncevic.github.io/idecobot <https://vroncevic.github.io/idecobot>`_

**idecobot** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/idecobot/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://www.python.org/psf/donations/

# Infrastructure Architectural Audit (`infrastructure_issues.md`)

This document tracks architectural compliance, SOLID principles, and clean boundary separation for the **Infrastructure / Adapters** layer (`idecobot/infrastructure/`).

---

## Master Status Matrix

| Component / Submodule | Audit Status | SOLID / Design Violations | Actionable Items |
|---|---|---|---|
| `infrastructure/gui/editor/` | 🟢 RESOLVED | Hardcoded string catalog eliminated (DIP/Single Source of Truth) | Dynamic loading from WorkspaceService |
| `infrastructure/gui/jog/` | 🟢 RESOLVED | Missing gripper action code in JogConstants | Added grip_action_grip & aligned tool_constants in factory |
| `infrastructure/gui/log/` | 🟢 RESOLVED | Bytecode preview column misalignment | Fixed field widths in BytecodePreview |
| `infrastructure/communication/`| 🟢 COMPLIANT | None (Threaded streamer & transport) | Strict protocol framing isolation |
| `infrastructure/storage/` | 🟢 RESOLVED | Missing user workspace lifecycle manager | WorkspaceService with auto-unpacking |
| `infrastructure/gui/menu/` | 🟢 RESOLVED | Monolithic IMenuBar method sprawl eliminated (ISP/SRP) | Decomposed into domain handlers (File, Diag, Help) |
| `infrastructure/diagnostics/` | 🟢 COMPLIANT | None (Modular SRP telemetry readers & coordinator facade) | Flushed serial buffers, low-voltage & thermal alerts |
| `infrastructure/cli/` | 🟢 COMPLIANT | None (Pluggable command executors) | Keep CLI separated from GUI loop |

---

## Architectural Findings & Resolutions

### 1. `BytecodePreview` DELAY Column Misalignment
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/gui/log/bytecode_constants.py`
  - `idecobot/infrastructure/gui/log/bytecode_preview.py`
  - `tests/bytecode_constants_test.py`
- **Violation Rationale:**
  - `HEX FRAME` column width in `BytecodePreview` was hardcoded to `{frame_hex:<40}`.
  - A 17-byte MyCobot joint coordinate packet serializes into 50 hexadecimal characters (`FE FE 0F 22 00 00 00 00 00 00 00 00 00 00 00 00 1E FA`).
  - Because 50 > 40, Python formatting pushed the `delay_str` out by 10 extra characters for long packets, while short packets (5 bytes, 7 bytes) were padded to 40 characters.
  - Furthermore, the header template `header_template` had `DELAY` positioned at index 55 instead of index 69.
- **Resolution:**
  - Introduced explicit column tokens in `BytecodeConstants`: `col_step_width = 6`, `col_cmd_width = 6`, `col_hex_width = 54`.
  - Re-anchored `header_template` so `DELAY` starts at column 69 and set `divider_length = 74`.
  - Updated `BytecodePreview.set_frames()` to format rows using parameterized column widths.
  - Created unit tests in `tests/bytecode_constants_test.py` asserting exact column indices for 5-byte and 17-byte frames.

### 2. User Workspace Auto-Initialization and Bundled Example Extraction
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/config/examples.tgz`
  - `idecobot/infrastructure/storage/iworkspace_service.py`
  - `idecobot/infrastructure/storage/workspace_constants.py`
  - `idecobot/infrastructure/storage/workspace_service.py`
  - `idecobot/infrastructure/gui/menu/menu_bar.py`
  - `idecobot/infrastructure/gui/menu/menu_bar_factory.py`
  - `idecobot/infrastructure/gui/setup/factory.py`
  - `tests/workspace_constants_test.py`
  - `tests/workspace_service_test.py`
- **Design Decisions & Compliance:**
  - Pure Dependency Injection: `WorkspaceService` receives strictly `WorkspaceConstants` without optional fallback parameters or internal path discovery.
  - Structural Typing: `WorkspaceService` satisfies `IWorkspaceService` without inheritance, `@override`, or interface imports.
  - Auto-Extraction: If `~/.idecobot/workspace` does not exist or has no `.cobot` scripts, the application extracts all 13 bundled scripts (8 command showcases + 5 advanced routines) from `infrastructure/config/examples.tgz`.
  - GUI Integration: `MenuBar` file open/save dialogs set `initialdir` to the active workspace directory.
  - Strict Parameter Contracts: `MenuBar` and `MenuBarFactory` require `workspace_dir: str` as a mandatory dependency with no `None` fallback.

### 3. Elimination of Hardcoded `ExampleCatalog` & Dynamic Workspace Integration
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/gui/editor/example_catalog.py` (DELETED)
  - `docs/source/idecobot.infrastructure.gui.editor.example_catalog.rst` (DELETED)
  - `idecobot/infrastructure/gui/editor/editor_constants.py`
  - `idecobot/infrastructure/gui/editor/editor_coordinator.py`
  - `idecobot/infrastructure/gui/editor/editor_panel_factory.py`
  - `idecobot/infrastructure/gui/setup/factory.py`
  - `tests/editor_coordinator_test.py`
  - `tests/editor_panel_test.py`
- **Violation Rationale:**
  - `example_catalog.py` contained 323 lines of hardcoded string literals duplicating `.cobot` scripts inside Python code. This violated DRY and the Single Source of Truth principle.
  - Users could not see custom `.cobot` scripts added to their workspace in the template dropdown.
- **Resolution:**
  - Injected `IWorkspaceService` and `IScriptStorageService` into `EditorCoordinator`.
  - `get_available_templates()` now dynamically queries `WorkspaceService.list_scripts()`, discovering all `.cobot` files in `~/.idecobot/workspace/`.
  - `load_template()` dynamically loads script contents using `IScriptStorageService.load_script()`.
  - Removed `ExampleCatalog` entirely from the codebase and Sphinx documentation.
  - Expanded combobox character width from 18 to 34 in `EditorConstants` to display complete routine names cleanly.

### 4. `MotionCodec` Fixed-Point Coordinate Encoding and Decoding Alignment
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/communication/protocol/motion_codec.py`
  - `tests/codec_test.py`
- **Violation Rationale:**
  - `pack_coords()` and `unpack_coords()` used a single `coord_scale_factor` (100.0) across all six parameters.
  - Elephant Robotics protocol requires $X, Y, Z$ in units of $0.1\text{ mm}$ (factor 10.0) and $RX, RY, RZ$ in units of $0.01^\circ$ (factor 100.0).
- **Resolution:**
  - Updated `pack_coords()` to scale indices 0..2 by `coord_scale_factor` (10.0) and indices 3..5 by `angle_scale_factor` (100.0).
  - Updated `unpack_coords()` to divide raw linear values by `coord_scale_factor` and raw angular values by `angle_scale_factor`.
  - Updated `tests/codec_test.py` to assert $0.1\text{ mm}$ linear resolution fidelity.

### 5. Menu Bar Domain Decomposition (`IMenuBar` Method Sprawl)
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/gui/menu/ifile_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/file_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/idiagnostics_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/diagnostics_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/ihelp_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/help_menu_handler.py`
  - `idecobot/infrastructure/gui/menu/imenu_bar.py`
  - `idecobot/infrastructure/gui/menu/menu_bar.py`
  - `idecobot/infrastructure/gui/menu/menu_bar_factory.py`
  - `tests/menu_bar_test.py`
- **Violation Rationale:**
  - `IMenuBar` was originally designed as a monolithic interface holding all menu operations (file dialogs, about dialog, help dialog, plus anticipated robot diagnostic queries).
  - This violated the **Interface Segregation Principle (ISP)** and **Single Responsibility Principle (SRP)**, creating method sprawl and coupling unrelated operations (file I/O, dialog UI, hardware diagnostics) to a single contract.
- **Resolution:**
  - Segregated the menu subsystem into dedicated domain handlers with structural protocols:
    1. **File Domain:** `IFileMenuHandler` (`new_script()`, `open_script_dialog()`, `save_script_dialog()`) and `FileMenuHandler`.
    2. **Diagnostics Domain:** `IDiagnosticsMenuHandler` (`diagnose_link()`, `diagnose_angles()`, `diagnose_coords()`, `diagnose_temperatures()`, `diagnose_voltages()`, `diagnose_power_on()`, `diagnose_release_servos()`, `run_startup_diagnostics()`) and `DiagnosticsMenuHandler`.
    3. **Help Domain:** `IHelpMenuHandler` (`show_about_dialog()`, `show_dsl_help()`) and `HelpMenuHandler`.
  - Refactored `IMenuBar` and `MenuBar` to act as a pure coordinator exposing domain handler accessors (`get_file_handler()`, `get_diagnostics_handler()`, `get_help_handler()`).
  - Maintained backward-compatible delegation methods on `MenuBar` while ensuring strict structural typing without protocol inheritance or circular dependencies.
  - All files strictly stay under line limits (132, 146, 94, 80, 205, 192 lines respectively).

### 6. Hardware Diagnostics Telemetry & Robot Health Subsystem
- **Status:** 🟢 COMPLIANT
- **Affected Files:**
  - `idecobot/infrastructure/diagnostics/diagnostics_constants.py`
  - `idecobot/infrastructure/diagnostics/ijoint_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/joint_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/iservo_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/servo_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/ispatial_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/spatial_diagnostics_reader.py`
  - `idecobot/infrastructure/diagnostics/idiagnostics_coordinator.py`
  - `idecobot/infrastructure/diagnostics/diagnostics_coordinator.py`
  - `idecobot/infrastructure/diagnostics/diagnostics_factory.py`
  - `tests/diagnostics_test.py`
- **Design Decisions & Compliance:**
  - Dedicated SRP Readers: Split telemetry retrieval into `JointDiagnosticsReader` (angles & temperatures), `SpatialDiagnosticsReader` (Cartesian coordinates & link responsiveness), and `ServoDiagnosticsReader` (operating voltages & power).
  - Resilient Serial Communication: Readers invoke `transport.flush()` before query frame transmission to purge pending bootloader bytes.
  - Automatic Overheat & Undervoltage Detection: Alerts triggered when servo temperatures exceed 50°C (e.g. Joint 5 at 60°C) or voltages drop below 6.8V.
  - Live Connection Hook: When connecting to robot arm (`engine.connect_port()`), an automatic 1.2s delayed startup routine flushes the serial port and executes `run_startup_diagnostics()`, logging full robot state to the Serial Log.

### 7. Gripper Action Code Mismatch in `JogPanelFactory` (`AttributeError`)
- **Status:** 🟢 RESOLVED
- **Affected Files:**
  - `idecobot/infrastructure/gui/jog/jog_constants.py`
  - `idecobot/infrastructure/gui/jog/jog_panel_factory.py`
  - `tests/jog_coordinator_test.py`
  - `tests/jog_panel_test.py`
- **Violation Rationale:**
  - `JogPanelFactory.handle_gripper()` attempted to check `if state == constants.grip_action_grip:`, but `constants` was an instance of `JogConstants` which only defined string verbs (`action_grip = 'Grip'`).
  - Integer action codes (`grip_action_grip = 1`, `grip_action_release = 0`) were defined in `ToolConstants` (`tool_constants`).
  - Clicking the Grip or Release button in the UI triggered a Tkinter callback `AttributeError: 'JogConstants' object has no attribute 'grip_action_grip'`.
- **Resolution:**
  - Updated `JogPanelFactory.handle_gripper()` to query `tool_constants.grip_action_grip`.
  - Added `grip_action_grip: int = 1` and `grip_action_release: int = 0` to `JogConstants` to ensure symmetrical robustness across both configuration models.
  - Implemented unit tests in `tests/jog_panel_test.py` asserting GUI button invocation for Grip, Release, Power, and Home operations.





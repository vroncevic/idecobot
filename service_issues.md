# Application Service Architectural Audit (`service_issues.md`)

This document tracks architectural compliance, SOLID principles, and clean boundary separation for the **Application Service** layer (`idecobot/core/service/`).

---

## Master Status Matrix

| Component / Submodule | Audit Status | SOLID / Design Violations | Actionable Items |
|---|---|---|---|
| `core/service/dsl/lexer/` | 🟢 COMPLIANT | None (Single responsibility tokenization) | Strict token typing |
| `core/service/dsl/parser/` | 🟢 COMPLIANT | None (Decoupled command parsers) | Granular parser registry |
| `core/service/dsl/compiler/`| 🟢 COMPLIANT | None (Pure AST bytecode generation) | Keep independent of transport |
| `core/service/dsl/linter/` | 🟢 COMPLIANT | None (Pluggable kinematic lint rules) | Maintain granular rule classes |
| `core/service/kinematics/` | 🟢 COMPLIANT | None (Kinematic boundary validation) | Preserve pure math validation |
| `core/service/communication/`| 🟢 COMPLIANT | None (Command encoder / decoder) | Abstract framing dependency |

---

## Architectural Findings & Resolutions

### 1. Granular Command Parsers & Compilers
- **Status:** 🟢 COMPLIANT
- **Observation:** Each statement (`MOVE`, `WAIT`, `SPEED`, `POWER`, `RELAX`, `TOOL`, `HOME`) is handled by a dedicated parser implementing `ICommandParser` and a dedicated compiler implementing `ICommandCompiler`.
- **Resolution:** Validated compliance with Single Responsibility (SRP) and Open/Closed Principle (OCP).

### 2. `MoveCoordsCommandCompiler` Multi-Scale Factor Application
- **Status:** 🟢 RESOLVED
- **Layer:** DSL Compilers (`idecobot/core/service/dsl/compiler/commands/move_coords_command_compiler.py`)
- **Observation:** Previously applied uniform `coord_scale_factor` to all 6 Cartesian parameters, incorrectly scaling orientations $RX, RY, RZ$ as millimeters.
- **Resolution:** Split scaling pipeline so indices 0..2 ($X, Y, Z$) use `coord_scale_factor` (10.0), and indices 3..5 ($RX, RY, RZ$) use `angle_scale_factor` (100.0).


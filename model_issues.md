# Domain Model Architectural Audit (`model_issues.md`)

This document tracks architectural compliance, SOLID principles, and clean boundary separation for the **Domain Model** layer (`idecobot/core/model/`).

---

## Master Status Matrix

| Component / Submodule | Audit Status | SOLID / Design Violations | Actionable Items |
|---|---|---|---|
| `core/model/dsl/ast/` | 🟢 COMPLIANT | None (Strict AST immutability) | Keep models pure value objects |
| `core/model/dsl/token/` | 🟢 COMPLIANT | None (Immutable dataclasses) | Maintain slots & frozen attributes |
| `core/model/dsl/diagnostic/`| 🟢 COMPLIANT | None (Typed error models) | Continue decoupling from presentation |
| `core/model/kinematics/` | 🟢 COMPLIANT | None (Granular data structures) | Preserved joint and spatial bounds |
| `core/model/communication/`| 🟢 COMPLIANT | None (MyCobotFrame value object)| Strict byte serialization models |

---

## Architectural Findings & Resolutions

### 1. `BytecodeConstants` Table Alignment
- **Status:** 🟢 RESOLVED
- **Layer:** Presentation / DTO Configuration (`idecobot/infrastructure/gui/log/bytecode_constants.py`)
- **Observation:** `HEX FRAME` column width in the GUI bytecode inspector was defaulting to 40 characters, which caused 17-byte robot packets (50 characters) to push the `DELAY` column out of alignment.
- **Resolution:** Added explicit `col_step_width` (6), `col_cmd_width` (6), and `col_hex_width` (54) tokens with a matching 74-character header template and divider line.

### 2. `ProtocolConstants` Fixed-Point Coordinate Scaling Alignment
- **Status:** 🟢 RESOLVED
- **Layer:** Protocol Constants (`idecobot/core/model/communication/protocol_constants.py`)
- **Observation:** `coord_scale_factor` was configured as `100.0`, treating Cartesian coordinates as having $0.01\text{ mm}$ unit scaling rather than the hardware protocol's actual $0.1\text{ mm}$ scaling ($10\text{ units/mm}$). This caused commands like $120.0\text{ mm}$ to encode as $12000$ ($1.2\text{ meters}$), causing out-of-bounds kinematic rejections on physical arms.
- **Resolution:** Updated `coord_scale_factor` to `10.0` while maintaining `angle_scale_factor` at `100.0` ($0.01^\circ$).


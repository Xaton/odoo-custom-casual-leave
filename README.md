# Custom Casual Leave Management - Odoo Module

## Overview

This custom Odoo module automates Casual Leave allocation for employees based on the organization's financial year cycle.

The module is designed to reduce manual HR work by automatically managing monthly casual leave accrual and yearly reset operations using scheduled cron jobs.

The leave policy implemented in this module follows a financial year structure from:

1 April → 31 March

Only eligible employees receive leave allocation based on their employment status and active contract condition.

---

## Features

- Automatically provides 1 Casual Leave every month
- Leave is credited only on the first day of each month
- Financial year based leave cycle (April to March)
- Automatically resets remaining Casual Leave balance after 31 March
- Supports automated execution through Odoo Cron Jobs
- Reduces manual HR leave management work

---

## Leave Allocation Logic

The module checks employee eligibility before allocating leave.

### Eligible Employees

Casual Leave is provided only if:

- Employee type is Full-Time
- Employee contract is in Running/Active state

If both conditions are satisfied, the employee receives:

1 Casual Leave per month

---

## Financial Year Workflow

### Monthly Accrual

- Starts from 1 April
- Runs automatically on the first day of every month
- Adds 1 Casual Leave to eligible employees

### Year-End Reset

- On 31 March, remaining unused Casual Leave balance is automatically reset to 0
- New leave cycle starts again from April

---

## Automation

The module uses Odoo Scheduled Actions (Cron Jobs) for automatic execution.

### Cron Operations

- Monthly Casual Leave Accrual
- Financial Year Leave Reset

This ensures the process runs without manual HR intervention.

---

## Technical Details

### Built Using

- Odoo
- Python
- XML
- Odoo Cron Jobs

### Main Components

- Employee eligibility validation
- Monthly leave allocation scheduler
- Financial year reset scheduler
- Automated backend processing

---

## Use Case

This module is useful for organizations that:

- Follow financial year leave policies
- Want automated leave allocation
- Need HR process automation
- Manage full-time employee contracts inside Odoo

---

## Installation

1. Copy the module into the `custom_addons` directory
2. Restart Odoo server
3. Update Apps List
4. Install the module from Odoo Apps menu

---

## Module Structure

```text
custom_casual_leave/
├── data/
│   └── cron.xml
├── models/
├── security/
├── __init__.py
├── __manifest__.py
└── .gitignore

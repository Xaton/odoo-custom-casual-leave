from odoo import models, fields
from datetime import date


class CasualLeaveAccrual(models.AbstractModel):
    _name = "casual.leave.accrual"
    _description = "Casual Leave Financial Year Accrual"

    # ==================================================
    # MONTHLY CASUAL LEAVE ACCRUAL (1 DAY ONLY)
    # ==================================================
    def run_monthly_cl_accrual(self):
        self = self.sudo()
        today = fields.Date.today()

        # -------------------------
        # Financial Year (Apr–Mar)
        # -------------------------
        if today.month >= 4:
            fy_start = date(today.year, 4, 1)
            fy_end = date(today.year + 1, 3, 31)
        else:
            fy_start = date(today.year - 1, 4, 1)
            fy_end = date(today.year, 3, 31)

        # Casual Leave Type
        leave_type = self.env["hr.leave.type"].search(
            [("name", "ilike", "Casual")], limit=1
        )
        if not leave_type:
            return

        employees = self.env["hr.employee"].search([])

        for emp in employees:

            # -------------------------
            # Contract-based join date
            # -------------------------
            contract = emp.contract_id
            if not contract or not contract.date_start:
                continue

            # ==================================================
            # ONLY FULL-TIME EMPLOYEES SHOULD GET CASUAL LEAVE
            # ==================================================
            # Contract Type must be "Full-Time"
            if not contract.contract_type_id:
                continue

            if contract.contract_type_id.name != "Full-Time":
                continue

            join_date = contract.date_start

            #Skip employees with expired contract
            if contract.state != "open":
                continue

            # Skip future joiners
            if join_date > today:
                continue

            # Skip employees joining after FY
            if join_date > fy_end:
                continue

            # Skip employees with contract end 
            if contract.date_end and contract.date_end < today:
                continue

            # -------------------------
            # Ensure FY Allocation
            # -------------------------
            allocation = self.env["hr.leave.allocation"].search([
                ("employee_id", "=", emp.id),
                ("holiday_status_id", "=", leave_type.id),
                ("date_from", "=", fy_start),
                ("date_to", "=", fy_end),
            ], limit=1)

            if not allocation:
                allocation = self.env["hr.leave.allocation"].create({
                    "name": f"Casual Leave FY {fy_start.year}-{fy_end.year}",
                    "employee_id": emp.id,
                    "holiday_status_id": leave_type.id,
                    "allocation_type": "regular",
                    "date_from": fy_start,
                    "date_to": fy_end,
                    "number_of_days": 1,   # must be >=1 at create
                })
                allocation.action_validate()
                 #  Mark accrual done for this month
                allocation.last_cl_accrual_date = today
                continue

            # -------------------------
            # Prevent double accrual in same month
            # -------------------------
            if allocation.last_cl_accrual_date:
                if (
                    allocation.last_cl_accrual_date.month == today.month
                    and allocation.last_cl_accrual_date.year == today.year
                ):
                    continue

            # -------------------------
            # Add exactly ONE CL
            # -------------------------
            allocation.number_of_days += 1
            allocation.last_cl_accrual_date = today

    # ==================================================
    # YEAR END RESET (31 MARCH)
    # ==================================================
    def run_cl_year_reset(self):
        self = self.sudo()
        today = fields.Date.today()

        if today.month != 3 or today.day != 31:
            return

        allocations = self.env["hr.leave.allocation"].search([
            ("date_to", "=", today),
        ])

        for alloc in allocations:
            alloc.write({
                "number_of_days": 0,
                "last_cl_accrual_date": False,
            })

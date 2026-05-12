from odoo import models, fields


class HrLeaveAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    last_cl_accrual_date = fields.Date(
        string="Last Casual Leave Accrual Date"
    )

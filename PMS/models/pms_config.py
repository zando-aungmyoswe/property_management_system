from odoo import fields, models, api
import pytz

_tzs = [
    (tz, tz)
    for tz in sorted(pytz.all_timezones,
                     key=lambda tz: tz if not tz.startswith('Etc/') else '_')
]


def _tz_get(self):
    return _tzs


class PmsFormat(models.Model):
    _name = "pms.format"

    name = fields.Char("Name")
    sample = fields.Char("Sample")
    active = fields.Boolean(default=True)
    format_line_id = fields.One2many("pms.format.detail", "format_id",
                                     "Format Line")

    @api.multi
    def toggle_active(self):
        for pt in self:
            if not pt.active:
                pt.active = self.active
        super(PmsFormat, self).toggle_active()


class PmsFormatDetail(models.Model):
    _name = "pms.format.detail"

    name = fields.Char("Name", default="New")
    format_id = fields.Many2one("pms.format", "Format")
    position_order = fields.Integer("Position Order")
    value_type = fields.Selection([('fix', "Fix"), ('dynamic', 'Dynamic'),
                                   ('digit', 'Digit'),
                                   ('datetime', 'Datetime')],
                                  string="Type",
                                  default="fix")
    fix_value = fields.Char("Value")
    digit_value = fields.Integer("Value")
    dynamic_value = fields.Char("Value")
    datetime_value = fields.Char("Value")
    value = fields.Char("Value")

    @api.onchange("value_type")
    def onchange_value_type(self):
        if self.value_type:
            if self.value_type == 'fix':
                self.value = self.fix_value
            if self.value_type == 'dynamic':
                self.value = self.dynamic_value
            if self.value_type == 'digit':
                self.value = str(self.digit_value)
            if self.value_type == 'datetime':
                self.value = str(self.datetime_value)


class PmsRule(models.Model):
    _name = "pms.rule"

    name = fields.Char("Name", default="Rule", readonly=True)
    currency_id = fields.Many2one('res.currency', "Currency")
    property_code_len = fields.Integer("Property Code Length")
    floor_code_len = fields.Integer('Floor Code Length')
    space_unit_code = fields.Many2one('pms.format', 'Space Unit Format')
    spu_format = fields.Char('Format',
                             related="space_unit_code.sample",
                             store=True)
    pos_id_format = fields.Many2one('pms.format', 'POS ID Format')
    pos_format = fields.Char('Format',
                             related="pos_id_format.sample",
                             store=True)
    timezone = fields.Selection(
        _tz_get,
        string='Timezone',
        default=lambda self: self._context.get('tz'),
        help=
        "The partner's timezone, used to output proper date and time values "
        "inside printed reports. It is important to set a value for this field. "
        "You should use the same timezone that is otherwise used to pick and "
        "render date and time values: your computer's timezone.")

    @api.multi
    def execute(self):
        self.ensure_one()
        if not self.env.user._is_admin() and not self.env.user.has_group(
                'base.group_system'):
            raise AccessError(_("Only administrators can change the settings"))

        self = self.with_context(active_test=False)

        config = self.env['res.config'].next() or {}
        if config.get('type') not in ('ir.actions.act_window_close', ):
            return config

        # force client-side reload (update user menu and current view)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
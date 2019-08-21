#-*- coding: utf-8 -*-
from odoo import models, fields, api, tools
import base64
import pytz

_tzs = [
    (tz, tz)
    for tz in sorted(pytz.all_timezones,
                     key=lambda tz: tz if not tz.startswith('Etc/') else '_')
]


def _tz_get(self):
    return _tzs


class PMSPropertyType(models.Model):
    _name = 'pms.property.type'

    name = fields.Char("Property Type", required=True)
    active = fields.Boolean(default=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.name
            result.append((record.id, code))
        return result

    @api.multi
    def toggle_active(self):
        for pt in self:
            if not pt.active:
                pt.active = self.active
        super(PMSPropertyType, self).toggle_active()


class PMSProperties(models.Model):
    _name = 'pms.properties'

    name = fields.Char("Name", required=True, size=250)
    code = fields.Char("Code", required=True)
    property_type = fields.Many2one(
        "pms.property.type",
        "Type",
        required=True,
        help="The properties's type is set the specific type.")
    uom = fields.Many2one("uom.uom",
                          "UOM",
                          required=True,
                          help="Unit Of Measure is need to set for Area.")
    gross_floor_area = fields.Integer('GFA', help="Gross Floor Area")
    net_lett_able_area = fields.Integer('NLA', help="Net Lett-able Area")
    web_site_url = fields.Char("Website", size=250, help="Website URL")
    auto_generate_posid = fields.Boolean("Auto Generate Pos ID",
                                         help="Auto Generating POS ID?")
    next_pos_id = fields.Char("Next Pos ID")
    pos_id_format = fields.Char("POS ID Format", size=250)
    office_phone = fields.Char("Office Phone", size=250)
    project_start_date = fields.Date("Project Start Date")
    target_open_date = fields.Date("Target Opening Date")
    actual_opening_date = fields.Date("Actual Openiing Date")
    bank_info = fields.Many2one('res.bank', "Bank Information")
    # bank_account = fields.Char("Bank Account")
    property_contract_address_id = fields.Many2many('res.partner',
                                                    'pms_contract_address',
                                                    string='Contacts',
                                                    domain=[('active', '=',
                                                             True)])
    management_company = fields.Many2one("res.company", "Company")
    leaseterms_line_id = fields.Many2many("pms.leaseterms",
                                          "pms_properties_leaseterms_rel",
                                          "properties_id",
                                          "leaseterm_id",
                                          string="Add LeaseTerms")
    currency_id = fields.Many2one("res.currency", "Currency")
    timezone = fields.Selection(
        _tz_get,
        string='Timezone',
        default=lambda self: self._context.get('tz'),
        help=
        "The partner's timezone, used to output proper date and time values "
        "inside printed reports. It is important to set a value for this field. "
        "You should use the same timezone that is otherwise used to pick and "
        "render date and time values: your computer's timezone.")
    image = fields.Binary(
        "Image",
        attachment=True,
        help=
        "This field holds the image used as avatar for this contact, limited to 1024x1024px",
    )
    image_medium = fields.Binary("Medium-sized image", attachment=True, help="Medium-sized image of this contact. It is automatically "\
        "resized as a 128x128px image, with aspect ratio preserved. "\
        "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True, help="Small-sized image of this contact. It is automatically "\
        "resized as a 64x64px image, with aspect ratio preserved. "\
        "Use this field anywhere a small image is required.")

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state",
                               string='State',
                               ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country',
                                 string='Country',
                                 ondelete='restrict')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.code
            result.append((record.id, code))
        return result

    @api.model
    def create(self, values):
        if values['image']:
            print("Image", values['image'])
            tools.image_resize_images(values, sizes={'image': (1024, None)})
        return super(PMSProperties, self).create(values)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals, sizes={'image': (1024, None)})
        return super(PMSProperties, self).write(vals)


# class Users(models.Model):
#     _inherit = "res.users"

#     @api.model_create_multi
#     def create(self, vals_list):
#         users = super(
#             Users, self.with_context(default_customer=False)).create(vals_list)
#         users.partner_id.user_id = users
#         return users

# class CrmTeam(models.Model):
#     _inherit = "crm.team"

#     @api.model
#     def create(self, values):
#         team = super(
#             CrmTeam,
#             self.with_context(mail_create_nosubscribe=True)).create(values)
#         if values.get('member_ids'):
#             team._add_members_to_favorites()
#         if values['member_ids']:
#             for user in values['member_ids']:
#                 for u in user[2]:
#                     print("user=>", user)
#                     users = self.env['res.users'].search([('user_id', '=', u)])

#                     users.partner_id.team_id = team
#                     print("partner_id", users.partner_id)
#         return team


class PMSFloor(models.Model):
    _name = 'pms.floor'

    name = fields.Char("Description", required=True)
    code = fields.Char("Floor Code")
    floor_code_ref = fields.Char("Floor Ref Code")
    active = fields.Boolean("Active")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.code
            result.append((record.id, code))
        return result


class PMSLeaseTerms(models.Model):
    _name = 'pms.leaseterms'

    name = fields.Char("Description", required=True)
    lease_term_type = fields.Selection([('month', "Month"), ('year', "Year")],
                                       string="Type")
    min_time_period = fields.Integer("Min Time Period")
    max_time_period = fields.Integer("Max Time Period")
    active = fields.Boolean("Active", default=True)


# class MlMeterType(models.Model):
#     _name = "ml.meter.type"

#     name = fields.Char("Meter Type")
#     i_lmr_date = fields.Date("Installed Date")
#     s_lmr_value = fields.Integer("Start Reading Value")
#     e_lmr_value = fields.Integer("End Reading Value")
#     uom_id = fields.Many2one("uom.uom", 'UOM')
#     digit = fields.Selection([('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
#                               ('7', '7'), ('8', '8'), ('9', '9')],
#                              "Display Digits")
#     end_date = fields.Date("Inactive On")
#     status = fields.Boolean("Status")
#     utility = fields.Many2one("ml.space.utility", "Utility")
#     display_type = fields.Many2one('ml.display.type', 'Display Type')
#     charge_type = fields.Selection([('fixed', 'Fixed'),
#                                     ('variable', 'Variable')],
#                                    string="Charge Type")

# class UtilityType(models.Model):
#     _name = "utility.type"

#     name = fields.Char("Utility Name")
#     code = fields.Char("Utility Type")

#     @api.multi
#     def name_get(self):
#         result = []
#         for record in self:
#             code = record.code
#             result.append((record.id, code))
#         return result

# class MeterNumber(models.Model):
#     _name = 'meter.number'

#     name = fields.Char("Name")
#     number = fields.Integer('Number')

#     @api.multi
#     def name_get(self):
#         result = []
#         for record in self:
#             number = record.number
#             result.append((record.id, number))
#         return result


class PMSSpaceUtility(models.Model):
    _name = 'pms.space.utility'

    name = fields.Char("New")
    # utility_type = fields.Many2one('utility.type', "Utility Type")
    # utility_code = fields.Char("Code", related="utility_type.code", store=True)
    # meter_no = fields.Many2one("meter.number")
    start_date = fields.Date("Start Date")
    utt_idd = fields.Boolean("IDD")
    utt_local = fields.Boolean("LOCAL")
    utt_mobile = fields.Boolean("MOBILE")
    utt_std = fields.Boolean("STD")
    utt_gen = fields.Boolean("GEN")
    utt_sub = fields.Boolean("SUB")
    interface_type = fields.Selection([('auto', 'Auto'), ('manual', 'Manual'),
                                       ('mobile', 'Mobile')], "Interface Type")
    remark = fields.Text("Remark")
    # meter_type_id = fields.One2many("ml.meter.type", 'utility', "Meter Type")
    unit_id = fields.Many2one("pms.space", string='Space Unit')


class PMSSpace(models.Model):
    _name = 'pms.space'

    name = fields.Char("Name", default="New", readonly=True)
    property_id = fields.Many2one("pms.properties",
                                  string="Property",
                                  required=True)
    floor_id = fields.Many2one("pms.floor", string="Floor")
    unit_no = fields.Char("Space Unit No", required=True)
    area = fields.Integer("Space Area")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    uom = fields.Many2one("uom.uom", "UOM")
    remark = fields.Text("Remark")
    status = fields.Boolean("Status", default=True)
    utility_id = fields.One2many("pms.space.utility", "unit_id", "Facility")

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.unit_no
            result.append((record.id, code))
        return result

    @api.model
    def create(self, values):
        if values.get('name', 'New') == 'New':
            values['name'] = 'Mall(' + self.env['ml.mall'].browse(
                values['mall']).code + ')/Unit(' + values['unit_no'] + ')'
        return super(PMSSpace, self).create(values)


# class MlDisplayType(models.Model):
#     _name = "ml.display.type"

#     name = fields.Char("Display Name")
#     code = fields.Char("Display Code")

#     @api.multi
#     def name_get(self):
#         result = []
#         for record in self:
#             code = record.code
#             result.append((record.id, code))
#         return result

# class ResStateCity(models.Model):
#     _name = 'res.state.city'

#     name = fields.Char("Name")
#     state_id = fields.Many2one("res.country.state", "State")

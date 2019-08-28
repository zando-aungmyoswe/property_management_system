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


class PMSProperties(models.Model):
    _name = 'pms.properties'

    l = 80

    @api.multi
    def get_limit(self):
        self.limit = 2
        l = 2

    @api.model
    def company_groups(self, present_ids, domain, **kwargs):
        companies = self.env['res.company'].search([]).name_get()
        return companies, None

    _group_by_full = {
        'company_id': company_groups,
    }

    company_id = fields.Many2many('res.company')
    name = fields.Char("Name", required=True, size=250)
    code = fields.Char("Code", required=True)
    property_type = fields.Many2one(
        "pms.property.type",
        "Type",
        required=True,
        help="The properties's type is set the specific type.")
    uom = fields.Many2one("pms.uom",
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
    bank_info = fields.Many2one('pms.bank', "Bank Information")
    # bank_account = fields.Char("Bank Account")
    property_contact_address_id = fields.Many2many('res.partner',
                                                   'pms_contact_address',
                                                   'property_id',
                                                   'partner_id',
                                                   string='Contacts',
                                                   domain=[('active', '=',
                                                            True)])
    property_address_id = fields.Many2many('res.partner',
                                           'pms_address',
                                           string='Contacts',
                                           store=False)
    management_company = fields.Many2one("res.company", "Company")
    leaseterms_line_id = fields.Many2many("pms.leaseterms",
                                          "pms_properties_leaseterms_rel",
                                          "properties_id",
                                          "leaseterm_id",
                                          string="Add LeaseTerms")
    currency_id = fields.Many2one("pms.currency", "Currency")
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
    city_id = fields.Many2one("pms.city",
                              string='State',
                              ondelete='restrict',
                              domain="[('state_id', '=?', state_id)]")
    state_id = fields.Many2one("pms.state",
                               string='State',
                               ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('pms.country',
                                 string='Country',
                                 ondelete='restrict')
    limit = fields.Integer(compute=get_limit)
    rows = fields.Integer(string="Rows", default=80)
    # position_type = fields.Selection([('ceo', 'CEO'), ('manager', "Manager"),
    #                                   ('superviser', "Superviser")],
    #                                  string="Position")

    @api.multi
    def action_contact_filter(self):
        print("position", self.position_type)
        if self.position_type == 'manager':
            self.property_address_id = None
            contact = self.mapped('property_contact_address_id')
            for loop in contact:
                if loop.id == 10:
                    self.property_address_id = loop
            return self.property_address_id

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
        print("Hello!", vals)
        return super(PMSProperties, self).write(vals)


# class PMSContactAddress(models.Model):
#     _name = "pms.contact.address"

#     property_id = fields.Many2one('pms.properties', "Properties")
#     partner_id = fields.Many2one('res.partner', "Partner")
#     name = fields.Char("Name", default="New")

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
    active = fields.Boolean("Active", default=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.code
            result.append((record.id, code))
        return result

    @api.multi
    def toggle_active(self):
        for pt in self:
            if not pt.active:
                pt.active = self.active
        super(PMSFloor, self).toggle_active()


class PMSLeaseTerms(models.Model):
    _name = 'pms.leaseterms'

    name = fields.Char("Description", required=True)
    lease_term_type = fields.Selection([('month', "Month"), ('year', "Year")],
                                       string="Type")
    min_time_period = fields.Integer("Min Time Period")
    max_time_period = fields.Integer("Max Time Period")
    active = fields.Boolean("Active", default=True)


class PMSSpaceUnit(models.Model):
    _name = 'pms.space.unit'

    name = fields.Char("Name", default="New", readonly=True)
    property_id = fields.Many2one("pms.properties",
                                  string="Property",
                                  required=True)
    floor_id = fields.Many2one("pms.floor", string="Floor")
    parent_id = fields.Many2one("pms.space.unit", "Parent", store=True)
    unittype_id = fields.Many2one("pms.space.type", "Space Type")
    uom = fields.Many2one("pms.uom", "UOM")
    management_id = fields.Many2one("pms.space.unit.management",
                                    "Space Management")
    unit_no = fields.Char("Unit Code", required=True)
    area = fields.Integer("Space Area")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    status = fields.Selection([('vacant', 'Vacant'), ('occupied', 'Occupied')],
                              string="Status",
                              default="vacant")
    # utility_id = fields.One2many("pms.space.utility", "unit_id", "Facility")

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
            values['name'] = 'PMS(' + self.env['pms.properties'].browse(
                values['property_id']
            ).code + ')/Unit(' + values['unit_no'] + ')'
        return super(PMSSpaceUnit, self).create(values)


# class ResStateCity(models.Model):
#     _name = 'res.state.city'

#     name = fields.Char("Name")
#     state_id = fields.Many2one("res.country.state", "State")

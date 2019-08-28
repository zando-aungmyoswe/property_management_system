from odoo import models, fields, api


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


class PMSUtilityType(models.Model):
    _name = "pms.utility.type"

    name = fields.Char("Utility Name")
    code = fields.Char("Utility Code")
    parent_id = fields.Many2one("pms.utility.type", "Parent")
    active = fields.Boolean(default=True)

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
        super(PMSPropertyType, self).toggle_active()


class PMSSpaceUtility(models.Model):
    _name = 'pms.facilities'

    name = fields.Char("Description", default="New")
    utility_type_id = fields.Many2one('pms.utility.type',
                                      "Utility Type",
                                      required=True)
    meter_no = fields.Many2one("pms.meter.type", "Meter No", required=True)
    space_unit_id = fields.Many2one("pms.space.unit", string="Space Unit")
    display_type = fields.Many2one("pms.display.type", string="Display Type")
    supplier_type_id = fields.Many2one('pms.utility.type',
                                       "Supplier Type",
                                       required=True)
    start_date = fields.Date("Start Date")
    interface_type = fields.Selection([('auto', 'Auto'), ('manual', 'Manual'),
                                       ('mobile', 'Mobile')], "Interface Type")
    remark = fields.Text("Remark")
    install_date = fields.Date("Install Date")
    start_reading_value = fields.Integer("Start Reading Value")
    end_reading_value = fields.Integer("End Reading Value")
    digit = fields.Integer("Digit")
    end_date = fields.Date("End Date")
    status = fields.Boolean("Status", default=True)


class PMSSpaceUntiManagement(models.Model):
    _name = 'pms.space.unit.management'

    name = fields.Char("Name", default="New", readonly=True)
    floor_id = fields.Many2one("pms.floor", "Floor")
    space_unit_id = fields.Many2one("pms.space.unit", "From Unit")
    area = fields.Integer("Area")
    no_of_unit = fields.Integer("No of Unit")
    to_unit = fields.Char("To Unit")
    combination_type = fields.Selection(
        [('random', 'Random'), ('range', 'Range')],
        "Combination Type",
    )
    action_type = fields.Selection([('division', 'Division'),
                                    ('combination', 'Combination')],
                                   "Action Type",
                                   default="division")
    state = fields.Selection([('draft', "Draft"), ('done', "Done")],
                             "Status",
                             default="draft")
    space_unit = fields.Many2many("pms.space.unit", string="Unit")

    @api.multi
    def action_division(self):
        if self.state == 'draft':
            self.state = "done"

    @api.multi
    def action_combination(self):
        if self.state == 'draft':
            self.state = "done"


class PMSSpaceType(models.Model):
    _name = 'pms.space.type'

    name = fields.Char("Name")
    chargeable = fields.Boolean("Chargeable")
    divisible = fields.Boolean("Divisible")


class PMSDisplayType(models.Model):
    _name = "pms.display.type"

    name = fields.Char("Display Name")
    code = fields.Char("Display Code")
    active = fields.Boolean(default=True)

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            code = record.code
            result.append((record.id, code))
        return result


class PMSMeterType(models.Model):
    _name = "pms.meter.type"

    name = fields.Char("Meter No")
    utility_id = fields.Many2one("pms.utility.type", "Utility Type")
    display_type = fields.Many2one('pms.display.type', 'Display Type')
    digit = fields.Selection([('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                              ('7', '7'), ('8', '8'), ('9', '9')],
                             "Display Digits")
    charge_type = fields.Selection([('fixed', 'Fixed'),
                                    ('variable', 'Variable')],
                                   string="Charge Type")


class PMSTerms(models.Model):
    _name = "pms.terms"

    name = fields.Char("Name", default="New", readonly=True)
    space_unit_fromat_id = fields.Many2one("pms.format",
                                           string="Unit Code Format")
    pos_id_format_id = fields.Many2one("pms.format", string="POS ID Format")
    company_id = fields.Many2one("res.company", string="Company")
    is_auto_generate_posid = fields.Boolean("Auto Generate POS ID")
    property_code_len = fields.Integer("Property Code Len")
    floor_code_len = fields.Integer("Floor Code Len")
    space_unit_code_len = fields.Integer("Space Unit Code Len")
    active = fields.Boolean("Active", default=True)

    @api.multi
    def toggle_active(self):
        for pt in self:
            if not pt.active:
                pt.active = self.active
        super(PMSTerms, self).toggle_active()


class PMSUom(models.Model):
    _name = "pms.uom"

    name = fields.Char("Name", required=True)
    category_id = fields.Many2one("pms.uom.category",
                                  "Category",
                                  required=True)
    uom_type = fields.Selection([('bigger', "Bigger"),
                                 ('reference', 'Reference'),
                                 ('smaller', 'Smaller')],
                                "Type",
                                default='reference',
                                required=True)
    active = fields.Boolean(default=True)

    @api.multi
    def toggle_active(self):
        for pt in self:
            if not pt.active:
                pt.active = self.active
        super(PMSUom, self).toggle_active()


class PMSUomCategory(models.Model):
    _name = "pms.uom.category"

    name = fields.Char("Name", required=True)
    type_id = fields.Many2one("pms.uom.category", "Type")


class PMSBank(models.Model):
    _name = 'pms.bank'

    country = fields.Many2one("pms.country", "Country Name")
    city_id = fields.Many2one("pms.city", "City Name")
    state_id = fields.Many2one("pms.state", "State Name")
    name = fields.Char("Name")
    bic = fields.Char("Bank Identifier Code")
    phone = fields.Char("Phone")
    email = fields.Char("Email")
    no = fields.Char("No")
    street = fields.Char("Street")
    zip_code = fields.Char("Zip")
    active = fields.Char(default=True)


class PMSCity(models.Model):
    _name = "pms.city"

    state_id = fields.Many2one("pms.state", "State Name", required=True)
    name = fields.Char("City Name", required=True)
    code = fields.Char("City Code", required=True)


class PMSCity(models.Model):
    _name = "pms.state"

    country_id = fields.Many2one("pms.country", "Country Name", required=True)
    name = fields.Char("State Name", required=True)
    code = fields.Char("State Code", required=True)


class PMSCity(models.Model):
    _name = "pms.country"

    name = fields.Char("Country Name", required=True)
    code = fields.Char("Country Code", required=True)


class PMSCurrency(models.Model):
    _name = "pms.currency"

    name = fields.Char("Name", required=True)
    symbol = fields.Char("Symbol", required=True)
    status = fields.Boolean("Active")

    @api.multi
    def action_status(self):
        if self.status == True:
            self.status= False
        else:
            self.status = True
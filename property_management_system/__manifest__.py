# -*- coding: utf-8 -*-
{
    'name':
    "Property Management System",
    'description':
    """Property Management System for Payment Bill Transporting Analysis""",
    'author':
    "Aung Myo Swe",
    'summary':
    """Property Management System""",
    'website':
    "www.zandotech.com",
    'category':
    'base',
    'version':
    '12.1.0.1',
    'depends': ['base', 'uom', 'web'],
    'data': [
        'views/pms_property_type_view.xml',
        'views/pms_properties_view.xml',
        'views/pms_floor_views.xml',
        'security/ir.model.access.csv',
        'views/pms_rule_configuration_view.xml',
        'views/pms_format_view.xml',
        'views/pms_leaseterms_view.xml',
        'views/list_view.xml',
        'views/pms_terms_view.xml',
        'views/pms_space_unit_management.xml',
        'views/pms_space_unit_view.xml',
        'views/pms_facilities_view.xml',
    ],
    'installable':
    True,
    'application':
    True,
}
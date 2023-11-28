# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

{
    "name": "User Simulation",
    "summary": """
        User simulation For admin Who can login to any user
        from this module using smart button on upper right corner.
    """,
    "description": """
    To unable smart button you have to give access rights to perticular user from,
    Settings > Users > select the User > Other : User Simulation(tick the checkbox)
    """,
    "author": "Heliconia Solutions Pvt. Ltd.",
    "website": "https://heliconia.io",
    "category": "Tools",
    "version": "15.0.0.1.0",
    "license": "OPL-1",
    "depends": ["base", "web"],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "wizard/user_simulation_wizard_view.xml",
    ],
    "images": ["static/description/heliconia_odoo_user_simulation.gif"],
    "assets": {
        "web.assets_backend": [
            "hspl_user_simulation/static/src/js/user_simulation.js",
        ],
        "web.assets_qweb": [
            "hspl_user_simulation/static/src/xml/widget.xml",
        ],
    },
}

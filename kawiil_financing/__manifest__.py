{
    "name": "Kawiil Financing",
    "summary": "Module to keep track of Kawiil Motors Loan Cusotmer's Loan Applications",
    "category": "Kawiil/Financing",
    "maintainer": "Odoo Developer",
    "website": "https://github.com/odoo-trainings/development-masterclass",
    "version": "1.0.0",
    "author": "ODOP, Trainee",
    "depends": ["product"],
    # Odoo Proprietary License, the default for custom customer work.
    "license": "OPL-1",
    # XML and CSV files Odoo loads on install, in the order you list them.
    # TODO (assignments 2.05 to 2.08): register your data files here. Order is
    # not cosmetic — Odoo resolves external ids as it reads, so a file can only
    # refer to something a file above it already created. Security, then views,
    # then the menu that points at them:
    #     "security/kawiil_financing_groups.xml",
    #     "security/ir.model.access.csv",
    #     "security/kawiil_financing_security.xml",
    #     "views/loan_application_views.xml",
    #     "views/loan_application_tag_views.xml",
    #     "views/loan_application_document_type_views.xml",
    #     "views/kawiil_financing_menu.xml",
    "data": [],
    # Sample records, loaded only when a database is created with demo data.
    # TODO (assignments 2.04 and 2.08): configuration data before transactional
    # data, so the loans can refer to tags that already exist:
    #     "demo/config_demo.xml",
    "demo": [
        "demo/loan_demo.xml",],
    "application": True,
}

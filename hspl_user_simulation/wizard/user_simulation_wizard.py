# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

import odoo
import werkzeug
from odoo import SUPERUSER_ID, _, fields, http, models
from odoo.addons.web.controllers.main import ensure_db
from odoo.http import request


class UserSimulationWizard(models.TransientModel):
    _name = "user.simulation.wizard"
    _description = "user simulation wizard"

    user_id = fields.Many2one("res.users", string="User ")

    @http.route("/web/dbredirect", type="http", auth="none")
    def web_db_redirect(self, redirect="/", **kw):
        ensure_db()
        return werkzeug.utils.redirect(redirect, 303)

    def _login_redirect(self, uid, redirect=None):
        return redirect if redirect else "/web"

    def login_simulation(self, redirect=None):
        database_name = self.env.cr.dbname
        request.params["login_success"] = False
        if request.httprequest.method == "GET" and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)
        if not request.uid:
            request.uid = SUPERUSER_ID
        values = request.params.copy()
        if request.httprequest.method == "POST":
            old_uid = request.uid
            uid_a = self.user_id
            request.session["is_simulated"] = True
            uid = request.session.authenticate(database_name, uid_a.login, "aaaaa")
            if uid is not False:
                request.params["login_success"] = True
                return {"type": "ir.actions.act_url", "url": "/web?", "target": "self"}
            request.uid = old_uid
            values["error"] = _("Wrong login/password")
        else:
            if "error" in request.params and request.params.get("error") == "access":
                values["error"] = _(
                    "Only employee can access this database. Please contact the administrator."
                )

        if "login" not in values and request.session.get("auth_login"):
            values["login"] = request.session.get("auth_login")

        if not odoo.tools.config["list_db"]:
            values["disable_database_manager"] = True

        response = request.render("web.login", values)
        response.headers["X-Frame-Options"] = "DENY"
        return response

# Copyright 2018, 2020 Heliconia Solutions Pvt Ltd (https://heliconia.io)

import logging

import pytz
from odoo import SUPERUSER_ID, api, models
from odoo.exceptions import AccessDenied
from odoo.http import request

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        if not password:
            raise AccessDenied()
        ip = request.httprequest.environ["REMOTE_ADDR"] if request else "n/a"
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                with self._assert_can_auth():
                    user = self.search(
                        self._get_login_domain(login),
                        order=self._get_login_order(),
                        limit=1,
                    )
                    if not user:
                        raise AccessDenied()
                    user = user.with_user(user)
                    if type(request.params).__name__ == "OrderedDict":
                        user._check_credentials(password, user_agent_env)
                    tz = request.httprequest.cookies.get("tz") if request else None
                    if tz in pytz.all_timezones and (
                        not user.tz or not user.login_date
                    ):
                        # first login or missing tz -> set tz to browser tz
                        user.tz = tz
                    user._update_last_login()
        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s from %s", db, login, ip)
            raise
        _logger.info("Login successful for db:%s login:%s from %s", db, login, ip)
        return user.id

    @api.model
    def check_for_user_simulation(self, user_id):
        # got the call here : we will check here the group and if it is simulated or not
        if (
            user_id
            in self.env.ref("hspl_user_simulation.group_user_simulation").users.ids
        ):
            return True
        if (
            self.env.ref("hspl_user_simulation.group_user_simulation").users.ids
            and user_id
            not in self.env.ref("hspl_user_simulation.group_user_simulation").users.ids
            and request.session.get("is_simulated")
        ):
            return True
        request.session["is_simulated"] = False
        return False

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if self.env.context.get("user_simulation_context"):
            user_ids = self.env.ref("base.group_user").users.ids
            args = args or []
            args += [("id", "in", user_ids)]
        return super(ResUsers, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )

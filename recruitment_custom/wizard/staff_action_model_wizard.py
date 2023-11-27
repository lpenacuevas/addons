from odoo import api, exceptions, fields, models


class staffModel(models.TransientModel):
    _name = "library.checkout.massmessage"
    _description = "Send message"

    message_subject = fields.Char()
    message_body = fields.Html()

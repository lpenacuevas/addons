import pytz
from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command

WARNING_MESSAGE = [
    ('no-message', 'No Message'),
    ('warning', 'Warning'),
    ('block', 'Blocking Message')
]
WARNING_HELP = 'Selecting the "Warning" option will notify user with the message, Selecting "Blocking Message" will throw an exception with the message and block the flow. The Message has to be written in the next field.'

ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')


@api.model
def _lang_get(self):
    return self.env['res.lang'].get_installed()


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]


def _tz_get(self):
    return _tzs


class PartnerApplicant(models.Model):
    _name = 'partner.applicant'
    _inherit = ['format.address.mixin', 'avatar.mixin']
    _order = "display_name ASC, id DESC"

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    name = fields.Char(compute="_compute_name",
                       inverse="_inverse_name_after_cleaning_whitespace",
                       required=False,
                       store=True,
                       readonly=False, )
    display_name = fields.Char(compute='_compute_display_name', recursive=True, store=True, index=True)
    date = fields.Date(index=True)
    title = fields.Many2one('res.partner.title', 'Título')
    ref = fields.Char(string='Reference', index=True)
    lang = fields.Selection(_lang_get, string='Idioma',
                            help="All the emails and documents sent to this contact will be translated in this language.")
    active_lang_count = fields.Integer(compute='_compute_active_lang_count')
    tz = fields.Selection(_tz_get, string='Timezone', default=lambda self: self._context.get('tz'),
                          help="When printing documents and exporting/importing data, time values are computed according to this timezone.\n"
                               "If the timezone is not set, UTC (Coordinated Universal Time) is used.\n"
                               "Anywhere else, time values are computed according to the time offset of your web client.")

    tz_offset = fields.Char(compute='_compute_tz_offset', string='Timezone offset', invisible=True)
    bank_ids = fields.One2many('res.partner.bank', 'partner_id', string='Banks')
    website = fields.Char('Sitio web')
    comment = fields.Html(string='Notas')

    category_id = fields.Many2many('res.partner.category', column1='partner_id',
                                   column2='category_id', string='Categorías', default=_default_category)
    active = fields.Boolean(default=True)
    type = fields.Selection(
        [('contact', 'Contacto'),
         ('invoice', 'Dirección de factura'),
         ('delivery', 'Dirección de entrega'),
         ('other', 'Otra dirección'),
         ("private", "Dirección privada"),
         ], string='Tipo de Dirección',
        default='contact',
        help="Invoice & Delivery addresses are used in sales orders. Private addresses are only visible by authorized users.")
    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='Estado', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='País', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    partner_latitude = fields.Float(string='Geo Latitud', digits=(10, 7))
    partner_longitude = fields.Float(string='Geo Longitud', digits=(10, 7))
    email = fields.Char('Correo electrónico')
    email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    phone = fields.Char('Teléfono')
    mobile = fields.Char('Móvil')
    color = fields.Integer(string='Color Index', default=0)
    contact_address = fields.Char(compute='_compute_contact_address', string='Complete Address')

    self = fields.Many2one(comodel_name=_name, compute='_compute_get_ids')

    def _email_send(self, email_from, subject, body, on_error=None):
        for partner in self.filtered('email'):
            tools.email_send(email_from, [partner.email], subject, body, on_error)
        return True

    def _parse_partner_name(self, text):
        """ Parse partner name (given by text) in order to find a name and an
        email. Supported syntax:

          * Raoul <raoul@grosbedon.fr>
          * "Raoul le Grand" <raoul@grosbedon.fr>
          * Raoul raoul@grosbedon.fr (strange fault tolerant support from
            df40926d2a57c101a3e2d221ecfd08fbb4fea30e now supported directly
            in 'email_split_tuples';

        Otherwise: default, everything is set as the name. Starting from 13.3
        returned email will be normalized to have a coherent encoding.
         """
        name, email = '', ''
        split_results = tools.email_split_tuples(text)
        if split_results:
            name, email = split_results[0]

        if email:
            email = tools.email_normalize(email)
        else:
            name, email = text, ''

        return name, email

    @api.depends('name', 'email')
    def _compute_email_formatted(self):
        """ Compute formatted email for partner, using formataddr. Be defensive
        in computation, notably

          * double format: if email already holds a formatted email like
            'Name' <email@domain.com> we should not use it as it to compute
            email formatted like "Name <'Name' <email@domain.com>>";
          * multi emails: sometimes this field is used to hold several addresses
            like email1@domain.com, email2@domain.com. We currently let this value
            untouched, but remove any formatting from multi emails;
          * invalid email: if something is wrong, keep it in email_formatted as
            this eases management and understanding of failures at mail.mail,
            mail.notification and mailing.trace level;
          * void email: email_formatted is False, as we cannot do anything with
            it;
        """
        self.email_formatted = False
        for partner in self:
            emails_normalized = tools.email_normalize_all(partner.email)
            if emails_normalized:
                # note: multi-email input leads to invalid email like "Name" <email1, email2>
                # but this is current behavior in Odoo 14+ and some servers allow it
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    ','.join(emails_normalized)
                ))
            elif partner.email:
                partner.email_formatted = tools.formataddr((
                    partner.name or u"False",
                    partner.email
                ))

    @api.depends('lang')
    def _compute_active_lang_count(self):
        lang_count = len(self.env['res.lang'].get_installed())
        for partner in self:
            partner.active_lang_count = lang_count

    def _compute_avatar(self, avatar_field, image_field):
        partners_without_image = self.filtered(lambda p: not p[image_field])
        for _, group in tools.groupby(partners_without_image, key=lambda p: p._avatar_get_placeholder_path()):
            group_partners = self.env['partner.applicant'].concat(*group)
            group_partners[avatar_field] = group_partners[0]._avatar_get_placeholder()

        for partner in self - partners_without_image:
            partner[avatar_field] = partner[image_field]

    """Extra fields for applicants"""

    birthday = fields.Date('Fecha de Nacimiento', tracking=True)
    nationality_id = fields.Many2one(
        'res.country', 'Nacionalidad (País)', tracking=True)
    gender = fields.Selection([
        ('male', 'Masculino'),
        ('female', 'Femenino'),
        ('other', 'Otro')
    ], tracking=True, string='Género')
    identification_id = fields.Char(string='No. Cédula de Identidad y Electoral',
                                    tracking=True)
    passport_id = fields.Char('No. Pasaporte', groups="hr.group_hr_user", tracking=True)
    marital_status = fields.Selection(
        string='Estado Civil',
        selection=[('single', 'Soltero'),
                   ('married', 'Casado'),
                   ('legal cohabitant', 'Union Libre')])
    blood_type = fields.Selection(
        string='Tipo de Sangre',
        selection=[('ab+', 'AB+'),
                   ('ab-', 'AB-'),
                   ('a+', 'A+'),
                   ('a-', 'A-'),
                   ('b+', 'B+'),
                   ('b-', 'B-'),
                   ('o+', 'O+'),
                   ('o-', 'O-')
                   ])
    reference_spot = fields.Char('Punto de Referencia')
    emergency_contact = fields.Char('Notificar a:')
    emergency_contact_phone = fields.Char('Teléfono(s)')
    emergency_contact_relationship = fields.Char('Parentesco')
    have_any_illness = fields.Char('Padece de alguna enfermedad?')
    have_any_allergy = fields.Char('Es alergico a algún medicamento?')

    partner_family_ids = fields.One2many('partner.family', 'partner_id', string='Composición familiar')
    partner_job_ids = fields.One2many('partner.job.experience', 'partner_relate_id', string='Experiencia Laboral')
    partner_skill_ids = fields.One2many('res.partner.skill', 'partner_id', string="Skills")
    partner_complementary_ids = fields.One2many('partner.complementary.experience', 'partner_complementary_id',
                                                string='Experiencia Laboral')
    partner_references_ids = fields.One2many('partner.references', 'partner_references_id',
                                             string='Composición familiar')
    partner_academy_ids = fields.One2many('partner.academy.record', 'partner_academy_id', string='Formacion Academica')

    res_partner_id = fields.Many2one('res.partner', 'Contacto Asociado')

    @api.onchange('res_partner_id')
    def _compute_fields_from_res_partner(self):
        for rec in self:
            if rec.res_partner_id:
                partner_data = rec.res_partner_id.read()[0]
                for field_name, field_value in partner_data.items():
                    excluded_fields = [
                        '__last_update', 'create_date', 'write_date', 'id', 'display_name',
                        'message_last_post', 'message_follower_ids'
                    ]
                    if field_name not in excluded_fields:
                        if field_value and field_name in rec._fields:
                            rec[field_name] = field_value

    """Changing parameters to first and lastname"""

    firstname = fields.Char("Nombres", index=True)
    lastname = fields.Char("Apellidos", index=True)

    @api.model
    def create(self, vals):
        """Add inverted names at creation if unavailable."""
        context = dict(self.env.context)
        name = vals.get("name", context.get("default_name"))

        if name is not None:
            # Calculate the splitted fields
            inverted = self._get_inverse_name(
                self._get_whitespace_cleaned_name(name),
            )
            for key, value in inverted.items():
                if not vals.get(key) or context.get("copy"):
                    vals[key] = value
            # Remove the combined fields
            if "name" in vals:
                del vals["name"]
            if "default_name" in context:
                del context["default_name"]
        # pylint: disable=W8121
        return super(PartnerApplicant, self.with_context(context)).create(vals)

    def copy(self, default=None):
        """Ensure partners are copied right.

        Odoo adds ``(copy)`` to the end of :attr:`~.name`, but that would get
        ignored in :meth:`~.create` because it also copies explicitly firstname
        and lastname fields.
        """
        return super(PartnerApplicant, self.with_context(copy=True)).copy(default)

    @api.model
    def default_get(self, fields_list):
        """Invert name when getting default values."""
        result = super(PartnerApplicant, self).default_get(fields_list)

        inverted = self._get_inverse_name(
            self._get_whitespace_cleaned_name(result.get("name", ""))
        )

        for field in list(inverted.keys()):
            if field in fields_list:
                result[field] = inverted.get(field)

        return result

    @api.model
    def _names_order_default(self):
        return "first_last"

    @api.model
    def _get_names_order(self):
        """Get names order configuration from system parameters.
        You can override this method to read configuration from language,
        country, company or other"""
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("partner_names_order", self._names_order_default())
        )

    @api.model
    def _get_computed_name(self, lastname, firstname):
        """Compute the 'name' field according to splitted data.
        You can override this method to change the order of lastname and
        firstname the computed name"""
        order = self._get_names_order()
        if order == "last_first_comma":
            return ", ".join(p for p in (lastname, firstname) if p)
        elif order == "first_last":
            return " ".join(p for p in (firstname, lastname) if p)
        else:
            return " ".join(p for p in (lastname, firstname) if p)

    @api.depends("firstname", "lastname")
    def _compute_name(self):
        """Write the 'name' field according to splitted data."""
        for record in self:
            record.name = record._get_computed_name(record.lastname, record.firstname)

    def _inverse_name_after_cleaning_whitespace(self):
        """Clean whitespace in :attr:`~.name` and split it.

        The splitting logic is stored separately in :meth:`~._inverse_name`, so
        submodules can extend that method and get whitespace cleaning for free.
        """
        for record in self:
            # Remove unneeded whitespace
            clean = record._get_whitespace_cleaned_name(record.name)
            record.name = clean
            record._inverse_name()

    @api.model
    def _get_whitespace_cleaned_name(self, name, comma=False):
        """Remove redundant whitespace from :param:`name`.

        Removes leading, trailing and duplicated whitespace.
        """
        if isinstance(name, bytes):
            # With users coming from LDAP, name can be a byte encoded string.
            # This happens with FreeIPA for instance.
            name = name.decode("utf-8")

        try:
            name = " ".join(name.split()) if name else name
        except UnicodeDecodeError:
            # with users coming from LDAP, name can be a str encoded as utf-8
            # this happens with ActiveDirectory for instance, and in that case
            # we get a UnicodeDecodeError during the automatic ASCII -> Unicode
            # conversion that Python does for us.
            # In that case we need to manually decode the string to get a
            # proper unicode string.
            name = " ".join(name.decode("utf-8").split()) if name else name

        if comma:
            name = name.replace(" ,", ",")
            name = name.replace(", ", ",")
        return name

    @api.model
    def _get_inverse_name(self, name):
        """Compute the inverted name.

        - If the partner is a company, save it in the lastname.
        - Otherwise, make a guess.

        This method can be easily overriden by other submodules.
        You can also override this method to change the order of name's
        attributes

        When this method is called, :attr:`~.name` already has unified and
        trimmed whitespace.
        """
        # Company name goes to the lastname
        if not name:
            parts = [name or False, False]
        # Guess name splitting
        else:
            order = self._get_names_order()
            # Remove redundant spaces
            name = self._get_whitespace_cleaned_name(
                name, comma=(order == "last_first_comma")
            )
            parts = name.split("," if order == "last_first_comma" else " ", 1)
            if len(parts) > 1:
                if order == "first_last":
                    parts = [" ".join(parts[1:]), parts[0]]
                else:
                    parts = [parts[0], " ".join(parts[1:])]
            else:
                while len(parts) < 2:
                    parts.append(False)
        return {"lastname": parts[0], "firstname": parts[1]}

    def _inverse_name(self):
        """Try to revert the effect of :meth:`._compute_name`."""
        for record in self:
            parts = record._get_inverse_name(record.name)
            record.lastname = parts["lastname"]
            record.firstname = parts["firstname"]

    @api.constrains("firstname", "lastname")
    def _check_name(self):
        """Ensure at least one name is set."""
        for record in self:
            if all(
                    (
                            not (record.firstname or record.lastname),
                    )
            ):
                raise exceptions.EmptyNamesError(record)

    @api.model
    def _install_partner_firstname(self):
        """Save names correctly in the database.

        Before installing the module, field ``name`` contains all full names.
        When installing it, this method parses those names and saves them
        correctly into the database. This can be called later too if needed.
        """
        # Find records with empty firstname and lastname
        records = self.search([("firstname", "=", False), ("lastname", "=", False)])

        # Force calculations there
        records._inverse_name()
        _logger.info("%d partners updated installing module.", len(records))

    # Disabling SQL constraint givint a more explicit error using a Python
    # contstraint
    _sql_constraints = [("check_name", "CHECK( 1=1 )", "Contacts require a name.")]

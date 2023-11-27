import datetime
import logging

from . import zklib
from .zkconst import *
from struct import unpack
from odoo import api, fields, models
from odoo import _
from odoo.exceptions import UserError, ValidationError
import pytz

_logger = logging.getLogger(__name__)
try:
    from zk import ZK, const
except ImportError as ex:
    _logger.error("Please Install pyzk library.")


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Char(string='Biometric Device ID')


class ZkMachine(models.Model):
    _name = 'zk.machine'

    name = fields.Char(string='Machine IP', required=True)
    port_no = fields.Integer(string='Port No', required=True)
    address_id = fields.Many2one('res.partner', string='Working Address')
    company_id = fields.Many2one(
        'res.company', string='Company', default=lambda self: self.env.user.company_id.id)

    def device_connect(self, zk):
        try:
            conn = zk.connect()
            return conn
        except NameError:
            return False

    def clear_attendance(self):
        for info in self:
            try:
                machine_ip = info.name
                zk_port = info.port_no
                timeout = 30
                try:
                    zk = ZK(machine_ip, port=zk_port, timeout=timeout)
                except NameError as ex:
                    raise UserError(
                        _("Please install it with 'pip3 install pyzk'." .ex))
                conn = self.device_connect(zk)
                if conn:
                    conn.enable_device()
                    clear_data = zk.get_attendance()
                    if clear_data:
                        # conn.clear_attendance()
                        self._cr.execute(
                            """delete from zk_machine_attendance""")
                        conn.disconnect()
                        raise UserError(_('Attendance Records Deleted.'))
                    else:
                        raise UserError(
                            _('Unable to clear Attendance log. Are you sure attendance log is not empty.'))
                else:
                    raise UserError(
                        _('Unable to connect to Attendance Device. Please use Test Connection button to verify.'))
            except:
                raise ValidationError(
                    'Unable to clear Attendance log. Are you sure attendance device is connected & record is not empty.')

    def getSizeUser(self, zk):
        """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
        indicating that data packets are to be sent

        Returns the amount of bytes that are going to be sent"""
        command = unpack('HHHH', zk.data_recv[:8])[0]
        if command == CMD_PREPARE_DATA:
            size = unpack('I', zk.data_recv[8:12])[0]
            print("size", size)
            return size
        else:
            return False

    def zkgetuser(self, zk):
        """Start a connection with the time clock"""
        try:
            users = zk.get_users()
            print(users)
            return users
        except:
            return False

    @api.model
    def cron_download(self):
        machines = self.env['zk.machine'].search([])
        for machine in machines:
            machine.download_attendance()

    def download_attendance(self):
        _logger.info("++++++++++++Cron Executed++++++++++++++++++++++")
        zk_attendance = self.env['zk.machine.attendance']
        att_obj = self.env['hr.attendance']
        for info in self:
            machine_ip = info.name
            zk_port = info.port_no
            timeout = 15
            try:
                zk = ZK(machine_ip, port=zk_port, timeout=timeout, ommit_ping=True)
                # zk = ZK(machine_ip, port=zk_port, timeout=timeout,
                #         password=0, force_udp=False, ommit_ping=False)
            except NameError:
                raise UserError(
                    _("Pyzk module not Found. Please install it with 'pip3 install pyzk'."))
            conn = self.device_connect(zk)
            if conn:
                # conn.disable_device() #Device Cannot be used during this time.
                try:
                    user = conn.get_users()
                except:
                    user = False
                try:
                    attendance = conn.get_attendance()
                except:
                    attendance = False
                if attendance:
                    for each in attendance:
                        atten_time = each.timestamp
                        atten_time = datetime.strptime(atten_time.strftime(
                            '%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(atten_time, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        atten_time = datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        atten_time = fields.Datetime.to_string(atten_time)
                        if user:
                            for uid in user:
                                if uid.user_id == each.user_id:
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', each.user_id)])
                                    if get_user_id:
                                        duplicate_atten_ids = zk_attendance.search(
                                            [('device_id', '=', each.user_id), ('punching_time', '=', atten_time)])
                                        if duplicate_atten_ids:
                                            continue
                                        else:
                                            zk_attendance.create({'employee_id': get_user_id.id,
                                                                  'device_id': each.user_id,
                                                                  'attendance_type': str(each.status),
                                                                  'punch_type': str(each.punch),
                                                                  'punching_time': atten_time,
                                                                  'address_id': info.address_id.id})
                                            att_var = att_obj.search([('employee_id', '=', get_user_id.id),
                                                                      ('check_out', '=', False)])
                                            print('ddfcd', str(each.status))
                                            if each.punch == 0:  # check-in
                                                if not att_var:
                                                    att_obj.create({'employee_id': get_user_id.id,
                                                                    'check_in': atten_time})
                                            if each.punch == 1:  # check-out
                                                if len(att_var) == 1:
                                                    att_var.write(
                                                        {'check_out': atten_time})
                                                else:
                                                    att_var1 = att_obj.search(
                                                        [('employee_id', '=', get_user_id.id)])
                                                    if att_var1:
                                                        att_var1[-1].write(
                                                            {'check_out': atten_time})

                                    else:
                                        print('ddfcd', str(each.status))
                                        print('user', uid.name)
                                        employee = self.env['hr.employee'].create(
                                            {'device_id': each.user_id, 'name': uid.name})
                                        zk_attendance.create({'employee_id': employee.id,
                                                              'device_id': each.user_id,
                                                              'attendance_type': str(each.status),
                                                              'punch_type': str(each.punch),
                                                              'punching_time': atten_time,
                                                              'address_id': info.address_id.id})
                                        att_obj.create({'employee_id': employee.id,
                                                        'check_in': atten_time})
                                else:
                                    pass
                    # zk.enableDevice()
                    conn.disconnect
                    return True
                else:
                    raise UserError(
                        _('Unable to get the attendance log, please try again later.'))
            else:
                raise UserError(
                    _('Unable to connect, please check the parameters and network connections.'))

    def Try_connect(self): 
        for info in self:
            ip = info.name
            puerto = info.port_no
        conn = None
        zk = ZK(ip, port=puerto, timeout=5, ommit_ping=True)
        _logger.info(zk)
        try:
            _logger.info('Connecting to device ...')
            conn = zk.connect()
            _logger.info('Disabling device ...')
           
            conn.disable_device()
            _logger.info('Firmware Version: : {}'.format(conn.get_firmware_version()))
            # print '--- Get User ---'
            users = conn.get_users()
            for user in users:
                privilege = 'User'
                if user.privilege:
                    privilege = 'Admin'
                                                            
                _logger.info('- UID #{}'.format(user.uid))
                _logger.info('  Name       : {}'.format(user.name))
                _logger.info('  Privilege  : {}'.format(privilege))
                _logger.info('  Password   : {}'.format(user.password))
                _logger.info('  Group ID   : {}'.format(user.group_id))
                _logger.info('  User  ID   : {}'.format(user.user_id))
                _logger.info("Voice Test ...")
                
        
            conn.test_voice()
            _logger.info('Enabling device ...')
            conn.enable_device()
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('DONE'),
                'message': 'Connection Success',
                'type':'success', 
                'sticky': False, },}
            
        except Exception as ex:
            _logger.info(ex)
            return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('FAIL'),
                'message': f'Connection fail {ex}',
                'type':'danger', 
                'sticky': False, },}           
        finally:
            if conn:
                conn.disconnect()
        

        
        
 



 
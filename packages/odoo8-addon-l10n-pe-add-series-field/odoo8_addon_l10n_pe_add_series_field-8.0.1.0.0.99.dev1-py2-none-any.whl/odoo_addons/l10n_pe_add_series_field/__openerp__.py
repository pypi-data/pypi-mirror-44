# coding: utf-8
#
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2012 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
#
#    Coded by: Luis Ernesto García Medina (ernesto_gm@vauxoo.com)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

{
    'name': 'Printer Series Field in Journal',
    'version': '8.0.1.0.0',
    'category': 'Vauxoo',
    'depends': ['base', 'account'],
    'author': 'Vauxoo',
    'website': 'http://www.vauxoo.com',
    "license": 'AGPL-3',
    'data': [
        'view/account_journal_view.xml'
    ],
    'test': [
    ],
    'demo': [],
    'installable': True,
    'auto_install': False
}

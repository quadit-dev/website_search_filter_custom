# -*- coding: utf-8 -*-
# Copyright 2019 <Quadit S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale as controller  # noqa


class website_sale(controller):

    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',  # noqa
        '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''  # noqa
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):

        res = super(website_sale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)  # noqa
        return res

    def _get_search_domain(self, search, category, attrib_values):
        domain = request.website.sale_product_domain()
        if search:

            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', '|', '|', '|', '|', '|',
                    ('name', 'ilike', search),
                    ('barcode', '=', search),
                    ('description', 'ilike', search),
                    ('description_sale', 'ilike', search),
                    ('product_variant_ids.default_code', 'ilike', search),
                    ('product_variant_ids.autor', 'ilike', search),
                    ('product_variant_ids.editorial', 'ilike', search),
                    ('description', 'ilike', srch),
                    ('description_sale', 'ilike', srch),
                ]

        if category:
            domain += [('public_categ_ids', 'child_of', int(category))]

        if attrib_values:
            attrib = None
            ids = []
            for value in attrib_values:
                if not attrib:
                    attrib = value[0]
                    ids.append(value[1])
                elif value[0] == attrib:
                    ids.append(value[1])
                else:
                    domain += [('attribute_line_ids.value_ids', 'in', ids)]
                    attrib = value[0]
                    ids = [value[1]]
            if attrib:
                domain += [('attribute_line_ids.value_ids', 'in', ids)]
        return domain

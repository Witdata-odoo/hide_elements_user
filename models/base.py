from odoo import models, api
from lxml import etree

class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type='form', **options):
        key = super()._get_view_cache_key(view_id, view_type, **options)
        
        # --- ESCUDO DE SEGURIDAD (Auto-Bypass) ---
        # Verificamos directamente en PostgreSQL si la tabla relacional ya se creó.
        self.env.cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'hide_elements_rule_res_company_rel'")
        if not self.env.cr.fetchone():
            return key # Si no existe, salimos sin hacer nada para evitar la pantalla de error.
        # -----------------------------------------

        domain = [
            ('model_id.model', '=', self._name),
            '|', ('company_ids', '=', False), ('company_ids', 'in', self.env.company.id)
        ]
        has_rules = self.env['hide.elements.rule'].sudo().search_count(domain)
        
        if has_rules > 0:
            key = key + (f'user_{self.env.user.id}', f'company_{self.env.company.id}')
        return key

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)

        if self.env.is_superuser() or view_type != 'form':
            return res

        # --- ESCUDO DE SEGURIDAD (Auto-Bypass) ---
        self.env.cr.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'hide_elements_rule_res_company_rel'")
        if not self.env.cr.fetchone():
            return res
        # -----------------------------------------

        rules = self.env['hide.elements.rule'].sudo().search([
            ('model_id.model', '=', self._name),
            ('user_ids', 'in', self.env.user.id),
            '|', ('company_ids', '=', False), ('company_ids', 'in', self.env.company.id)
        ])

        if not rules:
            return res

        doc = etree.fromstring(res['arch'])
        xml_modified = False

        for rule in rules:
            if rule.restriction_type == 'readonly':
                doc.set('create', '0')
                doc.set('edit', '0')
                doc.set('delete', '0')
                
                for sheet in doc.xpath("//sheet"):
                    sheet.set('edit', '0')
                    sheet.set('create', '0')
                    
                for node in doc.xpath("//header/button"):
                     node.set('invisible', '1')
                    
                xml_modified = True
            
            elif rule.restriction_type == 'hide_button' and rule.element_name:
                for node in doc.xpath(f"//button[@name='{rule.element_name}']"):
                    if rule.condition:
                        old_invisible = node.get('invisible')
                        if old_invisible:
                            new_invisible = f"({old_invisible}) or ({rule.condition})"
                        else:
                            new_invisible = rule.condition
                        node.set('invisible', new_invisible)
                    else:
                        node.set('invisible', '1')
                    xml_modified = True

        if xml_modified:
            res['arch'] = etree.tostring(doc, encoding='unicode')

        return res
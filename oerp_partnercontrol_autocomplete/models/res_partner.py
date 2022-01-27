# -*- coding: utf-8 -*-
"""
@author: Online ERP Hungary Kft.
"""

from odoo import models, api

# SOAP Client
from zeep import Client
from zeep.helpers import serialize_object

import logging

_logger = logging.getLogger(__name__)

# BISNODE SOAP API URL
bisnode_soap_url = "https://www.cegminosites.hu/webservice/bs/BisnodeService.svc?wsdl"
BisnodeSOAPClient = Client(bisnode_soap_url)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, values):
        # Létrehozáskor ha csak egy üres szóköz van a website névnek akkor abban az esetben átálítja False-ra, ez azért
        # kellet mivel, ha üres lett volna akkor Undifend-ot írt volna ki, de így üresen marad
        if values.get("website") == " ":
            values["website"] = False
        return super(ResPartner, self).create(values)

    @api.model
    def autocomplete(self, query):
        """
        this is the original data returned by Odoo partner_autocomplete:
        query='i3 r'
        results=[
          {'city': 'Újlengyel', 'street': 'Petőfi Sándor Utca 48',
           'zip': '2724', 'bank_ids': [], 'country_code': 'HU',
           'name': 'I3 Rendszerház Informatikai Kereskedelmi És Szolgáltató Korlátolt Felelősségű Társaság',
           'vat': 'HU14933477', 'partner_gid': False, 'country_name': 'Hungary'
          },
        ]

        query='mol nyr'
        results={'Address': {'City': 'Budapest', 'Country': 'Magyarország', 'County': 'Budapest', 'StreetNo':
        'Október huszonharmadika u. 18.', 'Zip': '1117'}, 'Detail': "<span class='ui-state-highlight'>MOL</span>
        <span class='ui-state-highlight'>Nyrt</span>.", 'GroupTaxNumber': '17781774544', 'IsPartner': False,
        'LegalForm': 'Részvénytársaság', 'LegalFormCode': 55, 'MatchingType': 'Partial',
        'Name': 'MOL Magyar Olaj- és Gázipari Nyilvánosan Működő Részvénytársaság',
        'PcLink': 'http://www.partnercontrol.hu/mol_nyrt_49246.html?utm_medium=cegadatlap&utm_source=partnercontrol.hu-online-erp-hungary-kft&utm_campaign=webservice-integration',
         'ReasonType': 'Name', 'RegnNbr': '0110041683', 'ShortName': 'MOL Nyrt.', 'Status': 'Működő',
         'TaxNbr': '10625790444'
         }
        :param query:
        :type query:
        """

        res_country_tbl = self.env["res.country"].sudo()

        username = self.env["ir.config_parameter"].sudo().get_param("partnercontrol.username")
        password = self.env["ir.config_parameter"].sudo().get_param("partnercontrol.password")
        # serviceCd = self.env['ir.config_parameter'].sudo().get_param('bisnode_hun.serviceCd')

        use_long_name = self.env["ir.config_parameter"].sudo().get_param("partnercontrol.long_name", False)

        # if enabled the call of Odoo partner_autocomplete IAP, than call it
        def call_odoo():
            call_super = (
                self.env["ir.config_parameter"].sudo().get_param("partnercontrol.call_odoo_autocomplete", False)
            )
            if call_super:
                return super(ResPartner, self).autocomplete(query)
            else:
                return []

        if not (username and password):
            return call_odoo()

        result = BisnodeSOAPClient.service.QuickSearch(username, password, query, True)
        result = serialize_object(result)

        # Ha bármi jellegű hibá-ra futott akkor kiírjuk log-ba és meghíjuk az odoo-s autocomplete-t
        if result["ErrorMessage"]:
            _logger.info("Bisnode SOAP API Error: {0}".format(result["ErrorMessage"]))
            return call_odoo()

        # Ha nincsen találat akkor szintén meghívjuk az eredeti odoo-s autocompletet
        if not result["QuickSearchItems"]:
            return call_odoo()

        def get_hungary():
            """Visszadja magyarországot, mint ország"""
            return self.env.ref("base.hu").with_context(lang=self.env.user.lang)

        datas = []

        # Végigfutunk a találatokon
        for elem in result["QuickSearchItems"].get("QuickSearchItem", []):
            elem = dict(elem)
            if "Address" in elem:
                try:
                    elem["Address"] = dict(elem["Address"])
                except:
                    del elem["Address"]
            # Amennyiben a hosszú név be van pipálva akkor a hosszú nevet jeleníti meg
            name = elem.get("ShortName", "")
            if (use_long_name and elem.get("Name")) or not name:
                name = elem.get("Name", "")

            if not name:
                continue

            pchu_partner_id = False
            try:
                # Kiszedi a Bisnode azonososítót
                pchu_partner_id = int(elem.get("PcLink", "").split(".html")[0].split("_")[-1])
            except:
                pass

            # Beállítjuk az alapértelmezett értékeket az automatikusan kitöltendő adatok-nak, nehogy előforduljon olyan
            # , hogy az előző-t megtartja
            data = {
                "partner_gid": False,
                "pchu_partner_id": pchu_partner_id,
                "pchu_url": elem.get("PcLink", ""),
                "name": name,
                "bank_ids": [],
                "pchu_vip": elem.get("IsPartner", False),
                "vat": False,
                "zip": False,
                "country_id": False,
                "street": False,
                "city": False,
                "state_id": False,
                "website": " ",
            }

            # van magyar adószám modul feltelepítve?
            has_hungary_invoice = self.env["ir.model.fields"].search(
                [
                    ("model_id.model", "=", "res.partner"),
                    ("name", "=", "vat_hu"),
                ]
            )

            if has_hungary_invoice:
                data.update(
                    {
                        "l10n_hu_is_group_member_vat": False,
                        "l10n_hu_group_member_vat": False,
                        "company_registry": False,
                    }
                )

            # Kiszedi a hosszú nevét a válalatnak
            # if not use_long_name and has_hungary_invoice:
            #     data["long_name"] = elem.get("Name", False)

            # Kiszedi a válalat registrációs számát
            RegnNbr = elem.get("RegnNbr", None)
            if RegnNbr and has_hungary_invoice:
                data["company_registry"] = "{0}-{1}-{2}".format(RegnNbr[:2], RegnNbr[2:4], RegnNbr[4:])

            # csoporttag adószám
            hun_group_vat = False

            # adószám
            vat_hu = elem.get("TaxNbr", None)

            # Amennyiben van csoportos adószám és azt a adószám mező használja akkor beállítja a csoportos adószám
            # mezőt az adószámra
            if has_hungary_invoice and vat_hu:
                hun_group_vat = elem.get("GroupTaxNumber", None)

            # Beállítja a csoportos adószámot
            if hun_group_vat:
                data.update(
                    {
                        "l10n_hu_is_group_member_vat": True,
                        "l10n_hu_group_member_vat": "{0}-{1}-{2}".format(
                            hun_group_vat[:8], hun_group_vat[8:9], hun_group_vat[9:11]
                        ),
                    }
                )

            if vat_hu:
                if has_hungary_invoice:
                    # Magyar számlázás esetén a magar adószámba kerül
                    data["vat_hu"] = "{0}-{1}-{2}".format(vat_hu[:8], vat_hu[8:9], vat_hu[9:11])
                else:
                    # Nem magyar számlázás esetén pedig a sima adószám mezőbe
                    data["vat"] = "HU{0}".format(vat_hu[:8])

            if "Address" in elem:
                address = elem["Address"]
                # Az irányítószámot kiveszi
                if address.get("Zip", False):
                    data["zip"] = address["Zip"]
                if address.get("Country", False):
                    # ha fixen ez a neve, akkor ne keressünk
                    country = None
                    if address["Country"] == "Magyarország":
                        country = get_hungary()
                    if not country:
                        # Kikeresi az országot
                        country = res_country_tbl.search([("name", "=", address["Country"])], limit=1)

                    if country:
                        # Majd pedig a felhasználó által beálított nyelven megjeleníti a lekérdezett országot
                        country = country.with_context(lang=self.env.user.lang)
                        data["country_id"] = {"id": country.id, "display_name": country.display_name}

                # Ha nem kaptunk vissza országot, de az adatok arra utalnak, hogy magyar a válalat akkor berakja az
                # országot Magyarországra
                elif data["zip"] and len(data["zip"]) == 4 and data.get("vat_hu"):
                    country = get_hungary()
                    data["country_id"] = {"id": country.id, "display_name": country.display_name}

                # Itt rakja be az utcá-t
                if address.get("StreetNo", False):
                    data["street"] = address["StreetNo"]

                # Itt rakja be a várost
                if address.get("City", False):
                    data["city"] = address["City"]

                city_available = False
                try:
                    city_zip_tbl = self.env["res.country.state"]
                    city_tbl = self.env["res.city"]
                    city_available = "zip"
                except KeyError:
                    try:
                        city_tbl = self.env["res.city"]
                        city_available = "city"
                    except KeyError:
                        pass

                # Összerak egy keresést amely segítségével visszakaphatjukaz országot a város és az irányítószám
                # alapján
                if city_available == "zip":

                    s = []
                    if "zip" in data:
                        s.append(("city_ids.zipcode", "=", data["zip"]))
                    if "city" in data:
                        s.append(("city_ids.name", "=", data["city"]))

                    # _logger.info('search={0}'.format(s))

                    city = city_zip_tbl.search(s, limit=1)
                    # _logger.info('city={0}'.format(city))

                    # Ha talált egy várost amely a paramétereknek megfelel akkor abban az esetben behelyezi a
                    # hozzá rendelt országot
                    if city:
                        if city.country_id and not data.get("country_id"):
                            data["country_id"] = {
                                "id": city.country_id.id,
                                "display_name": city.country_id.display_name,
                            }
                        if city and not data.get("state_id"):
                            data["state_id"] = {"id": city.id, "display_name": city.display_name}

                # Itt kikeresi az államot is, ha persze van olyan találat, illetve, ha nincsen még ország
                # kiválasztva akkor azt is megpróbálja más úton kikeresni
                s = []
                if "zip" in data:
                    s.append(("zipcode", "=ilike", data["zip"]))
                if "city" in data:
                    s.append(("name", "=ilike", data["city"]))

                # _logger.info('search2={0}'.format(s))

                city = city_tbl.search(s, limit=1)
                # _logger.info('city2={0}'.format(city))
                if city:
                    if city.country_id and not data.get("country_id"):
                        data["country_id"] = {"id": city.country_id.id, "display_name": city.country_id.display_name}
                    if city.state_id and not data.get("state_id"):
                        data["state_id"] = {
                            "id": city.city.state_id.id,
                            "display_name": city.city.state_id.display_name,
                        }
                if not data.get("country_id") and elem.get("Address").get("Country") == "Magyarország":
                    country = get_hungary()
                    data["country_id"] = {"id": country.id, "display_name": country.display_name}

            if data:
                datas.append(data)

        if datas:
            return datas
        else:
            return call_odoo()

    @api.model
    def read_by_vat(self, vat):
        # is it ok to call Odoo partner_autocomplete IAP function?
        call_super = self.env["ir.config_parameter"].sudo().get_param("partnercontrol.call_odoo_autocomplete", False)
        # if yes, than use Bisnode only for Hungary, else use Odoo
        if call_super:
            # hungarian formats: HU12345678, 12345678901, 12345678-9-01
            if vat[:2].upper() == "HU":
                return self.autocomplete(vat[2:])
            elif len(vat) == 11:
                return self.autocomplete(vat)
            elif len(vat) == 13 and vat.count("-") == 2:
                return self.autocomplete(vat)
            else:
                return super(ResPartner, self).read_by_vat(vat)

        # only use Bisnode
        else:
            if vat[:2].upper() == "HU":
                return self.autocomplete(vat[2:])
            else:
                return self.autocomplete(vat)

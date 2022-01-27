# -*- coding: utf-8 -*-
"""
@author: Online ERP Hungary Kft.
"""


bisnode_url = 'https://www.cegminosites.hu/webservice/bs/BisnodeService.svc?wsdl'
userName = 'i3-rendszerhaz-kft'
password = '3o5htidFs3'

from zeep import Client
import datetime


client = Client(bisnode_url)

# gyors keresés
# QuickSearchResult QuickSearch(string userName, string password, string query, bool onlyActive)
query = 'i3 re'
onlyActive = True
result = client.service.QuickSearch(userName, password, query, onlyActive)

res = {
    'ErrorMessage': None,
    'QuickSearchItems': {
        'QuickSearchItem': [
            {
                'Address': {
                    'City': 'Újlengyel',
                    'Country': None,
                    'StreetNo': 'Petőfi Sándor utca 48.',
                    'Zip': '2724'
                },
                'Detail': "<span class='ui-state-highlight'>i3</span> <span class='ui-state-highlight'>Rendszerház</span> Kft.",
                'GroupTaxNumber': None,
                'IsPartner': False,
                'MatchingType': 'Partial',
                'Name': 'i3 Rendszerház Informatikai Kereskedelmi és Szolgáltató Korlátolt Felelősségű Társaság',
                'PcLink': 'http://www.partnercontrol.hu/i3_rendszerhaz_kft_4385773.html?utm_medium=cegadatlap&utm_source=partnercontrol.hu-i3-rendszerhaz-kft&utm_campaign=webservice-integration',
                'ReasonType': 'Name',
                'RegnNbr': '1309169888',
                'ShortName': 'i3 Rendszerház Kft.',
                'Status': 'Működő',
                'TaxNbr': '14933477213'
            },
            {
                'Address': {
                    'City': 'Szirmabesenyő',
                    'Country': None,
                    'StreetNo': 'Rákóczi u. 39.',
                    'Zip': '3711'
                },
                'Detail': "<span class='ui-state-highlight'>RE</span>-LAX <span class='ui-state-highlight'>93</span>. Bt.",
                'GroupTaxNumber': None,
                'IsPartner': False,
                'MatchingType': 'Partial',
                'Name': 'RE-LAX 93. Árnyékolástechnikai Betéti Társaság',
                'PcLink': 'http://www.partnercontrol.hu/relax_93_bt_159799.html?utm_medium=cegadatlap&utm_source=partnercontrol.hu-i3-rendszerhaz-kft&utm_campaign=webservice-integration',
                'ReasonType': 'Name',
                'RegnNbr': '0506003803',
                'ShortName': 'RE-LAX 93. Bt.',
                'Status': 'Működő',
                'TaxNbr': '21281284205'
            },
        ]
    }
}

# részletes adatok
# BisnodeResponse GetBisnodeResponse(string userName, string password, string taxnbr, int serviceCd)
serviceCd = 367
taxnbr = '14933477213'
#taxnbr = '14735808243'
#result = client.service.GetBisnodeResponse(userName, password, taxnbr, serviceCd)

res = {
    'Activity': None,
    'AdditionalInformation': None,
    'AnnualReport': None,
    'AuthorizedSignatories': {
        'Person': [
            {
                'Address': {
                    'City': 'Salgótarján',
                    'Country': 'Magyarország',
                    'StreetNo': 'Pécskő út 12/A. III. em. 25.',
                    'Zip': '3100'
                },
                'MotherName': 'Zsuffa Ibolya Zsuzsanna',
                'Name': 'Tóth Csaba',
                'OperativeDate': datetime.datetime(2014, 3, 11, 0, 0),
                'OwnerPercentageInterval': None,
                'OwnerPercentageNumber': 0.0,
                'OwnerType': 10346,
                'RegDate': datetime.datetime(2014, 4, 2, 0, 0),
                'RelationShipEndDate': None,
                'RelationShipStartDate': datetime.datetime(2009, 10, 1, 0, 0),
                'RepresentationTypeDescr': 'önálló',
                'TaxNumber': '8419380326',
                'TypeDescr': 'Ügyvezető (vezető tisztségviselő)'
            }
        ]
    },
    'AveragePaymentTermDays': None,
    'BCRReport': None,
    'Banks': {
        'Bank': [
            {
                'Account': '117090402000126100000000',
                'HqGiroCode': '117',
                'HqName': 'OTP Bank Nyrt.',
                'Name': 'OTP Budapesti r., VIII. József krt.',
                'StartDate': datetime.datetime(2015, 7, 13, 0, 0)
            }
        ]
    },
    'BeneficialOwners': None,
    'BisnodeCertificate': None,
    'BisnodeRating': None,
    'BisnodeRatingFromZeroToTen': None,
    'BmhPublicOrderFine': None,
    'Capital': {
        'Amount': 3000000.0,
        'Currency': 'HUF'
    },
    'CompAuditors': None,
    'CompOwners': None,
    'CompanyInformationExtract': None,
    'CompanyInformationHistory': None,
    'DBFinancialStrength': None,
    'DBLOB': None,
    'DBMaxCreditLimit': None,
    'DBNetWorth': None,
    'DBRiskIndicator': None,
    'DetailedLglEvents': None,
    'DetailedPremises': None,
    'DetailedRegAddress': None,
    'DomesticFamilyTreeId': None,
    'DunsNumber': None,
    'EbhSettledLabourRelationsInfringement': None,
    'Email': None,
    'Employee': '0',
    'Employees': None,
    'Errors': None,
    'EstabDate': None,
    'EuTaxNbr': 'HU14933477',
    'FinancialDataInterval': {
        'FinancialStatementIntervalRow': [
            {
                'Amount': 2315000.0,
                'Code': 9853,
                'Descr': 'E. Adózás előtti eredmény (+C+D)',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 20232000.0,
                'Code': 9807,
                'Descr': 'I. Értékesítés nettó árbevétele (01+02)',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 2148000.0,
                'Code': 9856,
                'Descr': 'F. Adózott eredmény (+E-XII)',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 1803000.0,
                'Code': 9753,
                'Descr': 'D. Saját tőke',
                'From': datetime.datetime(2015, 1, 1, 0, 0),
                'To': datetime.datetime(2015, 12, 31, 0, 0)
            },
            {
                'Amount': 3951000.0,
                'Code': 9753,
                'Descr': 'D. Saját tőke',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 19227000.0,
                'Code': 9807,
                'Descr': 'I. Értékesítés nettó árbevétele (01+02)',
                'From': datetime.datetime(2015, 1, 1, 0, 0),
                'To': datetime.datetime(2015, 12, 31, 0, 0)
            },
            {
                'Amount': 732000.0,
                'Code': 9853,
                'Descr': 'E. Adózás előtti eredmény (+C+D)',
                'From': datetime.datetime(2015, 1, 1, 0, 0),
                'To': datetime.datetime(2015, 12, 31, 0, 0)
            },
            {
                'Amount': 659000.0,
                'Code': 9856,
                'Descr': 'F. Adózott eredmény (+E-XII)',
                'From': datetime.datetime(2015, 1, 1, 0, 0),
                'To': datetime.datetime(2015, 12, 31, 0, 0)
            }
        ]
    },
    'FinancialStatement': None,
    'FullTaxNbr': '14933477213',
    'FunctionalLeaders': None,
    'GFOCode': None,
    'GroupTaxNumber': None,
    'InterestCount': None,
    'Interests': None,
    'IsMonitored': None,
    'IsPartner': False,
    'KshNbr': None,
    'LastModificationDate': None,
    'Leaders': None,
    'LegalForm': None,
    'LglEventStatus': True,
    'LglEvents': {
        'LglEvent': [
            {
                'Code': 'AP3',
                'Date': datetime.datetime(2016, 2, 22, 0, 0),
                'Descr': 'NAV - Végrehajtási határozat'
            },
            {
                'Code': 'BV1',
                'Date': datetime.datetime(2014, 9, 16, 0, 0),
                'Descr': 'Bírósági végrehajtás'
            }
        ]
    },
    'Liquidators': None,
    'MainInds': {
        'Date': datetime.datetime(2013, 2, 21, 0, 0),
        'Descr': 'Egyéb információ-technológiai szolgáltatás',
        'Teaor': '6209',
        'Type': '2008'
    },
    'MaxCrAmt': None,
    'NavSettledLabourRelationsInfringement': None,
    'OmmfSettledLabourRelationsInfringement': None,
    'OneStepCompanyConnections': None,
    'OptionalFields': None,
    'OtherConnections': None,
    'OwnerCount': None,
    'PaymentIndex': None,
    'PaymentIndexZeroToTen': None,
    'PcFinancial': None,
    'PcLink': 'http://www.partnercontrol.hu/i3_rendszerhaz_kft_4385773.html?utm_medium=cegadatlap&utm_source=partnercontrol.hu-i3-rendszerhaz-kft&utm_campaign=webservice-integration',
    'PcRatios': {
        'PcRatio': [
            {
                'Amount': 169.27,
                'Descr': 'Eladósodottság mértéke',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 10.61,
                'Descr': 'Árbevételarányos adózott eredmény',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            },
            {
                'Amount': 1.7629,
                'Descr': 'Likviditási ráta',
                'From': datetime.datetime(2016, 1, 1, 0, 0),
                'To': datetime.datetime(2016, 12, 31, 0, 0)
            }
        ]
    },
    'PersAuditors': None,
    'PersOwners': None,
    'PosEvents': None,
    'PrLink': None,
    'PreQualifyingData': {
        'PreQualifyingReason': 'Red',
        'PreQualifyingResult': 'R'
    },
    'Predecessors': None,
    'Premises': None,
    'PremisesCount': None,
    'PublicDebtFree': None,
    'RegAddress': {
        'City': 'Újlengyel',
        'Country': 'Magyarország',
        'StreetNo': 'Petőfi Sándor utca 48.',
        'Zip': '2724'
    },
    'RegDate': '2009. 10. 09.',
    'RegName': 'i3 Rendszerház Informatikai Kereskedelmi és Szolgáltató Korlátolt Felelősségű Társaság',
    'RegisteredEmail': None,
    'RegnNbr': '1309169888',
    'ResponseDate': datetime.datetime(2019, 5, 11, 1, 13, 56, 467982), # tzinfo=<FixedOffset '+02:00'>
    'ResultFound': 1,
    'ShortName': 'i3 Rendszerház Kft.',
    'StatementToDate': datetime.datetime(2016, 12, 31, 0, 0),
    'Status': 'Működő',
    'TEAORS': None,
    'TaxNumber': '14933477213',
    'TaxNumberHistories': None,
    'TelNumbers': None,
    'TradeExperience': None,
    'TradeModel': None,
    'TrafficLight': None,
    'Username': 'i3-rendszerhaz-kft',
    'Web': None
}



# fogyasztás lekérése
# GetCreditResponse GetCredit(string username, string password)
#result = client.service.GetCredit(userName, password)




## partner kezelés

# lekérés
#result = client.service.GetPartnerList(userName, password)

# hozzáadás
#result = client.service.AddPartner(userName, password)

# törlés
#result = client.service.RemovePartner(userName, password)





#assert result == 62.137
print(result)

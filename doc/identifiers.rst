Common Features
===============

.. module:: identifiers

.. autoclass:: Identifier
    :members: __copy__, __deepcopy__, __hash__, __repr__, __str__

Identifiers standardized by GS1
===============================

.. autoclass:: GLN
    :members: gs1_prefix, company_prefix, location_reference, check_digit,
        elements, separated

.. autoclass:: GTIN12
    :members: gs1_prefix, company_prefix, item_reference, check_digit,
        elements, separated

.. autoclass:: GTIN13
    :members: gs1_prefix, company_prefix, item_reference, check_digit,
        elements, separated

.. autoclass:: GTIN14
    :members: level_indicator, gs1_prefix, company_prefix, item_reference,
        check_digit, elements, separated

.. autoclass:: GSIN
    :members: gs1_prefix, company_prefix, shipper_reference, check_digit,
        elements, separated

.. autoclass:: SSCC
    :members: extension_digit, gs1_prefix, company_prefix, serial_reference,
        check_digit, elements, separated

Identifiers for publications
============================

.. autoclass:: ISBN
    :members: gs1_prefix, registration_group, registrant, publication,
        check_digit, elements, separated

.. autoclass:: ISMN
    :members: gs1_prefix, registration_group, registrant, publication,
        check_digit, elements, separated

.. autoclass:: ISSN
    :members: check_digit, raw_number, as_gtin, separated

.. not exposed in package so far, should it be?
    .. autoclass:: ISSN13
        :members: gs1_prefix, company_prefix, item_reference, check_digit,
            elements, separated, extract_issn

Identifiers for banks and bank accounts
=======================================

.. autoclass:: BIC
    :members: party_prefix, country_code, party_suffix, branch_code,
        elements

.. autoclass:: IBAN
    :members: country_code, check_digits, bank_identifier,
        bank_account_number, elements

Identifiers for exchanges and exchange traded financial assets
==============================================================

.. autoclass:: MIC

.. autoclass:: ISIN
    :members: country_code, nsin, check_digit, elements

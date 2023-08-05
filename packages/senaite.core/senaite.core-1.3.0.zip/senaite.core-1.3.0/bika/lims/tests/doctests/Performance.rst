Performance tests to keep times under control
=============================================

Running this test from the buildout directory:

    bin/test test_textual_doctests -t Performance


Test Setup
----------

Needed Imports:

    >>> import time
    >>> import transaction
    >>> from bika.lims import api
    >>> from bika.lims.utils import tmpID
    >>> from bika.lims.utils.analysisrequest import create_analysisrequest
    >>> from DateTime import DateTime
    >>> from plone.app.testing import setRoles
    >>> from plone.app.testing import TEST_USER_ID
    >>> from plone.app.testing import TEST_USER_PASSWORD

Variables:

    >>> portal = self.portal
    >>> request = self.request
    >>> bikasetup = portal.bika_setup
    >>> date_now = DateTime().strftime("%Y-%m-%d")

We need to create some basic objects for the test:

    >>> setRoles(portal, TEST_USER_ID, ['LabManager',])
    >>> client = api.create(portal.clients, "Client", Name="Happy Hills", ClientID="HH", MemberDiscountApplies=True)
    >>> contact = api.create(client, "Contact", Firstname="Rita", Lastname="Mohale")
    >>> sampletype = api.create(bikasetup.bika_sampletypes, "SampleType", title="Water", Prefix="W")
    >>> labcontact = api.create(bikasetup.bika_labcontacts, "LabContact", Firstname="Lab", Lastname="Manager")
    >>> department = api.create(bikasetup.bika_departments, "Department", title="Chemistry", Manager=labcontact)
    >>> category = api.create(bikasetup.bika_analysiscategories, "AnalysisCategory", title="Metals", Department=department)

Functional Helpers:

    >>> def create_services(num_services):
    ...     services = list()
    ...     for i in range(num_services):
    ...         service = api.create(bikasetup.bika_analysisservices,
    ...                    "AnalysisService", title="Test-{}".format(tmpID()),
    ...                    Keyword="Test-{}".format(tmpID()), Price="15",
    ...                    Category=category.UID(), Accredited=False)
    ...         services.append(service)
    ...     return services

    >>> def create_ar(services):
    ...     values = {'Client': client.UID(),
    ...               'Contact': contact.UID(),
    ...               'DateSampled': date_now,
    ...               'SampleType': sampletype.UID()}
    ...     return create_analysisrequest(client, request, values, services)


Analysis Request creation time
------------------------------

Define limits:

    >>> NUM_ANALYSIS_REQUESTS = 5
    >>> NUM_ANALYSES_PER_REQUEST = 50
    >>> MAX_SECONDS_PER_AR = 5

And required initial objects:

    >>> services = create_services(NUM_ANALYSES_PER_REQUEST)

Create an Analysis Request:

    >>> sec_start = time.time()
    >>> for i in range(NUM_ANALYSIS_REQUESTS):
    ...     ar = create_ar(services)
    >>> transaction.commit()
    >>> delta = (time.time()-sec_start)/float(NUM_ANALYSIS_REQUESTS)
    >>> delta < MAX_SECONDS_PER_AR
    True

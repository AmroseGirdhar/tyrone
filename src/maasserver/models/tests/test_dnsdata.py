# Copyright 2015-2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Tests for the DNSData model."""

__all__ = []


import random
import re

from django.core.exceptions import (
    PermissionDenied,
    ValidationError,
)
from maasserver.enum import NODE_PERMISSION
from maasserver.models.config import Config
from maasserver.models.dnsdata import (
    DNSData,
    HostnameRRsetMapping,
)
from maasserver.models.domain import Domain
from maasserver.models.node import Node
from maasserver.testing.factory import factory
from maasserver.testing.testcase import MAASServerTestCase
from testtools import ExpectedException

# duplicated from dnsdata.py so as to not export them
INVALID_CNAME_MSG = "Invalid CNAME: Should be '<server>'."
INVALID_MX_MSG = (
    "Invalid MX: Should be '<preference> <server>'."
    " Range for preference is 0-65535.")
INVALID_SRV_MSG = (
    "Invalid SRV: Should be '<priority> <weight> <port> <server>'."
    " Range for priority, weight, and port are 0-65536.")
CNAME_AND_OTHER_MSG = (
    "CNAME records for a name cannot coexist with non-CNAME records.")
MULTI_CNAME_MSG = "Only one CNAME can be associated with a name."


class TestDNSDataManagerGetDNSDataOr404(MAASServerTestCase):

    def test__user_view_returns_dnsdata(self):
        user = factory.make_User()
        dnsdata = factory.make_DNSData()
        self.assertEqual(
            dnsdata,
            DNSData.objects.get_dnsdata_or_404(
                dnsdata.id, user, NODE_PERMISSION.VIEW))

    def test__user_edit_raises_PermissionError(self):
        user = factory.make_User()
        dnsdata = factory.make_DNSData()
        self.assertRaises(
            PermissionDenied,
            DNSData.objects.get_dnsdata_or_404,
            dnsdata.id, user, NODE_PERMISSION.EDIT)

    def test__user_admin_raises_PermissionError(self):
        user = factory.make_User()
        dnsdata = factory.make_DNSData()
        self.assertRaises(
            PermissionDenied,
            DNSData.objects.get_dnsdata_or_404,
            dnsdata.id, user, NODE_PERMISSION.ADMIN)

    def test__admin_view_returns_dnsdata(self):
        admin = factory.make_admin()
        dnsdata = factory.make_DNSData()
        self.assertEqual(
            dnsdata,
            DNSData.objects.get_dnsdata_or_404(
                dnsdata.id, admin, NODE_PERMISSION.VIEW))

    def test__admin_edit_returns_dnsdata(self):
        admin = factory.make_admin()
        dnsdata = factory.make_DNSData()
        self.assertEqual(
            dnsdata,
            DNSData.objects.get_dnsdata_or_404(
                dnsdata.id, admin, NODE_PERMISSION.EDIT))

    def test__admin_admin_returns_dnsdata(self):
        admin = factory.make_admin()
        dnsdata = factory.make_DNSData()
        self.assertEqual(
            dnsdata,
            DNSData.objects.get_dnsdata_or_404(
                dnsdata.id, admin, NODE_PERMISSION.ADMIN))


class DNSDataTest(MAASServerTestCase):

    def test_creates_dnsdata(self):
        name = factory.make_name('name')
        domain = factory.make_Domain()
        dnsdata = factory.make_DNSData(name=name, domain=domain)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.dnsresource.name, from_db.id),
            (name, dnsdata.id))

    # The following tests intentionally pass in a lowercase rrtype,
    # which will be upshifted in the creation of the DNSData record.
    def test_creates_cname(self):
        name = factory.make_name('name')
        dnsdata = factory.make_DNSData(rrtype='cname', name=name)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.id, from_db.rrtype),
            (dnsdata.id, 'CNAME'))

    def test_creates_cname_with_underscore(self):
        name = factory.make_name('na_me')
        dnsdata = factory.make_DNSData(rrtype='cname', name=name)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.id, from_db.rrtype),
            (dnsdata.id, 'CNAME'))

    def test_rejects_bad_cname_target(self):
        target = factory.make_name('na*e')
        dnsresource = factory.make_DNSResource(no_ip_addresses=True)
        dnsdata = DNSData(
            dnsresource=dnsresource,
            rrtype='CNAME', rrdata=target)
        with ExpectedException(
                ValidationError,
                re.escape(
                    "{'__all__': [\"%s\"]}" % INVALID_CNAME_MSG)):
            dnsdata.save()

    def test_creates_mx(self):
        name = factory.make_name('name')
        dnsdata = factory.make_DNSData(rrtype='mx', name=name)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.id, from_db.rrtype),
            (dnsdata.id, 'MX'))

    def test_creates_ns(self):
        name = factory.make_name('name')
        dnsdata = factory.make_DNSData(rrtype='ns', name=name)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.id, from_db.rrtype),
            (dnsdata.id, 'NS'))

    def test_creates_srv(self):
        service = factory.make_name(size=5)
        proto = factory.make_name(size=5)
        name = factory.make_name('name')
        target = factory.make_name('name')
        srv_name = '_%s._%s.%s' % (service, proto, name)
        data = "%d %d %d %s" % (
            random.randint(0, 65535),
            random.randint(0, 65535),
            random.randint(1, 65535),
            target)
        dnsdata = factory.make_DNSData(
            rrtype='srv', rrdata=data, name=srv_name)
        from_db = DNSData.objects.get(dnsresource__name=srv_name)
        self.assertEqual((
            from_db.dnsresource.name, from_db.id,
            from_db.rrtype, from_db.rrdata),
            (srv_name, dnsdata.id, 'SRV', data))

    def test_creates_txt(self):
        name = factory.make_name('name')
        dnsdata = factory.make_DNSData(rrtype='txt', name=name)
        from_db = DNSData.objects.get(dnsresource__name=name)
        self.assertEqual(
            (from_db.id, from_db.rrtype),
            (dnsdata.id, 'TXT'))

    def test_rejects_cname_with_address(self):
        name = factory.make_name('name')
        target = factory.make_name('target')
        domain = factory.make_Domain()
        dnsrr = factory.make_DNSResource(name=name, domain=domain)
        dnsrr.save()
        dnsdata = DNSData(
            dnsresource=dnsrr,
            rrtype='CNAME',
            rrdata=target)
        with ExpectedException(
                ValidationError,
                re.escape(
                    "{'__all__': ['%s']}" % CNAME_AND_OTHER_MSG)):
            dnsdata.save()

    def test_rejects_cname_with_other_data(self):
        name = factory.make_name('name')
        target = factory.make_name('target')
        domain = factory.make_Domain()
        rrtype = random.choice(['MX', 'NS', 'TXT'])
        dnsrr = factory.make_DNSData(
            name=name, domain=domain,
            no_ip_addresses=True, rrtype=rrtype).dnsresource
        dnsdata = DNSData(
            dnsresource=dnsrr, rrtype='CNAME', rrdata=target)
        with ExpectedException(
                ValidationError,
                re.escape(
                    "{'__all__': ['%s']}" % CNAME_AND_OTHER_MSG)):
            dnsdata.save()

    def test_allows_multiple_records_unless_cname(self):
        dnsdata = factory.make_DNSData(no_ip_addresses=True)
        if dnsdata.rrtype == 'CNAME':
            with ExpectedException(
                    ValidationError,
                    re.escape(
                        "{'__all__': ['%s']}" % MULTI_CNAME_MSG)):
                factory.make_DNSData(
                    dnsresource=dnsdata.dnsresource,
                    rrtype='CNAME')
        else:
            factory.make_DNSData(
                dnsresource=dnsdata.dnsresource,
                rrtype=dnsdata.rrtype)
            self.assertEqual(2, DNSData.objects.filter(
                dnsresource=dnsdata.dnsresource).count())


class TestDNSDataMapping(MAASServerTestCase):
    """Tests for get_hostname_dnsdata_mapping()."""

    def make_mapping(self, dnsresource):
        nodes = Node.objects.filter(
            hostname=dnsresource.name, domain=dnsresource.domain)
        if nodes.count() > 0:
            system_id = nodes.first().system_id
        else:
            system_id = None
        mapping = HostnameRRsetMapping(system_id)
        for data in dnsresource.dnsdata_set.all():
            if data.ttl is not None:
                ttl = data.ttl
            elif dnsresource.domain.ttl is not None:
                ttl = dnsresource.domain.ttl
            else:
                ttl = Config.objects.get_config('default_dns_ttl')
            mapping.rrset.add((ttl, data.rrtype, data.rrdata))
        return {dnsresource.name: mapping}

    def test_get_hostname_dnsdata_mapping_returns_mapping(self):
        domain = Domain.objects.get_default_domain()
        expected_mapping = {}
        # Create 3 labels with 0-5 resources each, verify that they
        # Come back correctly.
        for _ in range(3):
            name = factory.make_name('label')
            dnsrr = factory.make_DNSResource(
                name=name, domain=domain, no_ip_addresses=True)
            for count in range(random.randint(1, 5)):
                data = factory.make_DNSData(
                    dnsresource=dnsrr, ip_addresses=True)
            expected_mapping.update(self.make_mapping(data.dnsresource))
        # Add one resource to the domain which has no data, so it should not be
        # in the returned mapping.
        factory.make_DNSResource(domain=domain, no_ip_addresses=True)
        actual = DNSData.objects.get_hostname_dnsdata_mapping(domain)
        self.assertItemsEqual(expected_mapping, actual)

    def test_get_hostname_dnsdata_mapping_handles_ttl(self):
        # We create 2 domains, one with a ttl, one withoout.
        # Within each domain, create an RRset with and without ttl.
        global_ttl = random.randint(1, 99)
        Config.objects.set_config('default_dns_ttl', global_ttl)
        domains = [
            factory.make_Domain(),
            factory.make_Domain(ttl=random.randint(100, 199))]
        for dom in domains:
            factory.make_DNSData(domain=dom)
            factory.make_DNSData(domain=dom, ttl=random.randint(200, 299))
            expected_mapping = {}
            for dnsrr in dom.dnsresource_set.all():
                expected_mapping.update(self.make_mapping(dnsrr))
            actual = DNSData.objects.get_hostname_dnsdata_mapping(dom)
            self.assertItemsEqual(expected_mapping, actual)

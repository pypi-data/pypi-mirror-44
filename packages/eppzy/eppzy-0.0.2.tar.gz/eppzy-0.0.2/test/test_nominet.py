from eppzy.nominet import NContact
from eppzy.session import RequestWrapper

from test_contact import data_file_contents, MockTransport


def test_ncontact_create():
    def checks(body):
        assert b'traddie' in body
        return data_file_contents('rfc5733/contact_create_example.xml')
    mt = MockTransport(checks)
    nc = RequestWrapper(NContact.wrap(NContact.base)(mt))
    nc.create(
        'cid', 'nam', 'org', ['street'], 'city', 'sop', 'RC32 NFQ', 'GB',
        '+44.382919', 'fax', 'bob@bob.bob', '', trad_name='traddie')


def test_ncontact_info():
    def checks(body):
        assert b'info' in body
        assert b'mrbill' in body
        return data_file_contents('nominet/contact_info_example.xml')
    mt = MockTransport(checks)
    nc = RequestWrapper(NContact.wrap(NContact.base)(mt))
    r = nc.info('mrbill', 'passy')
    assert r.data['trad_name'] == 'Big enterprises'
    assert r.data['org'] == 'Company.'

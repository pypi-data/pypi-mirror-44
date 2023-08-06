from eppzy.nominet import NContact
from eppzy.session import RequestWrapper
from util import data_file_contents, mocked_session


def test_ncontact_create():
    def checks(body):
        assert b'traddie' in body
        return data_file_contents('rfc5733/contact_create_example.xml')
    with mocked_session(checks, [NContact.base], [NContact]) as s:
        s['contact'].create(
            'cid', 'nam', 'org', ['street'], 'city', 'sop', 'RC32 NFQ', 'GB',
            '+44.382919', 'fax', 'bob@bob.bob', '', trad_name='traddie')


def test_ncontact_info():
    def checks(body):
        assert b'info' in body
        assert b'mrbill' in body
        return data_file_contents('nominet/contact_info_example.xml')
    with mocked_session(checks, [NContact.base], [NContact]) as s:
        r = s['contact'].info('mrbill', 'passy')
    assert r.data['trad_name'] == 'Big enterprises'
    assert r.data['org'] == 'Company.'

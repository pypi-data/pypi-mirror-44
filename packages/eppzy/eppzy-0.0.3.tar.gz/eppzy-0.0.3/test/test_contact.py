from eppzy.rfc5733_contact import Contact
from util import mocked_session, data_file_contents


def test_contact_create():
    def checks(body):
        assert b'sop' in body
        return data_file_contents('rfc5733/contact_create_example.xml')
    with mocked_session(checks, [Contact]) as s:
        r = s['contact'].create(
            'cid', 'nam', 'org', ['street'], 'city', 'sop', 'RC32 NFQ', 'GB',
            '+44.382919', 'fax', 'bob@bob.bob', '', disclose=['name'])
    assert r.data['id'] == 'sh8013'


def test_contact_info():
    def checks(body):
        assert b'passable' in body
        return data_file_contents('rfc5733/contact_info_example.xml')
    with mocked_session(checks, [Contact]) as s:
        r = s['contact'].info('cid', 'passable')
    assert r.data['city'] == 'Dulles'
    assert r.data['street'] == ['123 Example Dr.', 'Suite 100']
    assert r.data['disclose'] == []
    assert r.data['undisclose'] == ['voice', 'email']


def test_contact_update():
    def checks(body):
        assert b'Frodo' in body
        return data_file_contents('rfc5733/contact_update_example.xml')
    with mocked_session(checks, [Contact]) as s:
        r = s['contact'].update(
            'conid', state_or_province='The Shire', name='Frodo',
            email='a@hob.bit', street=['Hobbity Road'], undisclose=['addr'])
    assert 'completed' in r.msg

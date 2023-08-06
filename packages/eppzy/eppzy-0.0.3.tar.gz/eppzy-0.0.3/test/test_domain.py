from eppzy.rfc5731_domain import Domain
from util import mocked_session, data_file_contents


def test_minimal_domain_info():
    d = Domain(None)
    xml, pr = d.info('dname')
    assert xml.find('command/info') is not None
    resp = d._parse_response(
        data_file_contents('rfc5731/domain_info_example.xml'))
    r = pr(resp.data)
    assert r['name'] == 'example.com'


def test_full_domain_info():
    def checks(body):
        assert b'dname' in body
        assert b'domain-1.0' in body
        return data_file_contents('rfc5731/domain_info_full_example.xml')
    with mocked_session(checks, [Domain]) as s:
        r = s['domain'].info('dname')
    assert r.data['name'] == 'example.com'
    assert r.data['host'] == ['ns1.example.com', 'ns2.example.com']
    assert r.data['registrant'] == 'jd1234'

from mock import Mock, patch

from eppzy.rfc5730_epp import EPP
from eppzy.rfc5733_contact import Contact
from eppzy.nominet import NContact
from eppzy.session import session


def test_session():
    with patch('eppzy.session.connection'):
        mock_epp = Mock(spec=EPP)
        with patch('eppzy.session.EPP', lambda _: mock_epp):
            mock_epp.recv_greeting.return_value = {
                'objUris': {'urn:ietf:params:xml:ns:contact-1.0'},
                'extensions': {
                    'http://www.nominet.org.uk/epp/xml/contact-nom-ext-1.0'}
            }
            s = session([Contact], [NContact], 'h', 12, 'someone', 'somepass')
            with s as objs:
                assert 'contact' in objs
                assert type(objs['contact']._wrapee).__name__ == 'NomContact'

import xml.etree.ElementTree as ET

from eppzy.bases import (EPPMapping, UnexpectedServerMessageType)


class EPP(EPPMapping):
    def recv_greeting(self):
        xml = self._transp.recv()
        e = ET.fromstring(xml)
        se = self._get_in_xmlns(self._epp_ns_url)
        ses = self._get_all_xmlns(self._epp_ns_url)
        g = se(e, 'greeting')
        m = se(g, 'svcMenu')
        if g:
            return {
                'svID': se(g, 'svID').text,
                'objURIs': {n.text for n in ses(m, 'objURI')},
                'extensions': frozenset(n.text for n in ses(
                    se(m, 'svcExtension'), 'extURI'))
            }
        else:
            raise UnexpectedServerMessageType(xml.decode('utf8'))

    def login(self, objUris, extnUris, client_id, password):
        rootElem, l, se = self._cmd_node('login')
        se(l, 'clID').text = client_id
        se(l, 'pw').text = password
        opts = se(l, 'options')
        se(opts, 'version').text = '1.0'
        se(opts, 'lang').text = 'en'
        svcs = se(l, 'svcs')
        for objUri in objUris:
            se(svcs, 'objURI').text = objUri
        if extnUris:
            sext = se(svcs, 'svcExtension')
            for extnUri in extnUris:
                se(sext, 'extUri').text = extnUri
        return (rootElem, lambda r: r)

    def logout(self):
        rootElem, l, se = self._cmd_node('logout')
        return (rootElem, lambda r: r)

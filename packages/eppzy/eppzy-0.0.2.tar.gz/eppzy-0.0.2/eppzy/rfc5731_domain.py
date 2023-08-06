from eppzy.bases import EPPMapping, object_handler, extract_optional


@object_handler('domain', 'urn:ietf:params:xml:ns:domain-1.0')
class Domain(EPPMapping):
    def _info_response(self, resp):
        resData = self._resData(resp)
        dse = self._get_in_xmlns(self.ns_url)
        dses = self._get_all_xmlns(self.ns_url)
        i = dse(resData, 'infData')
        data = {
            'name': dse(i, 'name').text,
            'roid': dse(i, 'roid').text,
            'host': [n.text for n in dses(i, 'host')]
        }
        extract_optional(dse, i, data, 'registrant')
        extract_optional(dse, i, data, 'crDate')
        extract_optional(dse, i, data, 'exDate')
        return data

    def info(self, domain_name, domain_pw=''):
        rootElem, d, se = self._cmd_node('info')
        se(d, 'name', attrib={'hosts': 'all'}).text = domain_name
        ai = se(d, 'authInfo')
        se(ai, 'pw').text = domain_pw
        return (rootElem, self._info_response)

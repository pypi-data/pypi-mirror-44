from .rfc5733_contact import Contact


class Extension:
    @classmethod
    def obj_uri(cls):
        return cls.base.ns_url


class NContact(Extension):
    base = Contact
    ext_uri = 'http://www.nominet.org.uk/epp/xml/contact-nom-ext-1.0'
    ext_name = 'contact-nom'

    @classmethod
    def wrap(cls, base):
        class NomContact(base):
            def _extend(self, x, ext_subtag, trad_name, type_, co_no):
                ex = self._ensure_child(x, 'extension')
                n, se = self._ns_node(
                    ex, ext_subtag, cls.ext_name, cls.ext_uri)
                if trad_name is not None:
                    se(n, 'trad-name').text = trad_name
                if type_ is not None:
                    se(n, 'type').text = type_
                if co_no is not None:
                    se(n, 'co-no').text = co_no
                return x

            def create(self, *a, trad_name=None, type_=None, co_no=None, **k):
                x, pr = super().create(*a, **k)
                return self._extend(x, 'create', trad_name, type_, co_no), pr

            def update(self, *a, trad_name=None, type_=None, co_no=None, **k):
                x, pr = super().update(*a, **k)
                return self._extend(x, 'update', trad_name, type_, co_no), pr

            def _info_response(self, resp):
                data = super()._info_response(resp)
                ext = self._get_extension(resp)
                se = self._get_in_xmlns(cls.ext_uri)
                infData = se(ext, 'infData')
                data['trad_name'] = se(infData, 'trad-name').text
                data['type_'] = se(infData, 'type').text
                data['co_no'] = se(infData, 'co-no').text
                return data
        return NomContact

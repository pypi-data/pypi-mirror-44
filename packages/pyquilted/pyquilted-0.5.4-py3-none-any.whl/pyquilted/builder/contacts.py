from pyquilted.quilted.contact_factory import ContactFactory
from pyquilted.quilted.contacts_list import ContactsList


class ContactsBuilder:
    """Contacts data mapper object"""
    def __init__(self, contacts_odict):
        self.contacts = ContactsList()
        self.odict = contacts_odict

    def deserialize(self):
        for key, val in self.odict.items():
            self._add_contact(ContactFactory.create(key, val))
        return self.contacts

    def _add_contact(self, contact):
        if contact:
            self.contacts.append(contact)

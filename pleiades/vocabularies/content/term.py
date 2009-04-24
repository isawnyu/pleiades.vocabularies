from zope.interface import implements
from Products.ATVocabularyManager.config import *
if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import *
else:
    from Products.Archetypes.atapi import *

from AccessControl import ClassSecurityInfo
try:
    from Products.Archetypes.interfaces.vocabulary import IVocabularyTerm
except ImportError:
    from Products.ATVocabularyManager.backports import IVocabularyTerm
    
from Products.ATVocabularyManager.tools import registerVocabularyTerm
from Products.ATVocabularyManager.types.simple.term import SimpleVocabularyTerm

from pleiades.vocabularies.config import PROJECTNAME
from pleiades.vocabularies.content.interfaces import IPleiadesVocabularyTerm


class PleiadesVocabularyTerm(SimpleVocabularyTerm):
    
    implements(IPleiadesVocabularyTerm)
    security = ClassSecurityInfo()
    portal_type = meta_type = 'PleiadesVocabularyTerm'
    archetype_name = 'PleiadesVocabularyTerm'
    _at_rename_after_creation = True
    
    __implements__ = getattr(BaseContent,'__implements__',()) + (IVocabularyTerm,)

    factory_type_information = {
        'allowed_content_types': tuple(),
        'allow_discussion': 1,
        'immediate_view':'base_view',
        'global_allow': 1,
        'filter_content_types': 1,
        }
        
    schema = BaseSchema + Schema((
        StringField('id',
            required=0, ## Still actually required, but
                        ## the widget will supply the missing value
                        ## on non-submits
            mode="rw",
            accessor="getId",
            mutator="setId",
            default='',
            widget=StringWidget(
                label="Key",
                label_msgid="label_key",
                description="Should not contain spaces, underscores or mixed case. ",
                description_msgid="help_key",
                i18n_domain="atvocabularymanager"),
            ),
        StringField('title',
            required=1,
            searchable=0,
            default='',
            accessor='Title',
            widget=StringWidget(
                label="Value",
                label_msgid="label_value",
                i18n_domain="atvocabularymanager"),
        )),
    )

    aliases = { 
        '(Default)' : 'base_view', 
        'view' : 'base_view', 
        'edit' : 'base_edit', 
    }
        
    # Methods
    # methods from Interface IVocabularTerm
    

    def getTermKey(self):
        """
        """
        if not HAS_LINGUA_PLONE or self.isCanonical():
            return self.getId()
        else:
            return self.getCanonical().getId()
    
    def getTermValue(self, lang=None):
        """
        """
        if not lang is None:
            # if we ask for a specific language, we try to
            # provide it
            trans = self.getTranslation(lang)
            # if not found, we return the title of the current term
            return trans and trans.Title() or self.Title()
        return self.Title()
    
    def getTermKeyPath(self):
        # terms of flat vocabularies can savely return their key
        return [self.getTermKey(),]

    def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
        request = REQUEST or self.REQUEST
        values = request.form

        if values.has_key('title'):
            orig_title = self.Title()
            
        BaseContent.processForm(self, data, metadata, REQUEST, values)

    def update(self, *args, **kwargs):
        if kwargs.has_key('title'):
            orig_title = self.Title()

        BaseContent.update(self, *args, **kwargs)

    edit = update

    factory_type_information={}
    actions=()


registerType(PleiadesVocabularyTerm, PROJECTNAME)
registerVocabularyTerm(PleiadesVocabularyTerm, 'PleiadesVocabulary')

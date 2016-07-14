from zope import schema
from zope.interface import Interface

from collective.z3cform.datagridfield.registry import DictRow


class IPeriodSchema(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')
    description = schema.TextLine(title=u'Description', required=False)
    lower_bound = schema.Int(title=u'Lower')
    upper_bound = schema.Int(title=u'Upper')
    same_as = schema.URI(title=u'Same As', required=False)
    hidden = schema.Bool(title=u'Hidden', default=False)


class IVocabTerm(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')


class IVocabTermExtended(Interface):
    id = schema.TextLine(title=u'Id')
    title = schema.TextLine(title=u'Title')
    description = schema.TextLine(title=u'Description', required=False)
    same_as = schema.URI(title=u'Same As', required=False)
    hidden = schema.Bool(title=u'Hidden', default=False)


class IPleiadesSettings(Interface):
    """Global Pleiades site specific settings"""

    time_periods = schema.List(
        title=u'Time Periods',
        value_type=DictRow(
            title=u'Period',
            schema=IPeriodSchema,
        )
    )

    place_types = schema.List(
        title=u'Place Types',
        value_type=DictRow(
            title=u'Place Type',
            schema=IVocabTermExtended,
        )
    )

    arch_remains = schema.List(
        title=u'Archaeological Remains',
        value_type=DictRow(
            title=u'Remains Entry',
            schema=IVocabTerm,
        )
    )

    location_types = schema.List(
        title=u'Location Types',
        value_type=DictRow(
            title=u'Location Entry',
            schema=IVocabTerm,
        )
    )

    relationship_types = schema.List(
        title=u'Relationship Types',
        value_type=DictRow(
            title=u'Relationship Entry',
            schema=IVocabTermExtended,
        )
    )

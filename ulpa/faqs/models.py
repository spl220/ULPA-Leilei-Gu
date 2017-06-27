from __future__ import unicode_literals, absolute_import

from django.db import models

from ulpa.utils.model_helpers import CreatedModifiedMixin


class FAQ(CreatedModifiedMixin, models.Model):

    question = models.CharField(max_length=256)

    answer = models.TextField()

    faq_category = models.ForeignKey('faqs.FAQCategory',
                                     related_name='faqs')

    class Meta(object):
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __unicode__(self):
        return u'%s' % (self.question)


class FAQCategory(CreatedModifiedMixin, models.Model):
    """

    """
    name = models.CharField(max_length=256)

    class Meta(object):
        """

        """
        verbose_name = "FAQ category"
        verbose_name_plural = "FAQ categories"

    def __unicode__(self):
        return u'%s' % (self.name)

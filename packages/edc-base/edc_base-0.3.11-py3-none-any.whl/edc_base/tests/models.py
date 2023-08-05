from dateutil.relativedelta import relativedelta
from django.db import models
from edc_utils import get_utcnow
from edc_model.models import HistoricalRecords
from edc_model.models import BaseUuidModel, BaseModel, ReportStatusModelMixin
from edc_model.validators import datetime_is_future, date_is_future
from edc_model.validators import datetime_not_future, date_not_future
from edc_model.validators import CellNumber, TelephoneNumber
from edc_sites.models import SiteModelMixin


def get_future_date():
    return get_utcnow() + relativedelta(days=10)


class TestSimpleModel(BaseModel):

    f1 = models.CharField(max_length=10, null=True)


class TestBaseModel(BaseModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)


class TestBaseModelWithStatus(BaseModel, ReportStatusModelMixin):

    f1 = models.CharField(max_length=10)


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)
    f5_other = models.CharField(max_length=10, null=True)


class TestModelWithHistory(SiteModelMixin, BaseUuidModel):

    f1 = models.CharField(max_length=10, default="1")

    history = HistoricalRecords()


class TestModelWithDateValidators(BaseModel):

    datetime_not_future = models.DateTimeField(
        validators=[datetime_not_future], default=get_utcnow
    )

    date_not_future = models.DateField(validators=[date_not_future], default=get_utcnow)

    datetime_is_future = models.DateTimeField(
        validators=[datetime_is_future], default=get_future_date
    )

    date_is_future = models.DateField(
        validators=[date_is_future], default=get_future_date
    )


class TestModelWithPhoneValidators(BaseModel):

    cell = models.CharField(max_length=25, null=True, validators=[CellNumber])
    tel = models.CharField(max_length=25, null=True, validators=[TelephoneNumber])

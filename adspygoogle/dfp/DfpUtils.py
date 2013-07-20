#!/usr/bin/python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Handy utility functions."""

__author__ = 'api.sgrinberg@gmail.com (Stan Grinberg)'

import gzip
import os
import StringIO
import time
import urllib

from adspygoogle.common import SanityCheck
from adspygoogle.common import Utils
from adspygoogle.common.Errors import ValidationError
from adspygoogle.dfp import DEFAULT_API_VERSION
from adspygoogle.dfp import LIB_HOME


def GetCurrencies():
  """Get a list of available currencies.

  Returns:
    list available currencies.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'currencies.csv'))


def GetTimezones():
  """Get a list of available timezones.

  Returns:
    list Available timezones.
  """
  return Utils.GetDataFromCsvFile(os.path.join(LIB_HOME, 'data',
                                               'timezones.csv'))


def GetAllEntitiesByStatement(client, service_name, query='', page_size=500,
                              server='https://www.google.com',
                              version=DEFAULT_API_VERSION, http_proxy=None):
  """Get all existing entities by statement.

  All existing entities are retrieved for a given statement and page size. The
  retrieval of entities works across all services. Thus, the same method can
  be used to fetch companies, creatives, ad units, line items, etc. The results,
  even if they span multiple pages, are grouped into a single list of entities.

  Args:
    client: Client an instance of Client.
    service_name: str name of the service to use.
    [optional]
    query: str a statement filter to apply, if any. The default is empty string.
    page_size: int size of the page to use. If page size is less than 0 or
               greater than 500, defaults to 500.
    server: str API server to access for this API call. The default value is
            'https://www.google.com'.
    version: str API version to use.
    http_proxy: str HTTP proxy to use.

  Returns:
    list a list of existing entities.
  """
  service = eval('client.Get%sService(server, version, http_proxy)'
                 % service_name)
  return GetAllEntitiesByStatementWithService(service, query, page_size)


def GetAllEntitiesByStatementWithService(service, query='', page_size=500,
                                         bind_vars=None):
  """Get all existing entities by statement.

  All existing entities are retrieved for a given statement and page size. The
  retrieval of entities works across all services. Thus, the same method can
  be used to fetch companies, creatives, ad units, line items, etc. The results,
  even if they span multiple pages, are grouped into a single list of entities.

  Args:
    service: ApiService an instance of the service to use.
    [optional]
    query: str a statement filter to apply, if any. The default is empty string.
    page_size: int size of the page to use. If page size is less than 0 or
               greater than 500, defaults to 500.
    bind_vars: list Key value pairs of bind variables to use with query.

  Returns:
    list a list of existing entities.
  """

  service_name = service._service_name[0:service._service_name.rfind('Service')]

  if service_name == 'Inventory':
    service_name = 'AdUnit'
  if service_name[-1] == 'y':
    method_name = service_name[:-1] + 'ies'
  else:
    method_name = service_name + 's'
  if service_name == 'Content':
    method_name = service_name
  method_name = 'Get%sByStatement' % method_name

  if page_size <= 0 or page_size > 500:
    page_size = 500

  if (query and
      (query.upper().find('LIMIT') > -1 or query.upper().find('OFFSET') > -1)):
    raise ValidationError('The filter query contains an option that is '
                          'incompatible with this method.')

  offset = 0
  all_entities = []
  while True:
    filter_statement = {
        'query': '%s LIMIT %s OFFSET %s' % (query, page_size, offset),
        'values': bind_vars
    }
    entities = eval('service.%s(filter_statement)[0].get(\'results\')'
                    % method_name)

    if not entities: break
    all_entities.extend(entities)
    if len(entities) < page_size: break
    offset += page_size
  return all_entities


def DownloadReport(report_job_id, export_format, service):
  """Download and return report data.

  Args:
    report_job_id: str ID of the report job.
    export_format: str Export format for the report file.
    service: GenericDfpService A service pointing to the ReportService.

  Returns:
    str Report data or empty string if report failed.
  """
  SanityCheck.ValidateTypes(((report_job_id, (str, unicode)),))

  # Wait for report to complete.
  status = service.GetReportJob(report_job_id)[0]['reportJobStatus']
  while status != 'COMPLETED' and status != 'FAILED':
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report job status: %s' % status
    time.sleep(30)
    status = service.GetReportJob(report_job_id)[0]['reportJobStatus']

  if status == 'FAILED':
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report process failed'
    return ''
  else:
    if Utils.BoolTypeConvert(service._config['debug']):
      print 'Report has completed successfully'

  # Get report download URL.
  report_url = service.GetReportDownloadURL(report_job_id, export_format)[0]

  # Download report.
  data = urllib.urlopen(report_url).read()
  data = gzip.GzipFile(fileobj=StringIO.StringIO(data)).read()
  return data

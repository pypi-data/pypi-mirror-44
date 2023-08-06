.. _api:

API Reference
=============

The StreamSets SDK for Python is broadly divided into abstractions for interacting with
StreamSet Data Collector and StreamSets Control Hub.

.. module:: streamsets.sdk

StreamSets Data Collector
-------------------------

Main interface
""""""""""""""
This is the main entry point used by users when interacting with SDC instances.

.. autoclass:: streamsets.sdk.DataCollector
    :members:

.. autoattribute:: sdc.DEFAULT_SDC_USERNAME
.. autoattribute:: sdc.DEFAULT_SDC_PASSWORD

Models
""""""
These models wrap and provide useful functionality for interacting with common SDC abstractions.

Alerts
^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Alert
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Alerts
    :members:

Data Rules
^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.DataDriftRule
    :members:
.. autoclass:: streamsets.sdk.sdc_models.DataRule
    :members:

History
^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.History
    :members:
.. autoclass:: streamsets.sdk.sdc_models.HistoryEntry
    :members:

Issues
^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Issue
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Issues
    :members:

Logs
^^^^
.. autoclass:: streamsets.sdk.sdc_models.Log
    :members:

Metrics
^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.MetricCounter
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricGauge
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricHistogram
    :members:
.. autoclass:: streamsets.sdk.sdc_models.MetricTimer
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Metrics
    :members:

Pipelines
^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelineBuilder
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Pipeline
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Stage
    :members:

Pipeline ACLs
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelineAcl
    :members:

Pipeline Permissions
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.PipelinePermission
    :members:
.. autoclass:: streamsets.sdk.sdc_models.PipelinePermissions
    :members:

Previews
^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Preview
    :members:

Snapshots
^^^^^^^^^
.. autoclass:: streamsets.sdk.sdc_models.Batch
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Record
    :members:
.. autoclass:: streamsets.sdk.sdc_models.RecordHeader
    :members:
.. autoclass:: streamsets.sdk.sdc_models.Snapshot
    :members:
.. autoclass:: streamsets.sdk.sdc_models.StageOutput
    :members:

Users
^^^^^
.. autoclass:: streamsets.sdk.sdc_models.User
    :members:


StreamSets Control Hub
----------------------

Main interface
""""""""""""""
This is the main entry point used by users when interacting with SCH instances.

.. autoclass:: streamsets.sdk.ControlHub
    :members:

Models
""""""
These models wrap and provide useful functionality for interacting with common SCH abstractions.

ACLs
^^^^
.. autoclass:: streamsets.sdk.sch_models.ACL
    :members:
.. autoclass:: streamsets.sdk.sch_models.ACLPermissionBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.Permission
    :members:

Classifiers
^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Classifier
    :members:

Classification Rules
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ClassificationRule
    :members:
.. autoclass:: streamsets.sdk.sch_models.ClassificationRuleBuilder
    :members:

DataCollectors
^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.DataCollector
    :members:
.. autoclass:: streamsets.sdk.sch_models.DataCollectors
    :members:

Group
^^^^^
.. autoclass:: streamsets.sdk.sch_models.Group
    :members:

Jobs
^^^^
.. autoclass:: streamsets.sdk.sch_models.Job
    :members:
.. autoclass:: streamsets.sdk.sch_models.Jobs
    :members:
.. autoclass:: streamsets.sdk.sch_models.JobBuilder
    :members:

Organizations
^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Organization
    :members:
.. autoclass:: streamsets.sdk.sch_models.Organizations
    :members:
.. autoclass:: streamsets.sdk.sch_models.OrganizationBuilder
    :members:

Pipelines
^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Pipeline
    :members:
.. autoclass:: streamsets.sdk.sch_models.Pipelines
    :members:
.. autoclass:: streamsets.sdk.sch_models.PipelineBuilder
    :members:

Protection Methods
^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ProtectionMethod
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionMethodBuilder
    :members:

Protection Policies
^^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicy
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicies
    :members:
.. autoclass:: streamsets.sdk.sch_models.ProtectionPolicyBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.PolicyProcedure
    :members:

Reports
^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Report
    :members:

Report Definitions
^^^^^^^^^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ReportDefinition
    :members:

Scheduler
^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.ScheduledTask
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskAudit
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskBaseModel
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskBuilder
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTaskRun
    :members:
.. autoclass:: streamsets.sdk.sch_models.ScheduledTasks
    :members:

Topologies
^^^^^^^^^^
.. autoclass:: streamsets.sdk.sch_models.Topology
    :members:
.. autoclass:: streamsets.sdk.sch_models.Topologies
    :members:
.. autoclass:: streamsets.sdk.sch_models.TopologyBuilder
    :members:

Users
^^^^^
.. autoclass:: streamsets.sdk.sch_models.User
    :members:
.. autoclass:: streamsets.sdk.sch_models.Users
    :members:
.. autoclass:: streamsets.sdk.sch_models.UserBuilder
    :members:

Common
------
Models used by StreamSets Data Collector and StreamSets Control Hub:

.. autoclass:: streamsets.sdk.models.Configuration
    :members:

Exceptions
----------

.. automodule:: streamsets.sdk.exceptions
    :members:

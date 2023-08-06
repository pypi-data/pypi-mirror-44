# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from hestia.humanize import humanize_timedelta
from marshmallow import fields, validate

from polyaxon_schemas.api.experiment import ExperimentSchema
from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.utils import UUID


class ExperimentGroupSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    uuid = UUID(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    unique_name = fields.Str(allow_none=True)
    user = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    project = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    content = fields.Str(allow_none=True)
    group_type = fields.Str(allow_none=True)
    search_algorithm = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    started_at = fields.LocalDateTime(allow_none=True)
    finished_at = fields.LocalDateTime(allow_none=True)
    total_run = fields.Str(allow_none=True)
    concurrency = fields.Int(allow_none=True)
    num_experiments = fields.Int(allow_none=True)
    num_scheduled_experiments = fields.Int(allow_none=True)
    num_pending_experiments = fields.Int(allow_none=True)
    num_running_experiments = fields.Int(allow_none=True)
    num_succeeded_experiments = fields.Int(allow_none=True)
    num_failed_experiments = fields.Int(allow_none=True)
    num_stopped_experiments = fields.Int(allow_none=True)
    last_status = fields.Str(allow_none=True)
    has_tensorboard = fields.Bool(allow_none=True)
    experiments = fields.Nested(ExperimentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ExperimentGroupConfig


class ExperimentGroupConfig(BaseConfig):
    SCHEMA = ExperimentGroupSchema
    IDENTIFIER = 'experiment_group'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'id', 'unique_name', 'user', 'concurrency', 'created_at', 'last_status',
        'started_at', 'finished_at', 'total_run', 'group_type', 'search_algorithm'
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at', 'started_at', 'finished_at']

    def __init__(self,
                 unique_name=None,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 name=None,
                 description=None,
                 content=None,
                 uuid=None,
                 project=None,
                 num_experiments=None,
                 tags=None,
                 group_type=None,
                 search_algorithm=None,
                 num_scheduled_experiments=None,
                 num_pending_experiments=None,
                 num_running_experiments=None,
                 num_succeeded_experiments=None,
                 num_failed_experiments=None,
                 num_stopped_experiments=None,
                 last_status=None,
                 has_tensorboard=False,
                 created_at=None,
                 updated_at=None,
                 started_at=None,
                 finished_at=None,
                 concurrency=None,
                 experiments=None,
                 total_run=None):
        self.unique_name = unique_name
        self.id = id
        self.user = user
        self.name = name
        self.description = description
        self.content = content
        self.uuid = uuid
        self.project = project
        self.tags = tags
        self.group_type = group_type
        self.search_algorithm = search_algorithm
        self.num_experiments = num_experiments
        self.num_scheduled_experiments = num_scheduled_experiments
        self.num_pending_experiments = num_pending_experiments
        self.num_running_experiments = num_running_experiments
        self.num_succeeded_experiments = num_succeeded_experiments
        self.num_failed_experiments = num_failed_experiments
        self.num_stopped_experiments = num_stopped_experiments
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.started_at = self.localize_date(started_at)
        self.finished_at = self.localize_date(finished_at)
        self.has_tensorboard = has_tensorboard
        self.last_status = last_status
        self.concurrency = concurrency
        self.experiments = experiments
        if all([self.started_at, self.finished_at]):
            self.total_run = humanize_timedelta((self.finished_at - self.started_at).seconds)


class GroupStatusSchema(BaseSchema):
    id = fields.Int()
    uuid = UUID()
    experiment_group = fields.Int()
    created_at = fields.LocalDateTime()
    status = fields.Str()
    message = fields.Str(allow_none=True)
    details = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return GroupStatusConfig


class GroupStatusConfig(BaseConfig):
    SCHEMA = GroupStatusSchema
    IDENTIFIER = 'GroupStatus'
    DATETIME_ATTRIBUTES = ['created_at']
    DEFAULT_EXCLUDE_ATTRIBUTES = ['experiment_group', 'uuid', 'details']

    def __init__(self,
                 id,  # pylint:disable=redefined-builtin
                 uuid,
                 experiment_group,
                 created_at,
                 status,
                 message=None,
                 details=None):
        self.id = id
        self.uuid = uuid
        self.experiment_group = experiment_group
        self.created_at = self.localize_date(created_at)
        self.status = status
        self.message = message
        self.details = details


class ProjectSchema(BaseSchema):
    id = fields.Int(allow_none=True)
    name = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'))
    user = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    owner = fields.Str(validate=validate.Regexp(regex=r'^[-a-zA-Z0-9_]+\Z'), allow_none=True)
    unique_name = fields.Str(allow_none=True)
    uuid = UUID(allow_none=True)
    description = fields.Str(allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    has_code = fields.Bool(allow_none=True)
    created_at = fields.LocalDateTime(allow_none=True)
    updated_at = fields.LocalDateTime(allow_none=True)
    num_experiments = fields.Int(allow_none=True)
    num_independent_experiments = fields.Int(allow_none=True)
    num_experiment_groups = fields.Int(allow_none=True)
    num_jobs = fields.Int(allow_none=True)
    num_builds = fields.Int(allow_none=True)
    has_tensorboard = fields.Bool(allow_none=True)
    has_notebook = fields.Bool(allow_none=True)
    experiment_groups = fields.Nested(ExperimentGroupSchema, many=True, allow_none=True)
    experiments = fields.Nested(ExperimentSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return ProjectConfig


class ProjectConfig(BaseConfig):
    SCHEMA = ProjectSchema
    IDENTIFIER = 'project'
    DEFAULT_EXCLUDE_ATTRIBUTES = [
        'id', 'uuid', 'description', 'updated_at',
        'experiment_groups', 'experiments', 'has_code', 'owner', 'user'
    ]
    DATETIME_ATTRIBUTES = ['created_at', 'updated_at']

    def __init__(self,
                 name,
                 id=None,  # pylint:disable=redefined-builtin
                 user=None,
                 owner=None,
                 unique_name=None,
                 uuid=None,
                 description=None,
                 is_public=True,
                 tags=None,
                 has_code=False,
                 has_tensorboard=False,
                 has_notebook=False,
                 created_at=None,
                 updated_at=None,
                 num_experiments=0,
                 num_experiment_groups=0,
                 num_independent_experiments=0,
                 num_jobs=0,
                 num_builds=0,
                 experiments=None,
                 experiment_groups=None):
        self.name = name
        self.id = id
        self.user = user
        self.owner = owner
        self.unique_name = unique_name
        self.uuid = uuid
        self.description = description
        self.is_public = is_public
        self.tags = tags
        self.has_code = has_code
        self.has_tensorboard = has_tensorboard
        self.has_notebook = has_notebook
        self.created_at = self.localize_date(created_at)
        self.updated_at = self.localize_date(updated_at)
        self.num_experiments = num_experiments
        self.num_independent_experiments = num_independent_experiments
        self.num_experiment_groups = num_experiment_groups
        self.num_jobs = num_jobs
        self.num_builds = num_builds
        self.experiments = experiments
        self.experiment_groups = experiment_groups

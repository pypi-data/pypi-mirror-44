import os
from logging import getLogger
from typing import Optional

from gumo.core.injector import injector
from gumo.core.domain import GumoConfiguration
from gumo.core.domain import GoogleCloudLocation
from gumo.core.domain import GoogleCloudProjectID
from gumo.core.domain import ApplicationPlatform
from gumo.core.exceptions import ConfigurationError

logger = getLogger('gumo.core')


class ConfigurationFactory:
    @classmethod
    def build(
            cls,
            google_cloud_project: Optional[str] = None,
            google_cloud_location: Optional[str] = None,
    ) -> GumoConfiguration:

        project_id = GoogleCloudProjectID(
            google_cloud_project if google_cloud_project else os.environ.get('GOOGLE_CLOUD_PROJECT')
        )

        location = GoogleCloudLocation(
            google_cloud_location if google_cloud_location else os.environ.get('GOOGLE_CLOUD_LOCATION')
        )

        is_google_platform = 'GAE_DEPLOYMENT_ID' in os.environ and 'GAE_INSTANCE' in os.environ
        application_platform = ApplicationPlatform.GoogleAppEngine if is_google_platform else ApplicationPlatform.Local

        if application_platform == ApplicationPlatform.Local:
            if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
                raise ConfigurationError('Envrionment variable "GOOGLE_APPLICATION_CREDENTIALS" is required.')

        return GumoConfiguration(
            google_cloud_project=project_id,
            google_cloud_location=location,
            application_platform=application_platform,
        )


def configure(
        google_cloud_project: Optional[str] = None,
        google_cloud_location: Optional[str] = None,
):
    conifg = ConfigurationFactory.build(
        google_cloud_project=google_cloud_project,
        google_cloud_location=google_cloud_location,
    )
    logger.debug(f'Gumo is configured, config={conifg}')

    if 'GOOGLE_CLOUD_PROJECT' not in os.environ:
        logger.debug('Environment Variable "GOOGLE_CLOUD_PROJECT" is not configured.')
        project_id = conifg.google_cloud_project.value
        os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
        logger.debug(f'Environment Variable "GOOGLE_CLOUD_PROJECT" has been updated to {project_id}')

    injector.binder.bind(GumoConfiguration, conifg)

    return conifg

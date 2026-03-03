from unittest.mock import MagicMock, patch

import pytest

from app.data_output_configuration.databricks.schema import (
    DatabricksTechnicalAssetConfiguration,
)
from app.data_output_configuration.glue.schema import (
    GlueTechnicalAssetConfiguration,
)
from app.data_output_configuration.postgresql.schema import (
    PostgreSQLTechnicalAssetConfiguration,
)
from app.data_output_configuration.redshift.schema import (
    RedshiftTechnicalAssetConfiguration,
)
from app.data_output_configuration.snowflake.schema import (
    SnowflakeTechnicalAssetConfiguration,
)


def _get_access_granularity_field(metadata):
    return next((f for f in metadata if f.name == "access_granularity"), None)


class TestAccessGranularityNotRequired:
    """Verify that access_granularity is not required in all platform schemas.

    The access_granularity field has an initial_value (schema), so marking it
    as required blocks form submission unnecessarily (issue #2705).
    """

    @pytest.mark.parametrize(
        "config_class",
        [
            SnowflakeTechnicalAssetConfiguration,
            DatabricksTechnicalAssetConfiguration,
            GlueTechnicalAssetConfiguration,
            RedshiftTechnicalAssetConfiguration,
            PostgreSQLTechnicalAssetConfiguration,
        ],
    )
    def test_access_granularity_not_required(self, config_class):
        db = MagicMock()
        with patch.object(config_class, "get_platform_options", return_value=[]):
            metadata = config_class.get_ui_metadata(db)

        field = _get_access_granularity_field(metadata)
        assert field is not None, "access_granularity field not found"
        assert field.required is False
        assert field.radio is not None
        assert field.radio.initial_value is not None

"""Experiments

Revision ID: 1ff6af4be6ef
Revises: d63936aaa65c
Create Date: 2025-03-23 19:54:22.260879

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "1ff6af4be6ef"
down_revision: Union[str, None] = "d63936aaa65c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    device_type_enum = sa.Enum("access_point", "sniffer", "terminal", name="devicetype")
    device_type_enum.create(op.get_bind())

    op.create_table(
        "experiments",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )
    op.drop_table("measurements")
    op.add_column("devices", sa.Column("experiment_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.add_column(
        "devices", sa.Column("type", sa.Enum("access_point", "sniffer", "terminal", name="devicetype"), nullable=False)
    )
    op.add_column("devices", sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column(
        "devices",
        "last_seen",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
    op.create_foreign_key(None, "devices", "experiments", ["experiment_id"], ["name"])
    op.add_column("structures", sa.Column("experiment_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_foreign_key(None, "structures", "experiments", ["experiment_id"], ["name"])
    op.alter_column(
        "uploaded_files",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "uploaded_files",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
    op.drop_constraint(None, "structures", type_="foreignkey")
    op.drop_column("structures", "experiment_id")
    op.drop_constraint(None, "devices", type_="foreignkey")
    op.alter_column(
        "devices",
        "last_seen",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
    op.drop_column("devices", "description")
    op.drop_column("devices", "type")
    op.drop_column("devices", "experiment_id")
    op.create_table(
        "measurements",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("device_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("uploaded_file_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("happened_at", postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
        sa.Column("additional_data", postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["devices.mac_address"], name="measurements_device_id_fkey"),
        sa.ForeignKeyConstraint(
            ["uploaded_file_id"], ["uploaded_files.id"], name="measurements_uploaded_file_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="measurements_pkey"),
    )
    op.drop_table("experiments")

    # Drop ENUM type manually on downgrade
    device_type_enum = sa.Enum("access_point", "sniffer", "terminal", name="devicetype")
    device_type_enum.drop(op.get_bind())

"""Uploaded files

Revision ID: f753a3e060f5
Revises: 651efce107b7
Create Date: 2024-11-04 11:08:55.018121

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "f753a3e060f5"
down_revision: Union[str, None] = "651efce107b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "uploaded_files",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("device_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("file_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("file_path", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column(
            "state", sa.Enum("pending", "processing", "done", "failed", "archived", name="filestate"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["devices.mac_address"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("uploaded_files")
    # ### end Alembic commands ###

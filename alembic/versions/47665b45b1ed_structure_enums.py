"""Door structure

Revision ID: 47665b45b1ed
Revises: 1ff6af4be6ef
Create Date: 2025-03-25 21:43:08.115391

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from alembic_postgresql_enum import TableReference

# revision identifiers, used by Alembic.
revision: str = "47665b45b1ed"
down_revision: Union[str, None] = "1ff6af4be6ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        enum_schema="public",
        enum_name="structuretype",
        new_values=["room", "wall", "table", "seat", "door"],
        affected_columns=[TableReference(table_schema="public", table_name="structures", column_name="category")],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.sync_enum_values(
        enum_schema="public",
        enum_name="structuretype",
        new_values=["room", "wall"],
        affected_columns=[TableReference(table_schema="public", table_name="structures", column_name="category")],
        enum_values_to_rename=[],
    )
    # ### end Alembic commands ###

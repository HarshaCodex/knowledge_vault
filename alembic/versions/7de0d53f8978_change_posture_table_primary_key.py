"""Change posture table primary key

Revision ID: 7de0d53f8978
Revises: 
Create Date: 2025-12-09 22:31:40.105929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7de0d53f8978"
down_revision: Union[str, Sequence[str], None] = "81efe2960764"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # This assumes the 'id' column might not exist yet.
    # If it does exist, you might need to remove this line.
    op.add_column(
        "posture",
        sa.Column("id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")),
    )

    # Drop the old primary key constraint.
    # IMPORTANT: Replace 'posture_pkey' with the actual constraint name from your database.
    # You can find it by running `\d posture` in psql.
    op.drop_constraint("posture_pkey", "posture", type_="primary")

    # Create the new primary key on the 'id' column.
    op.create_primary_key("posture_pkey", "posture", ["id"])

    # Now that user_id is not part of the PK, it can be made nullable if needed.
    op.alter_column("posture", "user_id", existing_type=sa.UUID(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Revert the changes in reverse order.
    op.alter_column("posture", "user_id", existing_type=sa.UUID(), nullable=False)

    # Drop the new primary key.
    op.drop_constraint("posture_pkey", "posture", type_="primary")

    # Re-create the old primary key (assuming it was on user_id).
    op.create_primary_key("posture_pkey", "posture", ["user_id"])

    op.drop_column("posture", "id")

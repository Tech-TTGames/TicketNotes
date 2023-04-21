"""v0.1.1.0 Integration Upgrade

Revision ID: 8c4e4c4f3661
Revises: 8c713ab3df0b
Create Date: 2023-04-21 13:27:35.953542+00:00

"""
import sqlalchemy as sa

# pylint: skip-file
from alembic import op

# revision identifiers, used by Alembic.
revision = "8c4e4c4f3661"
down_revision = "8c713ab3df0b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "general_configs",
        sa.Column(
            "integrated",
            sa.Boolean(),
            nullable=True,
            comment="Whether the bot is integrated with the main bot",
        ),
        schema="tickets_plus",
    )
    op.execute("UPDATE tickets_plus.general_configs SET integrated = FALSE")
    op.alter_column(
        "general_configs", "integrated", nullable=False, schema="tickets_plus"
    )
    op.add_column(
        "tickets",
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=True,
            comment="Unique discord-provided user ID",
        ),
        schema="tickets_plus",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("tickets", "user_id", schema="tickets_plus")
    op.drop_column("general_configs", "integrated", schema="tickets_plus")
    # ### end Alembic commands ###

"""Sale details buy and sell price added

Revision ID: 2782049668b5
Revises: bf69bc22975b
Create Date: 2024-07-28 19:11:39.738842

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2782049668b5'
down_revision = 'bf69bc22975b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales_details', sa.Column('sell_price', sa.Float(), nullable=False))
    op.add_column('sales_details', sa.Column('buy_price', sa.Float(), nullable=False))
    op.drop_column('sales_details', 'price')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sales_details', sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('sales_details', 'buy_price')
    op.drop_column('sales_details', 'sell_price')
    # ### end Alembic commands ###

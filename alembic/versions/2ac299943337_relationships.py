"""relationships

Revision ID: 2ac299943337
Revises: 
Create Date: 2024-07-09 18:38:14.123886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ac299943337'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('codebar', sa.String(), nullable=True),
    sa.Column('codebarinner', sa.String(), nullable=True),
    sa.Column('codebarmaster', sa.String(), nullable=True),
    sa.Column('unit', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('buy', sa.Float(), nullable=False),
    sa.Column('retailsale', sa.Float(), nullable=False),
    sa.Column('wholesale', sa.Float(), nullable=False),
    sa.Column('inventory', sa.Integer(), nullable=True),
    sa.Column('min_inventory', sa.Integer(), nullable=True),
    sa.Column('department', sa.String(), nullable=True),
    sa.Column('origin_id', sa.Integer(), nullable=True),
    sa.Column('box', sa.Integer(), nullable=True),
    sa.Column('master', sa.Integer(), nullable=True),
    sa.Column('lastupdate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('codebar'),
    sa.UniqueConstraint('codebarinner'),
    sa.UniqueConstraint('codebarmaster')
    )
    op.create_index(op.f('ix_products_id'), 'products', ['id'], unique=False)
    op.create_index(op.f('ix_products_key'), 'products', ['key'], unique=False)
    op.create_table('sales',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('seller', sa.String(), nullable=False),
    sa.Column('costumer', sa.String(), nullable=True),
    sa.Column('total', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sales_products',
    sa.Column('sale_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['sales.id'], ),
    sa.PrimaryKeyConstraint('sale_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sales_products')
    op.drop_table('sales')
    op.drop_index(op.f('ix_products_key'), table_name='products')
    op.drop_index(op.f('ix_products_id'), table_name='products')
    op.drop_table('products')
    # ### end Alembic commands ###

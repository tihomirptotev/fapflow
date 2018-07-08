"""empty message

Revision ID: 63e1856f5660
Revises: 7b4eec5bf6a2
Create Date: 2018-07-08 15:18:23.054339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63e1856f5660'
down_revision = '7b4eec5bf6a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint(None, 'roles', type_='foreignkey')
    op.drop_column('roles', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'roles', 'users', ['user_id'], ['id'])
    op.drop_table('user_roles')
    # ### end Alembic commands ###
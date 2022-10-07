"""empty message

Revision ID: 7af19243e11a
Revises: 7e50843c1605
Create Date: 2022-10-07 17:33:36.660803

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7af19243e11a'
down_revision = '7e50843c1605'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('class_model',
    sa.Column('class_id', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('class_id')
    )
    op.add_column('students', sa.Column('class_id', sa.String(length=3), nullable=True))
    op.create_foreign_key(None, 'students', 'class_model', ['class_id'], ['class_id'])
    op.drop_column('students', 'class_')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('class_', mysql.VARCHAR(length=3), nullable=True))
    op.drop_constraint(None, 'students', type_='foreignkey')
    op.drop_column('students', 'class_id')
    op.drop_table('class_model')
    # ### end Alembic commands ###
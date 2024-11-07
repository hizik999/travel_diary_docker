"""v1_0

Revision ID: 7b4d84016399
Revises: 
Create Date: 2024-11-06 16:47:14.889166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b4d84016399'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_labels_id'), 'labels', ['id'], unique=False)
    op.create_table('motions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('user_imei', sa.String(), nullable=False),
    sa.Column('acceleration_x', sa.Float(), nullable=True),
    sa.Column('acceleration_y', sa.Float(), nullable=True),
    sa.Column('acceleration_z', sa.Float(), nullable=True),
    sa.Column('gyro_x', sa.Float(), nullable=True),
    sa.Column('gyro_y', sa.Float(), nullable=True),
    sa.Column('gyro_z', sa.Float(), nullable=True),
    sa.Column('magnetometer_x', sa.Float(), nullable=True),
    sa.Column('magnetometer_y', sa.Float(), nullable=True),
    sa.Column('magnetometer_z', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Float(), nullable=True),
    sa.Column('label_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['label_id'], ['labels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_motions_id'), 'motions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_motions_id'), table_name='motions')
    op.drop_table('motions')
    op.drop_index(op.f('ix_labels_id'), table_name='labels')
    op.drop_table('labels')
    # ### end Alembic commands ###

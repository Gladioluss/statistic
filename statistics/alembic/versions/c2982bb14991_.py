"""empty message

Revision ID: c2982bb14991
Revises: 
Create Date: 2023-12-05 17:10:39.756161

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2982bb14991'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Project',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('real_project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Project_id'), 'Project', ['id'], unique=False)
    op.create_table('Time',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('day_of_month', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('quarter', sa.Integer(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('day_of_week', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Time_id'), 'Time', ['id'], unique=False)
    op.create_table('Subproject',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('real_subproject_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Subproject_id'), 'Subproject', ['id'], unique=False)
    op.create_table('Object',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('real_object_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('object_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('subproject_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['subproject_id'], ['Subproject.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Object_id'), 'Object', ['id'], unique=False)
    op.create_table('Defect',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('object_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('defect_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('defect_description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['object_id'], ['Object.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Defect_id'), 'Defect', ['id'], unique=False)
    op.create_table('Progress',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('time_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('object_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('progress', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['object_id'], ['Object.id'], ),
    sa.ForeignKeyConstraint(['time_id'], ['Time.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Progress_id'), 'Progress', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Progress_id'), table_name='Progress')
    op.drop_table('Progress')
    op.drop_index(op.f('ix_Defect_id'), table_name='Defect')
    op.drop_table('Defect')
    op.drop_index(op.f('ix_Object_id'), table_name='Object')
    op.drop_table('Object')
    op.drop_index(op.f('ix_Subproject_id'), table_name='Subproject')
    op.drop_table('Subproject')
    op.drop_index(op.f('ix_Time_id'), table_name='Time')
    op.drop_table('Time')
    op.drop_index(op.f('ix_Project_id'), table_name='Project')
    op.drop_table('Project')
    # ### end Alembic commands ###
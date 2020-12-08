"""initial schema

Revision ID: f42bc8b30dbe
Revises: 
Create Date: 2020-11-29 10:53:29.820847

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f42bc8b30dbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_created_at'), 'user', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_first_name'), 'user', ['first_name'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    op.create_index(op.f('ix_user_updated_at'), 'user', ['updated_at'], unique=False)
    op.create_table('team',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_team_created_at'), 'team', ['created_at'], unique=False)
    op.create_index(op.f('ix_team_id'), 'team', ['id'], unique=False)
    op.create_index(op.f('ix_team_name'), 'team', ['name'], unique=False)
    op.create_index(op.f('ix_team_updated_at'), 'team', ['updated_at'], unique=False)
    op.create_table('dataroom',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('team_fk', postgresql.UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['team_fk'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataroom_created_at'), 'dataroom', ['created_at'], unique=False)
    op.create_index(op.f('ix_dataroom_id'), 'dataroom', ['id'], unique=False)
    op.create_index(op.f('ix_dataroom_name'), 'dataroom', ['name'], unique=True)
    op.create_index(op.f('ix_dataroom_updated_at'), 'dataroom', ['updated_at'], unique=False)
    op.create_table('team_user',
    sa.Column('team_fk', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_fk', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['team_fk'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_fk'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('team_user')
    op.drop_index(op.f('ix_dataroom_updated_at'), table_name='dataroom')
    op.drop_index(op.f('ix_dataroom_name'), table_name='dataroom')
    op.drop_index(op.f('ix_dataroom_id'), table_name='dataroom')
    op.drop_index(op.f('ix_dataroom_created_at'), table_name='dataroom')
    op.drop_table('dataroom')
    op.drop_index(op.f('ix_team_updated_at'), table_name='team')
    op.drop_index(op.f('ix_team_name'), table_name='team')
    op.drop_index(op.f('ix_team_id'), table_name='team')
    op.drop_index(op.f('ix_team_created_at'), table_name='team')
    op.drop_table('team')
    op.drop_index(op.f('ix_user_updated_at'), table_name='user')
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_first_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_created_at'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
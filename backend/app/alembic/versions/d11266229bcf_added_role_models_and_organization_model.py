"""added role models and organization model

Revision ID: d11266229bcf
Revises: e461feb811d5
Create Date: 2021-02-16 06:29:37.816314

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd11266229bcf'
down_revision = 'e461feb811d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organization_created_at'), 'organization', ['created_at'], unique=False)
    op.create_index(op.f('ix_organization_id'), 'organization', ['id'], unique=False)
    op.create_index(op.f('ix_organization_name'), 'organization', ['name'], unique=True)
    op.create_index(op.f('ix_organization_updated_at'), 'organization', ['updated_at'], unique=False)
    op.create_table('organization_roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('organization_id', 'user_id')
    )
    op.create_index(op.f('ix_organization_roles_created_at'), 'organization_roles', ['created_at'], unique=False)
    op.create_index(op.f('ix_organization_roles_id'), 'organization_roles', ['id'], unique=False)
    op.create_index(op.f('ix_organization_roles_updated_at'), 'organization_roles', ['updated_at'], unique=False)
    op.create_table('dataroom_roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('team_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('dataroom_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['dataroom_id'], ['dataroom.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('dataroom_id', 'user_id')
    )
    op.create_index(op.f('ix_dataroom_roles_created_at'), 'dataroom_roles', ['created_at'], unique=False)
    op.create_index(op.f('ix_dataroom_roles_id'), 'dataroom_roles', ['id'], unique=False)
    op.create_index(op.f('ix_dataroom_roles_updated_at'), 'dataroom_roles', ['updated_at'], unique=False)
    op.create_table('team_roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('team_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('team_id', 'user_id')
    )
    op.create_index(op.f('ix_team_roles_created_at'), 'team_roles', ['created_at'], unique=False)
    op.create_index(op.f('ix_team_roles_id'), 'team_roles', ['id'], unique=False)
    op.create_index(op.f('ix_team_roles_updated_at'), 'team_roles', ['updated_at'], unique=False)
    op.drop_table('team_user')
    op.add_column('dataroom', sa.Column('organization_fk', postgresql.UUID(as_uuid=True), nullable=False))
    op.drop_constraint('dataroom_team_fk_fkey', 'dataroom', type_='foreignkey')
    op.create_foreign_key(None, 'dataroom', 'organization', ['organization_fk'], ['id'])
    op.drop_column('dataroom', 'team_fk')
    op.add_column('team', sa.Column('organization_fk', postgresql.UUID(as_uuid=True), nullable=False))
    op.create_foreign_key(None, 'team', 'organization', ['organization_fk'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'team', type_='foreignkey')
    op.drop_column('team', 'organization_fk')
    op.add_column('dataroom', sa.Column('team_fk', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'dataroom', type_='foreignkey')
    op.create_foreign_key('dataroom_team_fk_fkey', 'dataroom', 'team', ['team_fk'], ['id'])
    op.drop_column('dataroom', 'organization_fk')
    op.create_table('team_user',
    sa.Column('team_fk', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('user_fk', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['team_fk'], ['team.id'], name='team_user_team_fk_fkey'),
    sa.ForeignKeyConstraint(['user_fk'], ['user.id'], name='team_user_user_fk_fkey')
    )
    op.drop_index(op.f('ix_team_roles_updated_at'), table_name='team_roles')
    op.drop_index(op.f('ix_team_roles_id'), table_name='team_roles')
    op.drop_index(op.f('ix_team_roles_created_at'), table_name='team_roles')
    op.drop_table('team_roles')
    op.drop_index(op.f('ix_dataroom_roles_updated_at'), table_name='dataroom_roles')
    op.drop_index(op.f('ix_dataroom_roles_id'), table_name='dataroom_roles')
    op.drop_index(op.f('ix_dataroom_roles_created_at'), table_name='dataroom_roles')
    op.drop_table('dataroom_roles')
    op.drop_index(op.f('ix_organization_roles_updated_at'), table_name='organization_roles')
    op.drop_index(op.f('ix_organization_roles_id'), table_name='organization_roles')
    op.drop_index(op.f('ix_organization_roles_created_at'), table_name='organization_roles')
    op.drop_table('organization_roles')
    op.drop_index(op.f('ix_organization_updated_at'), table_name='organization')
    op.drop_index(op.f('ix_organization_name'), table_name='organization')
    op.drop_index(op.f('ix_organization_id'), table_name='organization')
    op.drop_index(op.f('ix_organization_created_at'), table_name='organization')
    op.drop_table('organization')
    # ### end Alembic commands ###
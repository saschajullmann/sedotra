"""added constraints to documents table and column extension and mime-type

Revision ID: e461feb811d5
Revises: edc3dc2fa9e2
Create Date: 2020-12-16 10:51:14.042861

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e461feb811d5'
down_revision = 'edc3dc2fa9e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('extension', sa.String(), nullable=False))
    op.add_column('document', sa.Column('mime_type', sa.String(), nullable=False))
    op.alter_column('document', 'file_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('document', 'md5_sum',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.create_unique_constraint('_file_per_dataroom', 'document', ['file_name', 'extension', 'md5_sum', 'dataroom_fk'])
    op.create_unique_constraint('_name_per_dataroom', 'document', ['name', 'dataroom_fk'])
    op.create_index(op.f('ix_document_extension'), 'document', ['extension'], unique=False)
    op.create_index(op.f('ix_document_mime_type'), 'document', ['mime_type'], unique=False)
    op.drop_index('ix_document_name', table_name='document')
    op.create_index(op.f('ix_document_name'), 'document', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_document_name'), table_name='document')
    op.create_index('ix_document_name', 'document', ['name'], unique=True)
    op.drop_index(op.f('ix_document_mime_type'), table_name='document')
    op.drop_index(op.f('ix_document_extension'), table_name='document')
    op.drop_constraint('_name_per_dataroom', 'document', type_='unique')
    op.drop_constraint('_file_per_dataroom', 'document', type_='unique')
    op.alter_column('document', 'md5_sum',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('document', 'file_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('document', 'mime_type')
    op.drop_column('document', 'extension')
    # ### end Alembic commands ###
"""Initial DB structure

Revision ID: 9cd1e651df8e
Revises: 
Create Date: 2022-03-29 22:04:28.093586

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9cd1e651df8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scan_targets',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('target', sa.TEXT(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('run_reports',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('scan_target_id', sa.BIGINT(), nullable=False),
                    sa.Column('scanner', sa.TEXT(), nullable=False),
                    sa.Column('args', sa.TEXT(), nullable=False),
                    sa.Column('started_at', sa.TIME(), nullable=False),
                    sa.Column('finished_at', sa.TIME(), nullable=False),
                    sa.Column('nmap_version', sa.TEXT(), nullable=False),
                    sa.Column('xml_version', sa.TEXT(), nullable=False),
                    sa.ForeignKeyConstraint(['scan_target_id'], ['scan_targets.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('hosts',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('run_id', sa.BIGINT(), nullable=False),
                    sa.Column('address', sa.TEXT(), nullable=True),
                    sa.Column('address_type', sa.TEXT(), nullable=True),
                    sa.ForeignKeyConstraint(['run_id'], ['run_reports.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('os_versions',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('host_id', sa.BIGINT(), nullable=False),
                    sa.Column('name', sa.TEXT(), nullable=True),
                    sa.Column('accuracy', sa.SMALLINT(), nullable=True),
                    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('host_id')
                    )
    op.create_table('ports',
                    sa.Column('id', sa.BIGINT(), nullable=False),
                    sa.Column('host_id', sa.BIGINT(), nullable=False),
                    sa.Column('port_num', sa.Integer(), nullable=False),
                    sa.Column('protocol', sa.TEXT(), nullable=True),
                    sa.Column('state', sa.TEXT(), nullable=False),
                    sa.Column('reason', sa.TEXT(), nullable=True),
                    sa.Column('service_name', sa.TEXT(), nullable=True),
                    sa.Column('service_product', sa.TEXT(), nullable=True),
                    sa.Column('version', sa.TEXT(), nullable=True),
                    sa.Column('os_type', sa.TEXT(), nullable=True),
                    sa.Column('extra_info', sa.TEXT(), nullable=True),
                    sa.ForeignKeyConstraint(['host_id'], ['hosts.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('ports')
    op.drop_table('os_versions')
    op.drop_table('hosts')
    op.drop_table('run_reports')
    op.drop_table('scan_targets')

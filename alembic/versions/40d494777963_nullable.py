"""nullable

Revision ID: 40d494777963
Revises: 37cab33633c7
Create Date: 2024-09-03 10:24:38.880042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '40d494777963'
down_revision: Union[str, None] = '37cab33633c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # add nullable field on table attendees
    op.alter_column('attendees', 'iin', existing_type=sa.VARCHAR(
        length=12), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document_types',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='document_types_pkey'),
                    sa.UniqueConstraint(
                        'doc_code', name='document_types_doc_code_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('ix_document_types_id',
                    'document_types', ['id'], unique=False)
    op.create_table('countries',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('country_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('cis_flag', sa.BOOLEAN(),
                              autoincrement=False, nullable=False),
                    sa.Column('country_iso', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='countries_pkey'),
                    sa.UniqueConstraint(
                        'country_code', name='countries_country_code_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('ix_countries_id', 'countries', ['id'], unique=False)
    op.create_table('categories',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('category_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('index', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='categories_pkey'),
                    sa.UniqueConstraint(
                        'category_code', name='categories_category_code_key')
                    )
    op.create_index('ix_categories_id', 'categories', ['id'], unique=False)
    op.create_table('users',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('email', sa.VARCHAR(length=150),
                              autoincrement=False, nullable=True),
                    sa.Column('password', sa.VARCHAR(length=255),
                              autoincrement=False, nullable=True),
                    sa.Column('workplace', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('iin', sa.VARCHAR(length=12),
                              autoincrement=False, nullable=False),
                    sa.Column('phone_number', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('is_accreditator', sa.BOOLEAN(),
                              autoincrement=False, nullable=False),
                    sa.Column('admin', sa.BOOLEAN(),
                              autoincrement=False, nullable=False),
                    sa.Column('last_signed_at', postgresql.TIMESTAMP(
                        timezone=True), autoincrement=False, nullable=True),
                    sa.Column('login_count', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='users_pkey'),
                    sa.UniqueConstraint('email', name='users_email_key'),
                    sa.UniqueConstraint('iin', name='users_iin_key'),
                    postgresql_ignore_search_path=False
                    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_table('attendees',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('surname', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('firstname', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('patronymic', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('birth_date', sa.DATE(),
                              autoincrement=False, nullable=True),
                    sa.Column('post', sa.VARCHAR(length=1024),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_series', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('iin', sa.VARCHAR(length=12),
                              autoincrement=False, nullable=False),
                    sa.Column('doc_number', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_begin', sa.DATE(),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_end', sa.DATE(),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_issue', sa.VARCHAR(length=50),
                              autoincrement=False, nullable=True),
                    sa.Column('photo', sa.VARCHAR(length=1024),
                              autoincrement=False, nullable=True),
                    sa.Column('doc_scan', sa.VARCHAR(length=1024),
                              autoincrement=False, nullable=True),
                    sa.Column('visit_object', sa.VARCHAR(length=1024),
                              autoincrement=False, nullable=True),
                    sa.Column('transcription', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('sex_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('country_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('request_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('doc_type_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['country_id'], ['countries.id'], name='attendees_country_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['doc_type_id'], ['document_types.id'], name='attendees_doc_type_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['request_id'], ['requests.id'], name='attendees_request_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['sex_id'], ['sexes.id'], name='attendees_sex_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='attendees_pkey')
                    )
    op.create_index('ix_attendees_iin', 'attendees', ['iin'], unique=False)
    op.create_index('ix_attendees_id', 'attendees', ['id'], unique=False)
    op.create_table('permissions',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('user_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('type_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['type_id'], ['permission_types.id'], name='permissions_type_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], name='permissions_user_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='permissions_pkey')
                    )
    op.create_index('ix_permissions_id', 'permissions', ['id'], unique=False)
    op.create_table('users_events',
                    sa.Column('user_id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('event_id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['event_id'], ['events.id'], name='users_events_event_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['user_id'], ['users.id'], name='users_events_user_id_fkey'),
                    sa.PrimaryKeyConstraint('user_id', 'event_id',
                                            name='users_events_pkey')
                    )
    op.create_table('sexes',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('sex_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='sexes_pkey'),
                    sa.UniqueConstraint('sex_code', name='sexes_sex_code_key')
                    )
    op.create_index('ix_sexes_id', 'sexes', ['id'], unique=False)
    op.create_table('requests',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('event_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('status', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('created_by_id', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['created_by_id'], ['users.id'], name='requests_created_by_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['event_id'], ['events.id'], name='requests_event_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='requests_pkey')
                    )
    op.create_index('ix_requests_name', 'requests', ['name'], unique=False)
    op.create_index('ix_requests_id', 'requests', ['id'], unique=False)
    op.create_table('events',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('number', sa.INTEGER(),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('event_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('date_start', sa.DATE(),
                              autoincrement=False, nullable=True),
                    sa.Column('date_end', sa.DATE(),
                              autoincrement=False, nullable=True),
                    sa.Column('city_id', sa.VARCHAR(),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['city_id'], ['cities.id'], name='events_city_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='events_pkey')
                    )
    op.create_index('ix_events_id', 'events', ['id'], unique=False)
    op.create_index('ix_events_event_code', 'events',
                    ['event_code'], unique=True)
    op.create_table('cities',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('city_code', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=False),
                    sa.Column('index', sa.VARCHAR(length=20),
                              autoincrement=False, nullable=True),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='cities_pkey'),
                    sa.UniqueConstraint(
                        'city_code', name='cities_city_code_key')
                    )
    op.create_index('ix_cities_id', 'cities', ['id'], unique=False)
    op.create_table('permission_types',
                    sa.Column('id', sa.VARCHAR(length=36),
                              autoincrement=False, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=False),
                    sa.Column('namekz', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('nameen', sa.VARCHAR(length=128),
                              autoincrement=False, nullable=True),
                    sa.Column('sequence_id', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        'now()'), autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint('id', name='permission_types_pkey')
                    )
    op.create_index('ix_permission_types_id',
                    'permission_types', ['id'], unique=False)
    # ### end Alembic commands ###

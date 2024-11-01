"""empty message

Revision ID: 37cab33633c7
Revises: 7130fce393b4
Create Date: 2024-02-23 15:33:34.577038

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37cab33633c7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    if not op.get_bind().dialect.has_table(op.get_bind(), "ranks"):
        # Создание таблицы departments
        op.create_table(
            'ranks',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(length=128)),

            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "positions"):
        # Создание таблицы departments
        op.create_table(
            'positions',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),

            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "departments"):
        # Создание таблицы departments
        op.create_table(
            'departments',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),

            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "managements"):
        # Создание таблицы managements
        op.create_table(
            'managements',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id')),
            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "divisions"):
        # Создание таблицы divisions
        op.create_table(
            'divisions',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column('management_id', sa.Integer, sa.ForeignKey('managements.id')),
            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "statuses"):
        # Создание таблицы statuses
        op.create_table(
            'statuses',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column('start_date', sa.Date, nullable=True),
            sa.Column('end_date', sa.Date, nullable=True),
            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "employers"):
        # Создание таблицы employers
        op.create_table(
            'employers',
            sa.Column('id', sa.Integer, primary_key=True, index=True),
            sa.Column('surname', sa.String(length=128), nullable=False),
            sa.Column('firstname', sa.String(length=128), nullable=False),
            sa.Column('patronymic', sa.String(length=128), nullable=True),
            sa.Column('sort', sa.Integer, nullable=False),
            sa.Column("photo", sa.String(length=1024), nullable=True),
            sa.Column("note", sa.Text, nullable=True),

            sa.Column('rank_id', sa.Integer, sa.ForeignKey('ranks.id')),
            sa.Column('division_id', sa.Integer, sa.ForeignKey('divisions.id')),
            sa.Column('status_id', sa.Integer, sa.ForeignKey('statuses.id')),
            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "states"):
        # Создание таблицы states
        op.create_table(
            'states',
            sa.Column('id', sa.Integer, primary_key=True),

            sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id')),
            sa.Column('management_id', sa.Integer, sa.ForeignKey('managements.id')),
            sa.Column('division_id', sa.Integer, sa.ForeignKey('divisions.id')),
            sa.Column('position_id', sa.Integer, sa.ForeignKey('positions.id')),
            sa.Column('employer_id', sa.Integer, sa.ForeignKey('employers.id'), nullable=True, unique=True),

            sa.Column(
                'created_at', sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                'updated_at',
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "categories"):
        op.create_table(
            "categories",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column("category_code", sa.String(length=20), nullable=False, unique=True),
            sa.Column("index", sa.String(length=20), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "cities"):
        op.create_table(
            "cities",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column("city_code", sa.String(length=20), nullable=True, unique=True),
            sa.Column("index", sa.String(length=20), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "events"):
        op.create_table(
            "events",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("number", sa.Integer, nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column(
                "event_code", sa.String(length=20), nullable=False, unique=True, index=True
            ),
            sa.Column("date_start", sa.Date, nullable=True),
            sa.Column("date_end", sa.Date, nullable=True),
            sa.Column("city_id", sa.Integer(), sa.ForeignKey("cities.id"), nullable=True),
            sa.Column("lead", sa.String(length=30), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
            sa.Column("is_for_gov", sa.Boolean, default=False),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("email", sa.String(length=150), nullable=True, unique=True),
            sa.Column("password", sa.String(length=255), nullable=True),
            sa.Column("workplace", sa.String(length=128), nullable=True),
            sa.Column("iin", sa.String(length=12), nullable=False, unique=True),
            sa.Column("phone_number", sa.String(length=20), nullable=True),
            sa.Column("is_accreditator", sa.Boolean, nullable=False, default=False),
            sa.Column("admin", sa.Boolean, nullable=False, default=False),
            sa.Column("last_signed_at", sa.TIMESTAMP(timezone=True), nullable=True),
            sa.Column("login_count", sa.Integer, nullable=False, default=0),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column("employer_id", sa.Integer(), sa.ForeignKey("employers.id"), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "users_events"):
        op.create_table(
            "users_events",
            sa.Column(
                "user_id",
                sa.Integer,
                sa.ForeignKey("users.id"),
                primary_key=True,
                nullable=True,
            ),
            sa.Column(
                "event_id",
                sa.Integer,
                sa.ForeignKey("events.id"),
                primary_key=True,
                nullable=True,
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "document_types"):
        op.create_table(
            "document_types",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column("doc_code", sa.String(length=20), nullable=True, unique=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "countries"):
        # Create table for Country
        op.create_table(
            "countries",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("country_code", sa.String(length=20), nullable=True, unique=True),
            sa.Column("cis_flag", sa.Boolean, nullable=True, default=False),
            sa.Column("country_iso", sa.String(length=20), nullable=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "requests"):
        # Create table for Request
        op.create_table(
            "requests",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False, index=True),
            sa.Column("event_id", sa.Integer(), sa.ForeignKey("events.id"), nullable=False),
            sa.Column("status", sa.String(length=20), nullable=True),
            sa.Column(
                "created_by_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "attendees"):
        # Create table for Attendee
        op.create_table(
            "attendees",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("surname", sa.String(length=128), nullable=False),
            sa.Column("firstname", sa.String(length=128), nullable=False),
            sa.Column("patronymic", sa.String(length=128), nullable=True),
            sa.Column("birth_date", sa.Date, nullable=True),
            sa.Column("post", sa.String(length=20), nullable=True),
            sa.Column("doc_series", sa.String(length=128), nullable=True),
            sa.Column("iin", sa.String(length=12), nullable=False, index=True),
            sa.Column("doc_number", sa.String(length=20), nullable=True),
            sa.Column("doc_begin", sa.Date, nullable=True),
            sa.Column("doc_end", sa.Date, nullable=True),
            sa.Column("doc_issue", sa.String(length=50), nullable=True),
            sa.Column("photo", sa.String(length=1024), nullable=True),
            sa.Column("doc_scan", sa.String(length=1024), nullable=True),
            sa.Column("visit_object", sa.String(length=1024), nullable=True),
            sa.Column("transcription", sa.String(length=128), nullable=True),
            sa.Column("stick_id", sa.String(length=128), nullable=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
            sa.Column("sex", sa.String(length=128), nullable=True),
            sa.Column(
                "country_id", sa.Integer(), sa.ForeignKey("countries.id"), nullable=False
            ),
            sa.Column(
                "request_id", sa.Integer(), sa.ForeignKey("requests.id"), nullable=False
            ),
            sa.Column(
                "doc_type_id",
                sa.Integer(),
                sa.ForeignKey("document_types.id"),
                nullable=False,
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "permission_types"):
        # Create table for Permission Types
        op.create_table(
            "permission_types",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("name", sa.String(length=128), nullable=False),
            sa.Column("namekz", sa.String(length=128), nullable=True),
            sa.Column("nameen", sa.String(length=128), nullable=True),
            sa.Column("sequence_id", sa.Integer, nullable=False, default=0),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    if not op.get_bind().dialect.has_table(op.get_bind(), "permissions"):
        # Create table for Permissions
        op.create_table(
            "permissions",
            sa.Column("id", sa.Integer, primary_key=True, index=True),
            sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
            sa.Column(
                "type_id",
                sa.Integer(),
                sa.ForeignKey("permission_types.id"),
                nullable=False,
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False, server_default=sa.func.now()
            ),
            sa.Column(
                "updated_at",
                sa.DateTime,
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("categories")
    op.drop_table("cities")
    op.drop_table("events")
    op.drop_table("users")
    op.drop_table("users_events")
    op.drop_table("document_types")
    op.drop_table("requests")
    op.drop_table("attendees")
    op.drop_table("countries")
    op.drop_table("sexes")
    op.drop_table("departments")
    op.drop_table("managements")
    op.drop_table("divisions")
    op.drop_table("positions")
    op.drop_table("ranks")
    op.drop_table("statuses")
    op.drop_table("employers")
    op.drop_table("states")

    # ### end Alembic commands ###

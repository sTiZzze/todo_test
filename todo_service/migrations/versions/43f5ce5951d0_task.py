"""task

Revision ID: 43f5ce5951d0
Revises: 
Create Date: 2023-11-29 18:39:27.882667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from config.database import Base
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '43f5ce5951d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abstract_instance',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_abstract_instance_id'), 'abstract_instance', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username'),
    postgresql_inherits='abstract_instance'
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('todo_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('completed', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    postgresql_inherits='abstract_instance'
    )
    op.create_index(op.f('ix_todo_list_id'), 'todo_list', ['id'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('status', postgresql.ENUM('in_progress', 'done', name='status_task'), server_default=sa.text("'in_progress'"), nullable=False),
    sa.Column('todo_list_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['todo_list_id'], ['todo_list.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    postgresql_inherits='abstract_instance'
    )
    op.create_index(op.f('ix_task_id'), 'task', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_todo_list_id'), table_name='todo_list')
    op.drop_table('todo_list')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_abstract_instance_id'), table_name='abstract_instance')
    op.drop_table('abstract_instance')
    # ### end Alembic commands ###
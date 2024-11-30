"""Add fs_uniquifier to users table and other changes for flask-security-too

Revision ID: 233778ef6fe3
Revises: 
Create Date: 2024-11-29 22:45:19.524978

"""
import uuid
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '233778ef6fe3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add fs_uniquifier column with default values for existing rows
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fs_uniquifier', sa.String(length=64), nullable=True))

    # Populate fs_uniquifier for existing rows
    conn = op.get_bind()
    users_table = sa.Table(
        'users', sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fs_uniquifier', sa.String(length=64))
    )
    for user in conn.execute(users_table.select()):
        conn.execute(
            users_table.update().where(users_table.c.id == user.id).values(fs_uniquifier=str(uuid.uuid4()))
        )

    # Set fs_uniquifier column to NOT NULL and unique after populating existing rows
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('fs_uniquifier', nullable=False)  # Ensure NOT NULL constraint
        batch_op.create_unique_constraint('uq_users_fs_uniquifier', ['fs_uniquifier'])
        batch_op.drop_column('image_file')  # Remove the image_file column



def downgrade():
    # Drop the fs_uniquifier column and its unique constraint
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_fs_uniquifier', type_='unique')
        batch_op.drop_column('fs_uniquifier')

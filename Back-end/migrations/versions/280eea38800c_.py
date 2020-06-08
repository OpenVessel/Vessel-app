"""empty message

Revision ID: 280eea38800c
Revises: 
Create Date: 2020-06-05 12:41:42.133004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '280eea38800c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('image_file', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('dicom',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_uploaded', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('dicom_stack', sa.LargeBinary(), nullable=False),
    sa.Column('thumbnail', sa.LargeBinary(), nullable=False),
    sa.Column('file_count', sa.Integer(), nullable=True),
    sa.Column('session_id', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('date_uploaded', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dicom_form_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_uploaded', sa.DateTime(), nullable=False),
    sa.Column('study_name', sa.String(length=300), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('session_id', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['dicom.session_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dicom_form_data')
    op.drop_table('upload')
    op.drop_table('dicom')
    op.drop_table('user')
    # ### end Alembic commands ###
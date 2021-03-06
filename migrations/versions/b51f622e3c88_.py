"""empty message

Revision ID: b51f622e3c88
Revises: b9d950f105be
Create Date: 2021-03-05 16:08:02.011062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b51f622e3c88'
down_revision = 'b9d950f105be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('answer', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text("'1'"))

    # ### end Alembic commands ###

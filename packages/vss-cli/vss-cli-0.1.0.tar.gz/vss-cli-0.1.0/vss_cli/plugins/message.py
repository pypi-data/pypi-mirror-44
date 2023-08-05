"""Token Management plugin for VSS CLI (vss-cli)."""
import click
from vss_cli.cli import pass_context
from vss_cli import const
from vss_cli.config import Configuration
from vss_cli.helper import format_output


@click.group(
    'message',
    short_help='Manage VSS Messages.'
)
@pass_context
def cli(ctx: Configuration):
    """Manage VSS Messages."""
    ctx.load_config()


@cli.command(
    'ls',
    short_help='list user message'
)
@click.option('-f', '--filter', type=click.STRING,
              help='apply filter')
@click.option('-s', '--sort', type=click.STRING,
              help='apply sorting ')
@click.option('-a', '--show-all', is_flag=True,
              help='show all results')
@click.option('-c', '--count', type=int,
              help='size of results')
@click.option('-p', '--page', is_flag=True,
              help='page results in a less-like format')
@pass_context
def message_ls(
        ctx: Configuration, filter, page,
        sort, show_all, count
):
    """List messages based on:

        Filter list in the following format <field_name>,<operator>,<value>
        where operator is eq, ne, lt, le, gt, ge, like, in.
        For example: valid,eq,false

            vss-cli message ls -f kind,eq,Notice

        Sort list in the following format <field_name>,<asc|desc>. For example:

            vss-cli message ls -s created_on,desc

    """
    columns = ctx.columns or const.COLUMNS_MESSAGE_MIN
    params = dict()
    if filter:
        params['filter'] = filter
    if sort:
        params['sort'] = sort
    # make request
    _requests = ctx.get_user_messages(
        show_all=show_all,
        per_page=count, **params)
    # format output
    output = format_output(
        ctx,
        _requests,
        columns=columns,
    )
    # page results
    if page:
        click.echo_via_pager(output)
    else:
        click.echo(output)


@cli.command(
    'get',
    help='Display user message info.'
)
@click.argument('mid', type=int, required=True)
@pass_context
def message_get(ctx: Configuration, mid):
    """Get given user message id info"""
    obj = ctx.get_user_message(mid)
    columns = ctx.columns or const.COLUMNS_MESSAGE
    click.echo(
        format_output(
            ctx,
            [obj],
            columns=columns,
            single=True
        )
    )


@cli.group(
    'set',
    short_help='Set given user message attribute.')
@pass_context
def message_set(ctx):
    """Update given user message id info"""


@message_set.command(
    'ack',
    short_help='Acknowledge user message'
)
@click.argument('mid', type=int, required=True, nargs=-1)
@click.option('-s', '--summary', is_flag=True,
              help='Print request summary')
@pass_context
def message_set_ack(ctx, mid, summary):
    result = []
    with click.progressbar(mid) as ids:
        for i in ids:
            result.append(ctx.ack_user_message(i))
    if summary:
        for res in result:
            click.echo(
                format_output(
                    ctx,
                    [res],
                    columns=[('STATUS', 'status')],
                    single=True
                )
            )

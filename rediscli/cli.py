import json
import click
from cmd2 import Cmd, make_option, options, Cmd2TestCase
from RedisClient import RedisClient
import config
from pygments import highlight
import pygments.formatters
from tabulate import tabulate
from pygments.lexers import JsonLexer
from wcwidth import wcswidth


class CmdLineApp(Cmd):
    def do_list(self, arg, opts=None):
        data = config.list_conns()
        header = ["ID","Name","Host","Port","DB","comments"]
        # tabulate.WIDE_CHARS_MODE = True
        # print_table(header,data)
        print tabulate(data,headers=header)
    @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
              make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
              make_option('-r', '--repeat', type="int", help="output [n] times")
              ])
    def do_conn(self,arg, opts=None):
        (host,port,db) = config.get_conn(int(arg))
        self.prompt = "%s:%s > " % (host,str(db))
        self.conn = RedisClient(host,port,db)

    # @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
    #           make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
    #           make_option('-r', '--repeat', type="int", help="output [n] times")
    #           ])
    def do_get(self,arg, opts=None):
        data = self.conn.get(arg)
        txt = highlight(unicode(data, 'UTF-8'), JsonLexer(), pygments.formatters.TerminalFormatter(bg="dark"))
        print txt.rstrip('\r\n').decode('raw_unicode_escape')

    def do_keys(self, arg, opts=None):
        print self.conn.keys(arg)




@click.command()
@click.option('--as-cowboy', '-c', is_flag=True, help='Greet as a cowboy.')
@click.argument('name', default='world', required=False)
def main(name, as_cowboy):
    """My Tool does one thing, and one thing well."""
    greet = 'Howdy' if as_cowboy else 'Hello'
    click.echo('{0}, {1}.'.format(greet, name))
    # prompt = HelloWorld()
    # prompt.prompt = '> '
    # prompt.cmdloop()
    app = CmdLineApp()
    app.prompt = "> "
    app.cmdloop()


if __name__ == '__main__':
    main()

import requests
import click
import time
import logging

logging.basicConfig(format="[%(asctime)s][%(levelname)s] %(message)s", level=logging.INFO)

session = requests.session()
session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, " \
                                "like Gecko) Chrome/107.0.0.0 Safari/537.36"
session.headers["Content-Type"] = "application/x-www-form-urlencoded"

@click.group()
@click.version_option("v1.0.0")
def main():
    """Magic applied to NUIST Laboratory learning website"""
    pass


@click.command('login')
@click.argument('id', nargs=1, type=str)
@click.argument('password', nargs=1, type=str)
def login(id, password):
    data = f"xuehao={id}&password={password}&postflag=1&cmd=login&role=0&%CC%E1%BD%BB=%B5%C7%C2%BC"
    res = session.post("http://examsafety.nuist.edu.cn/exam_login.php", bytes(data, encoding='ISO-8859-1'))
    if res.status_code != 200:
        click.echo(f"Login failed: {res.reason}")
        return

    data = "cmd=xuexi_online"
    while True:
        res = session.post("http://examsafety.nuist.edu.cn/exam_xuexi_online.php", bytes(data, encoding='ISO-8859-1'))
        if res.status_code != 200:
            click.echo("Service failed to send sign in message")
            continue
        json = res.json()
        if json['status'] != 1:
            logging.warning("Sign message invalid")
            continue
        logging.info(f"Sign in: {json['shichang']}")
        time.sleep(60)


main.add_command(login)

if __name__ == "__main__":
    main()

import click
from pizza import Pizza, Size
import pizzeria


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('pizza')
@click.option(
    '--delivery', is_flag=True, default=False,
    help='Доставка заказанной пиццы.')
@click.option(
    '--size', default='L', type=click.Choice(Size._member_names_),
    show_default=True, help='Размер пиццы.')
def order(pizza: str, delivery: bool, size: str) -> None:
    """Заказать пиццу PIZZA размера SIZE с опциональной доставкой."""

    if pizza.title() not in Pizza.get_pizzas():
        click.echo('К сожалению, у нас нет этого блюда. Посмотрите наше меню.')
        return
    cls_pizza = Pizza.get_pizzas()[pizza.title()]
    my_pizza = cls_pizza(size=Size(size))
    click.echo(pizzeria.bake(my_pizza))
    if delivery:
        click.echo(pizzeria.delivery(my_pizza))
    else:
        click.echo(pizzeria.pickup(my_pizza))


@cli.command()
def menu() -> None:
    """Показать меню."""

    pizzas = [cls_pizza() for cls_pizza in Pizza.get_pizzas().values()]
    for pizza in pizzas:
        click.echo(pizza)


if __name__ == '__main__':
    cli()
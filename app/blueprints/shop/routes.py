from .import bp as shop
from flask import render_template, flash, redirect, url_for
from app.blueprints.api.models import Item
from flask_login import login_required, current_user

@shop.route('/products')
@login_required
def products():
    # show all products
    items = Item.query.all()
    return render_template('show_all.html.j2', items=items)

@shop.route('/get_product/<int:id>')
@login_required
def get_product(id):
    # show a single product with details
    item = Item.query.get(id)
    return render_template('item_info.html.j2', item=item)

@shop.route('/add_item/<int:id>' , methods = ['GET', 'POST'])
@login_required
def add_item(id):
    # add item to current users CART
    item = Item.query.get(id)
    if item in current_user.cart:
        flash(f'Limit 1 item per perchase.', 'is-warning')
        return redirect(url_for('shop.products'))
    else:
        current_user.item_to_add(item)
        flash(f'The item: {item.name} has been added to your cart', 'is-success')
        return redirect(url_for('shop.products'))

@shop.route('/remove_item/<int:id>')
@login_required
def remove_item(id):
    # a button that removes only one product
    item = Item.query.get(id)
    if item in current_user.cart:
        current_user.item_to_delete(item)
        flash(f'The item has been removed from your cart.', 'is-success')
        return redirect(url_for('shop.cart'))
    else:
        flash(f'Error in removing item!', 'is-warning')
        return redirect(url_for('shop.cart'))


### CART ROUTES ###

@shop.route('/cart')
@login_required
def cart():
    # view current users cart
    item = current_user.cart
    if len(list(item)) == 0:
        flash('Uh oh! Looks like your cart is empty!', 'is-warning')
        return redirect(url_for('main.index'))
    else:
        return render_template('show_cart.html.j2', item=item)
        

@shop.route('/cart_clear')
@login_required
def clear_cart():
    # clears all items in cart
    current_user.clear_cart()
    flash('You cart has been cleared!', 'is-success')
    return redirect(url_for('shop.products'))

### END CART ROUTES ###

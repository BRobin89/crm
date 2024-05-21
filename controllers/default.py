# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------


# ---- example index page ----
def index():
    sqlstmt = "SELECT SUM(o.quantity) as howmany, strain FROM orders o JOIN products p ON o.product_id = p.id GROUP BY strain"
    rows = db.executesql(sqlstmt, as_dict=True)
    return dict(rows=rows)


def about():
    return dict(message="About us")


def productz():
    return dict(message="Our products")


@auth.requires_login()
def cannalytics():
    strain_sold = "SELECT SUM(o.quantity) as howmany, strain FROM orders o JOIN products p ON o.product_id = p.id GROUP BY strain"
    category_sold = "SELECT SUM(o.quantity) as howmany, category FROM orders o JOIN products p ON o.product_id = p.id GROUP BY category"
    strain_rows = db.executesql(strain_sold, as_dict=True)
    category_rows = db.executesql(category_sold, as_dict=True)
    return dict(strain_rows=strain_rows, category_rows=category_rows)


@auth.requires_login()
def dataadmin():
    return dict(message="Hello from Cannalytics!")


@auth.requires_login()
def brands():
    grid = SQLFORM.grid(db.brands)
    return dict(grid=grid)


@auth.requires_login()
def customers():
    grid = SQLFORM.grid(db.customers)
    return dict(grid=grid)


@auth.requires_login()
def events():
    grid = SQLFORM.grid(db.events)
    return dict(grid=grid)


@auth.requires_login()
def states():
    grid = SQLFORM.grid(db.states)
    return dict(grid=grid)


@auth.requires_login()
def products():
    grid = SQLFORM.grid(db.products)
    return dict(grid=grid)


@auth.requires_login()
def orders():
    grid = SQLFORM.grid(db.orders)
    return dict(grid=grid)


# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == "GET":
        raise HTTP(403)
    return response.json({"status": "success", "email": auth.user.email})


# ---- Smart Grid (example) -----
@auth.requires_membership("admin")  # can only be accessed by members of admin groupd
def grid():
    response.view = "generic.html"  # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables:
        raise HTTP(403)
    grid = SQLFORM.smartgrid(
        db[tablename], args=[tablename], deletable=False, editable=False
    )
    return dict(grid=grid)


# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

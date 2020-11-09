from views.clientView import ClientView
from views.orderView import OrderView
from views.categoryView import CategoryView
from views.productView import ProductView
from views.searchView import SearchView
from CUI.cui import CUI

if __name__ == '__main__':
    main = CUI()
    main.addField('Products', lambda: ProductView().run())
    main.addField('Categories', lambda: CategoryView().run())
    main.addField('Orders', lambda: OrderView().run())
    main.addField('Clients', lambda: ClientView().run())

    main.addField('Search', lambda: SearchView().run())
    main.run()
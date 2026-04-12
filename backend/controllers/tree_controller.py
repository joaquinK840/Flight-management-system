from services.avl_service import tree_service

class TreeController:
    def insert_value(self, value: int):
        return tree_service.insert_node(value)

    def get_tree(self):
        return tree_service.get_tree()

    def search_value(self, value: int):
        return tree_service.search_value(value)

    def cancel_value(self, value: int):
        return tree_service.cancel_value(value)

    def delete_value(self, value: int):
        return tree_service.delete_value(value)

    def reset_tree(self):
        return tree_service.reset_tree()

tree_controller = TreeController()
